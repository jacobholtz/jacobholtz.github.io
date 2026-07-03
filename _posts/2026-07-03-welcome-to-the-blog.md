---
title: "Welcome to the blog"
tlp: clear
tags: [meta]
---

This is the first entry, mostly here to show how the site is put together
and to give you a working example when you write your own. Feel free to
delete this post once you've got real writeups published — see
`_posts/2026-07-01-example-malicious-loader-teardown.md` for a fuller
example of the formatting options below.

## Filing a new writeup

Drop a markdown file in `_posts/` named `YYYY-MM-DD-a-short-title.md` with
front matter like this:

```yaml
---
title: "Your writeup title"
tlp: amber      # clear | green | amber | red
tags: [lockbit, ransomware, t1486]
---
```

- **`tlp`** controls the classification bar at the top of the post. It
  defaults to `clear` (site-wide default in `_config.yml`) if you omit it.
- **`tags`** show as chips under the title and get indexed automatically
  on the [tags page]({{ '/tags/' | relative_url }}) — use them for threat
  actors, malware families, and ATT&CK technique IDs.

## What renders well

Code blocks, IOC tables, and blockquotes all have dedicated styling:

```python
def is_suspicious(pe):
    return pe.sections_named(".xdata") and pe.entropy() > 7.2
```

| Indicator | Type | Notes |
|---|---|---|
| `185.220.101.42` | IP | C2 checkin, observed 2026-06 |
| `a91f...c3` | SHA256 | Initial-stage loader |

> A blockquote renders as an analyst-note callout — good for caveats,
> confidence levels, or attribution notes that shouldn't be read as the
> main narrative.

That's the whole toolkit. Write the report, tag it, ship it.
