# jacobholtz.github.io

CTI writeup blog, built with Jekyll and served by GitHub Pages.

## Writing a new post

Add a file to `_posts/` named `YYYY-MM-DD-a-short-title.md` (Jekyll's own
post-parser requires the year-first filename regardless of the site's
month-day-year display format used everywhere else):

```yaml
---
title: "Your writeup title"
tags: [actor-name, malware-family, t1055]
---

Body content in markdown. Code blocks, tables, and blockquotes are all
styled — see the two posts already in _posts/ for examples of each.
```

Delete the two example posts once you've replaced them with real writeups.

## Publishing from Obsidian

Writeups get drafted in an Obsidian vault (`~/Documents/Vault` by default) and
published into this repo with `scripts/publish.py`. It never touches anything
in the vault outside the note you point it at:

```sh
python3 scripts/publish.py "/path/to/vault/Writeups/My Post/My Post.md"
```

That converts the note and stages it in git — nothing is committed until you
say so. Add `--commit` to commit it, or `--commit --push` (or just `--push`)
to also push it live. `--dry-run` shows what would happen without writing
anything.

It handles:

- Obsidian image embeds (`![[img.png]]`, `![[img.png|alt text]]`,
  `![[img.png|697]]` for a fixed width) — images are copied into
  `assets/images/<slug>/` and renamed `01.png`, `02.png`, ... so published
  URLs never contain spaces or local paste timestamps.
- `[[wiki links]]` to other vault notes — flattened to plain text (with a
  warning), since they'd point at a private note with no public page.
- `%%obsidian comments%%` — stripped, so a note-to-self never ends up in a
  public post.
- A leading `# Title` heading that just repeats the frontmatter title — the
  post layout already renders that as an H1, so a duplicate is dropped.

Run `python3 scripts/publish.py --help` for all the flags (`--date`, `--slug`,
`--vault`, `--repo`, `--force`). `--date` takes `MM/DD/YYYY`, matching the
dates shown on the site — the script converts it to the `YYYY-MM-DD` filename
Jekyll requires internally.

**One kramdown gotcha to know about:** if a writeup wraps a very long single
line (e.g. dumping obfuscated/minified code) in a raw `<pre><div>...</div></pre>`
HTML block, kramdown can lose track of where the block ends and silently stop
rendering everything after it as markdown. Use a fenced code block instead —
` ```text ... ``` ` — which the site already gives horizontal scroll via CSS,
so there's no need for the manual `overflow-x` wrapper.

## Running locally

```sh
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`. `jekyll serve` rebuilds on file changes.

## Deploying

Push to `main` — GitHub Pages builds and deploys automatically. In the repo's
**Settings → Pages**, make sure the source is set to the `main` branch, root
folder (should be the default for a `<username>.github.io` repo).

## Adding a custom domain later

1. Buy the domain from any registrar.
2. Add a `CNAME` file to the repo root containing just the domain
   (e.g. `blog.example.com`), or set it under **Settings → Pages → Custom domain**
   (GitHub will create the file for you).
3. At your DNS provider:
   - Subdomain (`blog.example.com`): add a `CNAME` record pointing to
     `jacobholtz.github.io`.
   - Apex domain (`example.com`): add `A` records pointing to GitHub's IPs
     (`185.199.108.153`, `.109.153`, `.110.153`, `.111.153`).
4. Wait for DNS to propagate, then enable **Enforce HTTPS** in Pages settings.
