#!/usr/bin/env python3
"""Publish an Obsidian writeup into this Jekyll blog's _posts/ directory.

Usage:
    scripts/publish.py "/path/to/vault/Writeups/My Post/My Post.md"
    scripts/publish.py "<note>" --date 07/04/2026 --slug custom-slug
    scripts/publish.py "<note>" --dry-run
    scripts/publish.py "<note>" --commit
    scripts/publish.py "<note>" --commit --push

What it does:
  - Reads the note's frontmatter (title/tags) straight through.
  - Rewrites Obsidian image embeds (![[img.png]], ![[img.png|alt]],
    ![[img.png|width]]) into standard markdown/HTML, renaming each copy
    sequentially (01.png, 02.png, ...) under assets/images/<slug>/ so
    published URLs never contain spaces or local paste timestamps.
  - Flattens any [[wiki links]] to plain text, since they'd point at a
    private vault note with no public equivalent, and warns about each.
  - Strips %%obsidian comments%% so a note-to-self never leaks into a
    public post.
  - Drops a leading "# Title" heading if it just repeats the frontmatter
    title (the post layout already renders the title as an H1).
  - Writes _posts/<date>-<slug>.md and `git add`s the new files.
    --commit also commits; --push commits and pushes.

Nothing here reads or writes anything outside the note's own frontmatter,
its images, and this repo. The rest of the vault is never touched.
"""
import argparse
import datetime
import itertools
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VAULT = Path.home() / "Documents" / "Vault"

IMAGE_EMBED_RE = re.compile(r"!\[\[([^|\]]+?)(?:\|([^\]]+))?\]\]")
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^|\]]+?)(?:\|([^\]]+))?\]\]")
COMMENT_RE = re.compile(r"%%.*?%%", re.DOTALL)
SIZE_RE = re.compile(r"^\d+(x\d+)?$")


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")


def parse_frontmatter(raw):
    """Line-based YAML-ish parse: good enough for flat title/tags fields."""
    lines = raw.split("\n")
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return {}, raw

    start = i + 1
    j = start
    while j < len(lines) and lines[j].strip() != "---":
        j += 1
    if j >= len(lines):
        return {}, raw

    fields = {}
    k = 0
    fm_lines = lines[start:j]
    while k < len(fm_lines):
        line = fm_lines[k]
        if not line.strip():
            k += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            k += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value:
            fields[key] = value
            k += 1
        else:
            items = []
            k += 1
            while k < len(fm_lines) and re.match(r"^\s*-\s+", fm_lines[k]):
                items.append(re.sub(r"^\s*-\s+", "", fm_lines[k]).strip())
                k += 1
            fields[key] = items

    body = "\n".join(lines[j + 1:])
    return fields, body


def find_image(filename, note_dir, vault_root, warnings):
    for candidate in (note_dir / "images" / filename, note_dir / filename):
        if candidate.exists():
            return candidate
    matches = [p for p in vault_root.rglob(filename) if p.is_file()]
    if not matches:
        warnings.append(f"image not found anywhere in vault: {filename}")
        return None
    if len(matches) > 1:
        others = ", ".join(str(m) for m in matches[1:])
        warnings.append(f"multiple matches for {filename}, using {matches[0]} (others: {others})")
    return matches[0]


def strip_duplicate_title_heading(body, title):
    lines = body.split("\n")
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines):
        m = re.match(r"^#\s+(.*)$", lines[i].strip())
        if m and m.group(1).strip().lower() == title.strip().lower():
            del lines[i]
            return "\n".join(lines)
    return body


