# jacobholtz.github.io

CTI writeup blog, built with Jekyll and served by GitHub Pages.

## Writing a new post

Add a file to `_posts/` named `YYYY-MM-DD-a-short-title.md`:

```yaml
---
title: "Your writeup title"
tlp: amber      # clear | green | amber | red — defaults to clear
tags: [actor-name, malware-family, t1055]
---

Body content in markdown. Code blocks, tables, and blockquotes are all
styled — see the two posts already in _posts/ for examples of each.
```

Delete the two example posts once you've replaced them with real writeups.

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
