---
title: "Example: tearing down a fictional loader"
tlp: amber
tags: [example, loader, t1055, t1027]
---

> **This is a template, not a real report.** Every indicator, hash, and
> name below is invented for demonstration. Delete this post once you've
> read through it — it exists to show how a full writeup looks with tags,
> an ATT&CK mapping, an IOC table, and an analyst note all in play.

## Summary

A fictional loader we're calling **GhostCrate** drops a staged payload via
process hollowing into a signed system binary, then beacons out over HTTPS
using a JSON body disguised as telemetry. Observed only in a lab sample for
this template — treat all specifics as illustrative.

## Behavior

On execution, the sample:

1. Unpacks a second-stage DLL from its `.rsrc` section.
2. Hollows `svchost.exe` and maps the payload into it.
3. Establishes a beacon every 45–90 seconds with jittered timing.

```text
POST /telemetry/v2/sync HTTP/1.1
Host: cdn-edge-metrics[.]example
Content-Type: application/json

{"sid":"a91fbc3e","hb":1,"ts":1751500000}
```

> **ANALYST NOTE:** confidence in the C2 protocol details is moderate —
> this template only reflects a single fictional sample. Treat the beacon
> cadence and field names as illustrative, not a signature to hunt on.

## ATT&CK mapping

| Technique | ID | Notes |
|---|---|---|
| Process Injection | T1055 | Hollows `svchost.exe` for second-stage execution |
| Obfuscated Files or Information | T1027 | Second-stage DLL is XOR-encoded in `.rsrc` |

## Indicators (fictional)

| Indicator | Type | Notes |
|---|---|---|
| `cdn-edge-metrics[.]example` | Domain | C2, fronted behind a CDN in this scenario |
| `185.220.101.42` | IP | Observed C2 IP in the lab environment |
| `9f2c...1abe` | SHA256 | First-stage loader |
| `a91f...c3d0` | SHA256 | Second-stage payload (in-memory only) |

## Wrap-up

That's the shape of a full writeup: dek, behavior narrative, an ATT&CK
table, an IOC table, and an analyst note where confidence is worth
flagging separately from the main text.