def process_body(body, note_dir, vault_root, slug, warnings):
    body = COMMENT_RE.sub("", body)
    used_images = []
    counter = itertools.count(1)

    def replace_embed(m):
        filename, param = m.group(1).strip(), m.group(2)
        src = find_image(filename, note_dir, vault_root, warnings)
        if src is None:
            return f"<!-- MISSING IMAGE: {filename} -->"
        dest_name = f"{next(counter):02d}{src.suffix.lower()}"
        used_images.append((src, dest_name))
        web_path = f"/assets/images/{slug}/{dest_name}"
        alt_default = filename.rsplit(".", 1)[0]

        if param and SIZE_RE.match(param.strip()):
            dims = param.strip().split("x")
            attrs = f'width="{dims[0]}"'
            if len(dims) == 2:
                attrs += f' height="{dims[1]}"'
            return f'<img src="{web_path}" alt="{alt_default}" {attrs}>'

        alt = param.strip() if param else alt_default
        return f"![{alt}]({web_path})"

    body = IMAGE_EMBED_RE.sub(replace_embed, body)

    def replace_wikilink(m):
        target, alias = m.group(1).strip(), m.group(2)
        warnings.append(f'internal link flattened to plain text: "{target}"')
        return alias.strip() if alias else target

    body = WIKILINK_RE.sub(replace_wikilink, body)

    return body, used_images


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("note", type=Path, help="Path to the Obsidian note to publish")
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT, help=f"Vault root, for locating images (default: {DEFAULT_VAULT})")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="Path to the jacobholtz.github.io repo")
    parser.add_argument("--date", default=None, help="Publish date MM/DD/YYYY (default: today)")
    parser.add_argument("--slug", default=None, help="URL slug (default: derived from title)")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing post at the destination path")
    parser.add_argument("--commit", action="store_true", help="git commit the new files after writing them")
    parser.add_argument("--push", action="store_true", help="git push after committing (implies --commit)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing files or touching git")
    args = parser.parse_args()

    if args.push:
        args.commit = True

    note_path = args.note.expanduser().resolve()
    if not note_path.is_file():
        sys.exit(f"error: no such file: {note_path}")

    vault_root = args.vault.expanduser().resolve()
    repo_root = args.repo.expanduser().resolve()

    raw = note_path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(raw)

    title = fields.get("title", "").strip().strip('"').strip("'") or note_path.stem
    tags = fields.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip("[]").split(",") if t.strip()]

    if args.date:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%m/%d/%Y").date()
        except ValueError:
            sys.exit(f"error: --date must be MM/DD/YYYY, got {args.date!r}")
    else:
        date_obj = datetime.date.today()

    # Jekyll requires _posts files to be named YYYY-MM-DD-slug.md (year-first,
    # hard requirement of its own post parser) regardless of the site's
    # month-day-year display convention used everywhere else.
    date_str = date_obj.isoformat()

    slug = args.slug or slugify(title)
    if not slug:
        sys.exit("error: could not derive a slug from the title — pass --slug explicitly")

    dest_post = repo_root / "_posts" / f"{date_str}-{slug}.md"
    image_dir = repo_root / "assets" / "images" / slug

    if dest_post.exists() and not args.force:
        sys.exit(f"error: {dest_post} already exists (pass --force to overwrite)")

    body = strip_duplicate_title_heading(body, title)

    warnings = []
    new_body, used_images = process_body(body, note_path.parent, vault_root, slug, warnings)

    tags_yaml = "[" + ", ".join(tags) + "]"
    frontmatter = f'---\ntitle: "{title}"\ntags: {tags_yaml}\n---\n'
    final_content = frontmatter + "\n" + new_body.strip("\n") + "\n"

    print(f"Title:  {title}")
    print(f"Date:   {date_obj.strftime('%m/%d/%Y')}")
    print(f"Tags:   {', '.join(tags) or '(none)'}")
    print(f"Dest:   {dest_post.relative_to(repo_root)}")
    print(f"Images: {len(used_images)} to copy -> {image_dir.relative_to(repo_root)}/")
    for w in warnings:
        print(f"  ! {w}")

    if args.dry_run:
        print("\n--dry-run: no files written, nothing staged.")
        return

    if used_images:
        image_dir.mkdir(parents=True, exist_ok=True)
        for src, dest_name in used_images:
            shutil.copy2(src, image_dir / dest_name)

    dest_post.parent.mkdir(parents=True, exist_ok=True)
    dest_post.write_text(final_content, encoding="utf-8")

    git_paths = [str(dest_post)] + [str(image_dir / dest_name) for _, dest_name in used_images]
    subprocess.run(["git", "-C", str(repo_root), "add", *git_paths], check=True)
    print(f"\nStaged {len(git_paths)} file(s) in git.")

    if args.commit:
        msg = f"Publish: {title}"
        subprocess.run(["git", "-C", str(repo_root), "commit", "-m", msg], check=True)
        print(f"Committed: {msg}")

    if args.push:
        subprocess.run(["git", "-C", str(repo_root), "push"], check=True)
        print("Pushed to origin.")
    elif args.commit:
        print("Run `git push` in the repo when you're ready to go live.")
    else:
        print("Run `git commit` in the repo (or re-run with --commit) when you're ready.")


if __name__ == "__main__":
    main()
