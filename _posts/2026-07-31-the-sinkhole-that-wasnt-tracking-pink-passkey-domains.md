---
title: "The sinkhole that wasn't: 100 days of Pink's passkey phishing infrastructure"
tags: [pink, phishing, passkeys, infrastructure, methodology]
---

Since late April I've been tracking newly-registered domains containing the string `passkey` as a way of watching one specific campaign build out its infrastructure in near-real-time. As of today that's **1,177 domains** across **247 identifiable target organizations**, **33 registrars**, and **55 distinct phishing-kit chassis**.

Full disclosure: I used Claude to help build and run the tracking pipeline, and to help write this post.

This was going to be a straightforward "here's what 100 days of a campaign looks like" writeup. Then, on 7/30, my pipeline told me that 86% of the campaign's infrastructure had been sinkholed by Palo Alto Networks overnight. That would have been the story.

It wasn't true. I want to walk through both the campaign and the mistake, because the mistake is the more useful half.

### The actor

The cluster is publicly tracked under a few names. [Okta Threat Intelligence](https://www.okta.com/blog/threat-intelligence/vishing-actors-target-microsoft-entra-passkey-enrollment-/) tracks it as **O-UNC-066**; Palo Alto Networks Unit 42 tracks it as **CL-CRI-1147**, and the crew brands itself **Pink** on its data-leak site, live since 5/31/2026. Reporting ties it to The Com, the same loose network that produced Scattered Spider, ShinyHunters, and LAPSUS$. Motivation is data extortion — per their own DLS, "our only goal is profit."

The tradecraft is what makes it worth tracking. Rather than phishing credentials, Pink phones an employee, impersonates internal IT, and walks them through **enrolling an attacker-controlled passkey** on their own Microsoft Entra account. Behind the phishing page sits an operator-driven PHP panel with roughly one-second heartbeat polling, so a human operator can steer the victim through whatever MFA the tenant actually enforces — TOTP, number-matched push, SMS OTP — in real time.

That's the part worth sitting with. Passkeys are phishing-resistant *as an authentication ceremony*. The enrollment ceremony is not. If you can talk a user into registering your authenticator, the phishing resistance is now working on the attacker's behalf: they hold a legitimate, unphishable credential on the victim's tenant, and it survives the password reset that would normally end the incident.

>Pink registers domains incorporating the word "passkey" and hangs per-victim subdomains off them, which is precisely why the campaign is so tractable to track by domain-string alone. It's an unusual amount of infrastructure hygiene to give up.

### The shape of the infrastructure

The naming convention is the whole game. Most base domains are generic passkey-themed lures — `registerpasskey.com`, `startpasskeysetup.com`, `passkeymigration.com` — and the targeted organization is carried in the *subdomain*:

```
homedepot.registerpasskey.com
staples.passkeyenlist.com
deshaw.createssopasskey.com
```

I call these base domains "chassis," because a single one gets reused across many victims. The most-reused chassis in my dataset:

| Chassis | Distinct orgs | Sample targets |
| --- | --- | --- |
| `passkeywork.com` | 23 | Americold, Hertz, Dayforce, Arrive Logistics |
| `registerpasskey.com` | 20 | BAE Systems, Home Depot, DraftKings, FM Global |
| `passkeyactivate.com` | 15 | AECOM, EOG Resources, MasTec, Hibbett |
| `passkeyuser.com` | 11 | Ecolab, Reed Smith, ResMed, SC Johnson |
| `setupmypasskey.com` | 11 | Delta Air Lines, M&T Bank, Skechers, GoodRx |
| `startpasskeysetup.com` | 11 | AMD, Marvell, Banner Health, CarMax |
| `passkeymigration.com` | 9 | Coinbase, Binance, Block, Tesla, Swyftx |
| `passkeyenlist.com` | 9 | Staples, NCR Voyix, Watco, eClinicalWorks |

A few of those chassis are thematically clean enough to be interesting on their own. `passkeymigration.com` is almost entirely crypto and payments. `createssopasskey.com`, which showed up on 7/28, is entirely asset management and finance — Bain Capital, General Catalyst, Capital Group, Neuberger Berman, and as of this week D.E. Shaw, Ally, Brookfield, and Ares. That sits alongside an existing alt-asset cluster on `addssopasskey.com` / `ssopasskey.com` (Blackstone, TPG, KKR) and a tight Chicago prop-trading pairing on `passkeyonboard.com` (DRW and Jump Trading). Somebody is working a target list sector by sector.

Overall sector distribution across the 247 organizations:

| Sector | Orgs |
| --- | --- |
| Financial Services | 61 |
| Industrial & Aerospace | 25 |
| Transportation & Logistics | 23 |
| Healthcare & Pharma | 23 |
| Technology | 22 |
| Legal | 19 |
| Retail & Consumer | 17 |
| Media, Entertainment & Hospitality | 16 |
| Energy & Utilities | 12 |
| Everything else | 29 |

Registration volume by month: 257 in April (from the 4/20 start of my window), 170 in May, 221 in June, and **479 in July** — the campaign roughly doubled its registration rate in its fourth month, which is not the shape of an operation under pressure.

Registrar concentration is heavy: GMO/Onamae.com (353), NICENIC (347), and Tucows across two entities (200) account for the large majority. Of the 1,127 domains VirusTotal had crawled, only **206 carry any detection at all**, and the highest is `newuser-passkey.com` at 19/91. Most of this infrastructure is invisible to reputation-based blocking.

### The mistake

On 7/30 I was resolving a handful of newly-discovered domains and noticed they came back as CNAMEs to `sinkhole.paloaltonetworks.com`. I re-audited all 1,167 domains I was tracking at the time. The result:

| Status | Domains |
| --- | --- |
| CNAME to `sinkhole.paloaltonetworks.com` | 1,000 (86%) |
| Still resolving to attacker infrastructure | 81 |
| No DNS record at all | 86 |

The AWS Global Accelerator cluster that had been the campaign's largest hosting group — roughly 380 domains on `13.248.169.48` / `76.223.54.146` — was down to a handful of stragglers. Better still, I thought I'd caught the takedown *in motion*: the `createssopasskey.com` chassis had resolved to live Cloudflare IPs when I first checked it that morning, and was sinkholed by the time I re-audited a few hours later.

I wrote it up as an active, in-progress takedown.

The next morning I re-ran the same audit as a routine check. **Zero of 1,166 domains were sinkholed.** 572 resolved to live infrastructure, 594 had no record. The AWS Global Accelerator cluster was back to 388 domains — exactly where it had been before it "disappeared."

`sinkhole.paloaltonetworks.com` is the [default DNS sinkhole FQDN in PAN-OS](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClGECA0). It is a **forged CNAME that a Palo Alto firewall or DNS Security subscription returns to its own protected clients** for domains it classifies as malicious. It is per-network enforcement. It says nothing whatsoever about whether a domain has been seized, suspended, or taken down anywhere else on the internet.

I had run the 7/30 audit through a resolution path sitting behind exactly that kind of enforcement. What I recorded as a global takedown was my own DNS answering a question I hadn't asked it.

Confirming the correction took three checks, all of which I should have run the first time:

- **Multiple public resolvers.** 8.8.8.8, 1.1.1.1, and 9.9.9.9 all agree the domains resolve normally, and always did.
- **NS delegation.** `passkeyenlist.com` and `createssopasskey.com` are still on Cloudflare nameservers; `passkeysignin.com` is on `dyna-ns.net`; `passkeyrunner.xyz` sits on Afternic parking. A real sinkhole operation re-delegates to the takedown provider's nameservers. None of these were touched.
- **RDAP registry status.** Every domain shows ordinary registrar lock flags (`clientTransferProhibited`, `clientUpdateProhibited`). No `serverHold`, no `clientHold`, no `pendingDelete`. Nothing was seized.

In hindsight there were three tells, and I read all three backwards:

1. **Domains that were genuinely dead came back "sinkholed" too.** A takedown cannot make a non-existent domain resolve. A forging firewall answers *any* query matching its malicious-domain list, live or not. That's why my "sinkholed" bucket swallowed the parked domains — and it's the tell I most should have caught, because it's logically impossible under the theory I'd adopted.
2. **My "takedown in progress" evidence was the resolution path changing under me.** A domain that resolves live at 09:00 and sinkholed at 14:00 looks like a takedown rolling forward. It looks identical to the queries starting to traverse a different, filtered path partway through the session. I still haven't pinned down exactly which path that was — no VPN tunnel transition appears in the logs for that window, and the upstream resolver in use now doesn't filter anything — so the honest statement is that the *mechanism* is certain and the *route* is not.
3. **An 86% sweep in a single day, with no vendor announcement anywhere.** Takedowns of this scale get blog posts. I went looking for corroboration only *after* I'd written up the finding, which is exactly the wrong order.

The uncomfortable part is that the false positive was *directionally plausible*. Unit 42 does track this actor. A Palo Alto sinkhole on a Palo Alto-tracked campaign is a coherent story, and coherence is what made me stop checking. Threat intel gives you a lot of opportunities to confirm a satisfying narrative with a single measurement.

The rule I've adopted: **never characterize takedown or sinkhole status from one resolution path.** DNS from an endpoint inside an enforced network is a measurement of your own security stack, not of the internet. Confirm against two or more public resolvers, then corroborate at the delegation layer (NS) and the registry layer (RDAP) before claiming anything about infrastructure disruption.

### What's actually live

With the illusion removed, here's the real state as of 7/31, across the full 1,177-domain corpus. 574 resolve; the hosting is far more concentrated than the registrar spread implies:

| Endpoint | Domains | Provider |
| --- | --- | --- |
| `13.248.169.48`, `76.223.54.146` | 389 | AWS Global Accelerator |
| `198.185.159.144/145`, `198.49.23.144/145` | 16 | Squarespace |
| `104.21.17.206`, `172.67.178.76` | 12 | Cloudflare (`passkeyenlist.com` chassis) |
| `185.53.179.146` | 9 | Team Internet AG (`passkeysignin.com` chassis) |
| `45.138.216.23` | 8 | MachCloud B.V. |
| `34.42.100.71` | 8 | Google Cloud (`.link`/`.info` cluster) |

One caveat on that first row, because it's the kind of thing that produces a second false positive: **AWS Global Accelerator IPs are shared anycast space.** Many unrelated AWS customers resolve into those same ranges. Co-residence there is not by itself evidence that a domain belongs to this campaign — I've confirmed several pre-window, entirely unrelated `passkey` domains sitting on the same addresses. Those 389 are campaign domains because they matched on registration date and naming convention, not because of where they're hosted.

And the campaign has not slowed down. A fresh pull today returned 11 domains I hadn't seen, including the `createssopasskey.com` finance expansion, a `passkey-testlol.com` base with an `m365.` subdomain hung off it (`45.38.20.228`), and `myssopasskey.com` — registered through NICENIC at **16:42 UTC today**, while I was writing this.

### Detection notes

Domain-string tracking works unusually well here, but the real detection opportunity is on the identity side, because the domains are cheap and the enrollment event isn't:

- **Alert on passkey/FIDO2 credential registration as a high-severity identity event**, not an informational one — particularly a registration from a new device, a new ASN, or within a short window of a helpdesk contact. This is the single control that would break the campaign.
- **Watch for enrollment following a support interaction.** The vishing call is the initial access vector; correlating helpdesk tickets against credential-registration events catches what neither signal catches alone.
- **Constrain enrollment itself** — require registration from a managed device or an existing strong credential, rather than allowing bootstrap from a session an operator can drive.
- **Hunt DNS for the pattern**, i.e. `*.passkey*` and `passkey*` resolutions from user subnets. Reputation blocking will not save you here; 82% of these domains have zero VT detections.

### IOCs

A representative sample; the campaign is at 1,177 domains and growing daily, so treat the pattern as the indicator rather than the list.

| Type | Value | Note |
| ------ | ------ | ------ |
| Domain | `passkeyenlist[.]com` | Live Cloudflare chassis, 9 targeted orgs |
| Domain | `passkeysignin[.]com` | Live, Team Internet AG, 8 subdomains |
| Domain | `createssopasskey[.]com` | Live, asset-management targeting, 8+ orgs |
| Domain | `passkey-testlol[.]com` | Registered 7/30, `m365.` subdomain |
| Domain | `myssopasskey[.]com` | Registered 7/31 16:42 UTC, NICENIC |
| Domain | `newuser-passkey[.]com` | Highest VT detection in corpus (19/91) |
| IP | `13.248.169.48`, `76.223.54.146` | AWS Global Accelerator — **shared anycast, low-fidelity** |
| IP | `104.21.17.206`, `172.67.178.76` | Cloudflare, `passkeyenlist` chassis |
| IP | `185.53.179.146` | Team Internet AG, `passkeysignin` chassis |
| IP | `45.38.20.228` | `passkey-testlol[.]com` |
| IP | `34.42.100.71` | Google Cloud, `.link`/`.info` cluster |

### MITRE ATT&CK v19 Mapping

| **Tactic** | **Technique** | **Evidence** |
| --- | --- | --- |
| Resource Development | T1583.001 - Acquire Infrastructure: Domains | 1,177 passkey-themed domains across 33 registrars |
| Resource Development | T1583.004 - Acquire Infrastructure: Server | Operator-controlled PHP panel behind the phishing pages |
| Resource Development | T1608.005 - Stage Capabilities: Link Target | Per-victim `company.chassis.tld` subdomains staged per target |
| Initial Access | T1566.004 - Phishing: Spearphishing Voice | Vishing calls impersonating internal IT |
| Initial Access | T1656 - Impersonation | Operator poses as helpdesk; pages mirror victim branding |
| Credential Access | T1621 - Multi-Factor Authentication Request Generation | Panel drives TOTP / number-matched push / SMS OTP in real time |
| Credential Access | T1111 - Multi-Factor Authentication Interception | Real-time operator relay of MFA responses during the session |
| Persistence | T1098.005 - Account Manipulation: Device Registration | Attacker-controlled passkey enrolled on victim Entra account |
| Impact | T1657 - Financial Theft | Data-extortion DLS, live since 5/31/2026 |

Thanks for reading — and if you take one thing from this, let it be the DNS lesson rather than the domain list. The domains will have rotated by the time you read this.

Sources: [Okta Threat Intelligence](https://www.okta.com/blog/threat-intelligence/vishing-actors-target-microsoft-entra-passkey-enrollment-/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/entra-passkey-enrollment-vishing-targets-microsoft-365-users/) · [The Hacker News](https://thehackernews.com/2026/07/hackers-use-fake-microsoft-entra.html) · [Palo Alto Networks — Configure DNS Sinkhole](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClGECA0)
