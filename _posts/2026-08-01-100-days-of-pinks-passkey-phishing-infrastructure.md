---
title: "100 days of Pink's passkey phishing infrastructure"
tags: [pink, phishing, passkeys]
---

Since late April, a continuous wave of domains containing the string `passkey` has been registered for one specific phishing campaign built around passkey enrollment. At the time of writing, I identified a total of **1,177 domains** across **247 target organizations**, **33 registrars**, and **55 distinct phishing-kit chassis**.

The timing is worth noting, though not in the direction you might assume. On [July 13th](https://www.microsoft.com/en-us/security/blog/2026/07/13/microsoft-entra-id-security-updates-passkeys-are-the-default-authentication-method-in-entra-id/), Microsoft announced that passkeys become the default authentication method in Entra ID on **September 1st, 2026**, with users enabled for SMS or voice auto-enrolled and nudged to register a passkey at their next MFA sign-in. This campaign's first domains were registered on April 20th — roughly twelve weeks *before* that announcement, so it wasn't started in response to it. What the September change does is far more useful to the actor: it makes an unprompted "you need to register a passkey" message the expected experience for millions of enterprise users, and it does so right as this infrastructure reaches maturity.

### The actor

The cluster is publicly tracked under a few names. [Okta Threat Intelligence](https://www.okta.com/blog/threat-intelligence/vishing-actors-target-microsoft-entra-passkey-enrollment-/) tracks it as **O-UNC-066**; Palo Alto Networks [Unit 42](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-06-03-Pink-Extortion-Brand-Activity.txt) tracks it as **CL-CRI-1147**, and the crew brands itself as **Pink** and **Redact** on two data-leak sites. Evidence suggests a group formerly known as BlackFile rebranded as Pink/Redact due to pressure from ShinyHunters following alleged impersonation during victim negotiations. Reporting ties it to The Com, the same loose network that produced Scattered Spider, ShinyHunters, and LAPSUS$. Their primary motivation is data extortion per their own DLS: "our only goal is profit."

Rather than phishing credentials, Pink/Redact phones an employee, impersonates internal IT, and walks them through **enrolling an attacker-controlled passkey** on their own Microsoft Entra account. Behind the phishing page sits an operator-driven PHP panel with roughly one-second heartbeat polling, so a human operator can steer the victim through whatever MFA the tenant actually enforces in real time, such as TOTP, number-matched push, and SMS OTP.

Passkeys are meant to be phishing-resistant, however if you can talk a user into registering your authenticator, the phishing resistance is now working on the attacker's behalf: they hold a legitimate, unphishable credential on the victim's tenant, and it survives the password reset that would normally end the incident.

### Domain-keyword correlation

Pink registers domains incorporating the word "passkey" and hangs per-victim subdomains off them, which is precisely why the campaign is trackable by domain-string alone. Most base domains are generic passkey-themed lures like `registerpasskey.com`, `startpasskeysetup.com`, or `passkeymigration.com`. The targeted organization itself is carried in the subdomain:

```
homedepot.registerpasskey.com
staples.passkeyenlist.com
deshaw.createssopasskey.com
```

These base domains are reused across many victims. The most-reused chassis in my dataset:

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

### Targeted industries and geographic victimology

A few chassis can be grouped in entirely distinct industry verticals. For example, `passkeymigration.com` is almost entirely crypto and payments, and `createssopasskey.com`, which showed up on 7/28, is entirely asset management and finance. Overall, sector distribution spread across the 247 identified organizations totals 14:

![Sector distribution across the 247 targeted organizations](/assets/images/100-days-of-pinks-passkey-phishing-infrastructure/01.png)

Nearly a quarter of all targeted organizations operate in financial services, further reinforcing Pink/Redact's financial motivation.

The overwhelming majority of targeted organizations are based in the United States — 232 of the 244 I could place, or 95%. The remaining twelve sit in Canada (Brookfield, Clio, TMX Group, WestJet), the UK (Copper, easyJet), Finland (Kone), Switzerland (MSC), Germany (Qiagen), France (Questel), Israel (Global-e), and Australia (Swyftx). The map below shows the US distribution only, where California (49), Illinois and New York (19 each), and Texas (18) lead:

![US distribution of targeted organization headquarters](/assets/images/100-days-of-pinks-passkey-phishing-infrastructure/02.png)

Starting from April 20th, the registered domains gradually rose until the placeholder domains roughly doubled in July. This is indicative of the actor preparing for future abuse, although the number of targeted domains up until now does not appear to reflect that.

![Cumulative domain registrations, 2026-04-20 to 2026-08-01](/assets/images/100-days-of-pinks-passkey-phishing-infrastructure/03.png)

Registrar concentration heavily focuses on three: GMO/Onamae.com (367), NICENIC (355), and Tucows (200) account for the large majority. These statistics are not entirely surprising; all three are frequently cited as among the most-abused registrars due to their cheap cost, easily automated API-based registration, extensive reseller networks, and lax registration verification challenges. In fact, four of the five registrars with the most phishing domains reported in Interisle Consulting's [2025 study](https://domainnamewire.com/wp-content/Interisle_Phishing-Landscape-2025.pdf) appear among the registrars identified during analysis — NICENIC (#1), NameSilo (#2), NameCheap (#4), and Key-Systems (#5); only Dominet (HK) at #3 is absent. The same study ranks GMO/Onamae first for bulk registrations, with a single set of 17,591 domains registered inside ten hours.

![Registrar distribution](/assets/images/100-days-of-pinks-passkey-phishing-infrastructure/04.png)

### Infrastructure analysis

Across the full 1,177-domain corpus, 564 still resolve to at least one IP address:

| Endpoint | Domains | Provider |
| --- | --- | --- |
| `13.248.169.48`, `76.223.54.146` | 387 | AWS Global Accelerator |
| `198.185.159.144/145`, `198.49.23.144/145` | 16 | Squarespace |
| `104.21.17.206`, `172.67.178.76` | 12 | Cloudflare (`passkeyenlist.com` chassis) |
| `185.53.179.128` | 9 | Team Internet AG (`passkeysignin.com` chassis) |
| `34.42.100.71` | 8 | Google Cloud (`.link`/`.info` cluster) |
| `45.138.216.23` | 8 | MachCloud B.V. |

One caveat on that first row: AWS Global Accelerator IPs are shared anycast space, meaning many unrelated AWS customers resolve into those same ranges. Co-residence there is not by itself evidence that a domain belongs to this campaign. Those 387 are campaign domains because they matched on registration date and naming convention, not because of where they're hosted.

The other 613 domains are not simply parked. **386 of them — a third of the entire corpus, spanning 59 base domains — have been suspended by their own registrars**, carrying a `clientHold` status at the registry that removes the domain from the zone entirely. NICENIC accounts for 45 of those 59 suspended bases and Tucows another 9, which is notable given NICENIC is the campaign's second-largest registrar by volume. This is a continuous drip rather than a single sweep: RDAP last-changed dates run from April through today, and the most recent suspensions are days old. `createssopasskey.com`, the asset-management chassis first seen on 7/28, was suspended on 8/1 — a four-day operational lifespan that took all nine of its named subdomains offline with it.

Worth stressing how that was measured: suspension status comes from registry RDAP and whois, not from DNS resolution. A domain that fails to resolve tells you nothing on its own about *why*, and resolver-level answers can reflect filtering local to wherever you happen to be querying from rather than anything true of the domain globally.

### Detection notes

Domain-string tracking works unusually well here, but the real detection opportunity is on the identity side, because the domains are cheap and the enrollment event isn't:

- **Alert on passkey/FIDO2 credential registration as a high-severity identity event**, not an informational one. Focus on a registration from a new device, a new ASN, or within a short window of a helpdesk contact. This is the single control that would break the campaign.
- **Watch for enrollment following a support interaction.** The vishing call is the initial access vector; correlating helpdesk tickets against credential-registration events catches what neither signal catches alone.
- **Constrain enrollment itself**. Require registration from a managed device or an existing strong credential, rather than allowing bootstrap from a session an operator can drive.
- **Hunt DNS for the pattern**, i.e. `*.passkey*` and `passkey*` resolutions from user subnets. Reputation blocking will not save you here; 82% of these domains have zero VT detections.
- **Expect a spike around September 1st.** Once Entra begins auto-enrolling SMS and voice users into passkeys, "register your passkey" stops being a suspicious out-of-band request and starts being a message users are told to expect. Brief helpdesks and users before the change lands, not after.

### IOCs

A representative sample. The corpus stands at 1,177 domains, with new registrations still appearing through the end of July and roughly a third of the total already suspended at the registrar, so treat the naming pattern as the durable indicator rather than the list.

| Type | Value | Note |
| ------ | ------ | ------ |
| Domain | `passkeyenlist[.]com` | Live Cloudflare chassis, 9 targeted orgs |
| Domain | `passkeysignin[.]com` | Live, Team Internet AG, 8 subdomains |
| Domain | `createssopasskey[.]com` | Asset-management targeting, 9 orgs — **registrar-suspended 8/1** |
| Domain | `passkey-testlol[.]com` | Registered 7/30, `m365.` subdomain |
| Domain | `myssopasskey[.]com` | Registered 7/31 16:42 UTC, NICENIC, no DNS yet |
| Domain | `newuser-passkey[.]com` | Highest VT detection in corpus (19/91) |
| IP | `13.248.169.48`, `76.223.54.146` | AWS Global Accelerator — **shared anycast, low-fidelity** |
| IP | `104.21.17.206`, `172.67.178.76` | Cloudflare, `passkeyenlist` chassis |
| IP | `185.53.179.128` | Team Internet AG, `passkeysignin` chassis |
| IP | `45.38.20.228` | `passkey-testlol[.]com` |
| IP | `34.42.100.71` | Google Cloud, `.link`/`.info` cluster |

### MITRE ATT&CK v19 Mapping

| **Tactic**           | **Technique**                                          | **Evidence**                                                   |
| -------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| Resource Development | T1583.001 - Acquire Infrastructure: Domains            | 1,177 passkey-themed domains across 33 registrars              |
| Resource Development | T1583.004 - Acquire Infrastructure: Server             | Operator-controlled PHP panel behind the phishing pages        |
| Resource Development | T1608.005 - Stage Capabilities: Link Target            | Per-victim `company.chassis.tld` subdomains staged per target  |
| Initial Access       | T1566.004 - Phishing: Spearphishing Voice              | Vishing calls impersonating internal IT                        |
| Initial Access       | T1656 - Impersonation                                  | Operator poses as helpdesk; pages mirror victim branding       |
| Credential Access    | T1621 - Multi-Factor Authentication Request Generation | Panel drives TOTP / number-matched push / SMS OTP in real time |
| Credential Access    | T1111 - Multi-Factor Authentication Interception       | Real-time operator relay of MFA responses during the session   |
| Persistence          | T1098.005 - Account Manipulation: Device Registration  | Attacker-controlled passkey enrolled on victim Entra account   |
| Impact               | T1657 - Financial Theft                                | Data-extortion DLS                                             |

Thanks for reading!
