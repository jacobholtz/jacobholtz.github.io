---
title: "Deobfuscating a JavaScript-based Remcos loader"
tags: [remcos, javascript]
---

Sample retrieved 5/12/2026 at 7:28PM CST from [MalwareBazaar](https://bazaar.abuse.ch/sample/89bfece0fa4499eb58fe0e112ef212e32fab31f1d14432eba8eb30dce89d1aba/)

Full disclosure: I used Claude to help with deobfuscation and explaining concepts I was not familiar with. 

>Remcos is a commercially sold Windows remote access tool (RAT) marketed as legitimate remote-administration software but widely abused by threat actors for malicious remote control, keystroke/credential harvesting, and surveillance. It's commonly delivered via phishing (often as an obfuscated script or macro-laden document), and once installed it typically establishes persistence and beacons out to a C2 server over a custom protocol.


### Deobfuscation and Static Analysis
Upon unzipping the file archive and opening the JavaScript payload in a text editor, we are greeted with what appears to be many lines of gibberish text:

![Pasted image 20260512220530](/assets/images/deobfuscating-a-javascript-based-remcos-loader/01.png)

This is what a full line looks like:

```
this.FHOTDMJCRUDYVZRBEEQCCPVSJ += "⸟ᤎ⩕ɟ⪥FHOTDMJCRUDYVZRBEEQCCPVSJᗳƝߑ૤ⷉFHOTDMJCRUDYVZRBEEQCCPVSJᤎ⩕ɟ⪥FHOTDMJCRUDYVZRBEEQCCPVSJ⸟ᤎ⩕ɟ⪥↾ၑ⡳ଃᗳƝߑ૤ⷉᗳƝߑ૤ⷉᅭቔᒱಁ࡞ᬏ⊥শ໠ťᙼົᦻᴦ၈ൟ⵸बࣻ෿ᤤ↊ש🗚➏ŧ⌋【Ꮻ઒仜亚乒为人丙七两付丟了七丌丬丧些价乷仐仮仈丙仛予亟严乬万丠不久丐仾乃事亀亰亷丫亐丒亽乨亦习丘亡丏仳三丨乒仅亲京井亠乮亵乾丯丩份上东举仭乥亙串件三丘七乿丘乄亹与亳亨ᗳƝߑ૤ⷉᗳƝߑ૤ⷉ仦乥且仼乕亩三乘亂乖仌仺仐仙买仪乣什丂亢么丵仃乯丟乔乎亓丗之事亻什仾仇主亶仃丂亀亙丰丳乯临丮乴仹丞云享乪从亣丒乨丱丘上仮乸仓了亡乭亴乁与亚丽任价乏久亊乡义之亖丒乗亿丛亀亗仛仲仟京亇乞丸乚仾丈九仮乏仝乾乆亀亝举业仍丑们丼仲丛仁丫仡亩FHOTDMJCRUDYVZRBEEQCCPVSJ事丶价乔事亼争乺丨丮亭仝从仫享丫仅仰代丼丢仞亾丽乚亪亚亻仔亦份丂亰並亅丝仪亠亄乗乒习乧仍亭件仼主买亼么乊亦仗丵亂乽令両以亴二丹仈份丁亱亡丕与亊丿丹也仁仍亹乜乘仭亍代云仗亏了丼仭丌丫亦仺乒亄专乁丿主丂仦一丣乲仓义亖乍亠世丠亊人付乽乸仢亏互仢亸九交付亘乽亿仉丕丵亱亣乣亮了了亝亁仹亣乾丂丕乫乇乜仍丵仄亀丿交价亨丽交乩乨仙亱仐丣仿乏亝主亲仒仮且仆乄仑亍亅丮乮亊乂中亟东亝与付亁书他両丄乍丽仛交亄仓乸亢从严仡丮三仚京亍不任书乪丹亂乧乤乣亳丸也乶仨丢丸丂乼ᗳƝߑ૤ⷉᗳƝߑ૤ⷉ令亳仨乒亚仝仿両丸丌之丕三亿仞乯亿丗仩乹亚严亱仔乞FHOTDMJCRUDYVZRBEEQCCPVSJ万仐业仒丘乧乎仼仧乷仾亩仢二丱义乡亄乑乔介乙亐他以亶丟丷亏乎乎乹仱仌乵丑乯亠乹丰丑亏仏仭们义不五丫仟乖乶亅仼丟份仜丧丳予亖了乑乍乸亟丯以仝仌乚乕亙什业FHOTDMJCRUDYVZRBEEQCCPVSJ交仉件仿亅乌乵亾乪丬丄仠丙乩他亞丝丘仿仍丮仡亶乾乒东两乐亱仑争丢仾亨仅乨业乹仒乨乺丐仕亂仢仓丘什乎不仆乵乒丙乼乚丵亐么亡临亢五丰丛万云亂仄仁东什丩三乨今仛乗也仪亦仠么丱乖亂丛仢亄仉丂亶丁业仇举上亲仨乎丒乱仇仦亢二仪丼亾乵乃並举仙仗乶乛任乥丣亼仔仭亜仰亂份仂乖亓乱乏丘仝亹仏乪久上三乇仁丩乂于亿丱乐世乹仂仗么仵丩仩业亊交丛七乏乿专乮乨亿乙付亦仫乶丕亊仧亰以乩介些买丳乘仿了件丫亵亓争丬丘乴仨仱丹丯为丨仜亣仠亖亚乜今丙乯乾世乵亨介亢亻亁些丷亊亴仃业主丏仚严丼仠仨仲亜仮亴亀什仧亘产为仈乄一义仉专买了任亷丸之井亾为以乴仰们ᗳƝߑ૤ⷉᗳƝߑ૤ⷉ以亴仺享亴亞予亐乒亨争仲习乯事丕仏于义买丯不仭亸亍乶亠亂仮丷亢乜乻丼上万么且仟仼仉丩仒中亲丯习仗仌仇丷乕专乤亵乖万乏仉亗丶仍仪以丑仫仚乸丘仸仕丞个仔亵东云亁中亜丯举乡任丬仛付乁丮亻仛乴仗从乎丁乊乹京专丛亯丅仂仒于仔仿亅仇仐亴久亡亄乵仆乬仭亮亷之丰乨下丠仨乫乘亜仮乯亻乏仉亁丣乀亟丵京丱丬ᇠƶủᦻᴦ၈ൟ⵸बࣻ෿ᤤ↊ש🗚⌖❟ߩ⭳ᨔઆዃੀĎ⋆ସ⭴ſໝ·ⲳ⒔ᦝṪ౤ᤦFHOTDMJCRUDYVZRBEEQCCPVSJ઴Ꮽ᪬஄ᕨ⒨ඌℴ۔⸛ᛞաᱰఞ෈ِځᑓƺཱུෞڥ❉⋈ೂ཈ᇷ🗎ή⫺ᴃᬀӁⲥ᭰⪚໣ߝᗳƝߑ૤ⷉᗳƝߑ૤ⷉή⑈ᕆਤ⌱዆̿ᎍᒺ⣔῰Ѭ⫿๩⢘FHOTDMJCRUDYVZRBEEQCCPVSJᗳƝߑ૤ⷉFHOTDMJCRUDYVZRBEEQCCPVSJ᠁ᦒ";	
```

Claude suggested I try CJK byte frequency analysis and XOR/AES-CBC decryption to extract potential plain-text code. Before long, however, I noticed that line 48 contained an additional ~4.2 MB of text:

![Pasted image 20260512222901](/assets/images/deobfuscating-a-javascript-based-remcos-loader/02.png)

After extracting the additional text to its own file, passing it through `webcrack` (a public JavaScript deobfuscator and unpacker) twice, and cleaning up a bit of dead code, we are left with more junk:

![Pasted image 20260515125610](/assets/images/deobfuscating-a-javascript-based-remcos-loader/03.png)

![Pasted image 20260515125634](/assets/images/deobfuscating-a-javascript-based-remcos-loader/04.png)

![Pasted image 20260515125843](/assets/images/deobfuscating-a-javascript-based-remcos-loader/05.png)

After some more deobfuscation, we finally have human-readable text:
![Pasted image 20260515151713](/assets/images/deobfuscating-a-javascript-based-remcos-loader/06.png)

In short, the script checks if the `FHOTDMJCRUDYVZRBEEQCCPVSJ` file already exists, creating it if not. If the `LOUUU...` variable at the top is set to `YESSSSSSSS`, a scheduled task executing `FHOTDMJCRUDYVZRBEEQCCPVSJ` every 15 minutes is created. In this case, however, that functionality is not reached. Furthermore, the `makeid` function accepts an integer and generates a random string consisting of the number of characters specified in the passed integer. For example, if `makeid(15)` is called, the output string could be `mUalbIWhxyyjSpk`.

Next, three XML ActiveX objects are created to write base64-decoded content to a file with no extension, an EXE, and a TTF:
![Pasted image 20260517204124](/assets/images/deobfuscating-a-javascript-based-remcos-loader/07.png)

The EXE appears to be AutoIt3, a legitimate automation utility frequently abused by threat actors to execute malicious code:
![Pasted image 20260517205009](/assets/images/deobfuscating-a-javascript-based-remcos-loader/08.png)

VirusTotal also recognizes this payload as AutoIt3:
![Pasted image 20260517205048](/assets/images/deobfuscating-a-javascript-based-remcos-loader/09.png)
![Pasted image 20260517205101](/assets/images/deobfuscating-a-javascript-based-remcos-loader/10.png)

It is unclear why Scriptrunner.exe is included given I could not find anything calling the assigned variable, but I speculate it's a red herring meant to throw analysts off or a left-over artifact from development. The final two lines create a `WScript.Shell` object and calls the dropped EXE against the TTF.
![Pasted image 20260613112922](/assets/images/deobfuscating-a-javascript-based-remcos-loader/11.png)

Deobfuscating the TTF file reveals it's an AutoIt3 script, consistent with our prior discovery of the AutoIt3 executable. Here's what the script looks like before/after deobfuscation and cleanup:

![Pasted image 20260518203057](/assets/images/deobfuscating-a-javascript-based-remcos-loader/12.png)

![Pasted image 20260518204340](/assets/images/deobfuscating-a-javascript-based-remcos-loader/13.png)

Much better. In short, the eight-line function at the top of the obfuscated script performs in-place XOR string decryption using a hardcoded key (binary value of 99), so it was trivial to decrypt strings using this function. This technique effectively bypasses security tooling and analysts performing static string and keyword analysis by searching for phrases like "kernel32.dll", "NtAllocateVirtualMemory", "NtCreateThreadEx", etc. in files. Next, let's look at lines 1-12 in the deobfuscated code:

![Pasted image 20260518204925](/assets/images/deobfuscating-a-javascript-based-remcos-loader/14.png)

Line one is the standard input parameter to the `CreateProcessA`API call, controlling how the spawned process window appears. The shortened field names (`r1`, `r2`, `x1`, `fl`, `sw`, etc.) are legitimate Windows SDK names for `lpReserved`, `lpDesktop`, `dwX`, `dwY`, `dwFlags`, and `wShowWindow`. This particular byte layout matches the official STARTUPINFOA struct exactly so the API accepts it, albeit in a way intended to confuse analysis and prevent static keyword matching.

Similarly, line two allocates the PROCESS_INFORMATION output struct. This struct is populated with process handle (`ph`), thread handle (`th`), process ID (`pid`), and thread ID (`tid`). The script later reads `ph` on line seven to obtain the handle it will inject into.

Lines three through five configure the STARTUPINFO struct for hidden execution. In this case, `cb` is set to the struct's own size, a required component that validates the struct version and rejects malformed inputs. `fl` (dwFlags) is set to `1` = `STARTF_USESHOWWINDOW`, indicating to use the following `sw` field. `sw` (wShowWindow) is set to `0` = `SW_HIDE`. Combined with the flag above, this ensures the spawned process window is never visible to the end user or security researchers.

Line six is wrapped in a boolean condition check, exiting if the `DllCall` function fails. On this line, the `CreateProcessA` API function is called and passed the following parameters:
- `lpApplicationName` = `0` (NULL, no application name)
- `lpCommandLine` = `"C:\Windows\Syswow64\colorcpl.exe"` (the 32-bit Color Control Panel binary as the injection target)
- `lpProcessAttributes`, `lpThreadAttributes` = `0`
- `bInheritHandles` = `0` (FALSE, do not inherit handles)
- `dwCreationFlags` = `0x08000000` = `CREATE_NO_WINDOW` (suppresses console window creation as a second stealth layer on top of `SW_HIDE`)
- `lpEnvironment`, `lpCurrentDirectory` = `0`
- `lpStartupInfo` = pointer to the STARTUPINFO configured above
- `lpProcessInformation` = pointer to the PROCESS_INFORMATION struct above

If `CreateProcessA` fails, the script terminates execution instead of attempting payload injection into a non-existing process.

Line seven, as I mentioned earlier, reads the `ph` (hProcess) field from the PROCESS_INFORMATION struct. Now that the `CreateProcessA` call populated the struct, the script is able to perform actions on the colorcpl.exe process handle.

Line eight closes the thread handle since only the process thread is needed for injection. Later, the script will create its own thread with a `NtCreateThreadEx` call pointing at the injected payload.

Lines nine through twelve open the previously dropped `FHOTDMJCRUDYVZRBEEQCCPVSJ` payload, reads the byte count of its contents, and closes the opened file object. An additional check ensures contents actually exist, exiting if not.

The rest of the script (lines 14-35) stages a `DllStruct`  with enough space to XOR-decrypt `FHOTDMJCRUDYVZRBEEQCCPVSJ`  in-place with a key of `0x381EFC`. Interestingly, encrypted bytes are effectively XOR-decrypted using a key of `0xFC` since the `DllStructSetData` call will truncate any XOR output to a single byte since only one byte is iterated over at a time. 

<img src="/assets/images/deobfuscating-a-javascript-based-remcos-loader/15.png" alt="Pasted image 20260529194218" width="697">

### Dynamic Analysis
At this point, I hit a wall. I successfully XOR-decrypted the payload and determined an encrypted Donut v1.0 loader was in play, however I could not extract a clean executable or shellcode. After taking a fresh snapshot, I fire up `x32dgb.exe` (a 32-bit Windows binary debugger)  to start dynamic analysis. Unfortunately, I did not take screenshots during analysis, but with Claude's help I was able to extract the suspected Remcos payload by attaching `x32dbg.exe` to the payload-injected `colorcpl.exe` process. After running a Python clean-up script (also from Claude), we're left with a stripped-down version of Remcos.

While I was not able to extract C2 information from the final payload, [AnyRun](https://any.run/report/d5ccc2fde274432d70b52bb6373a693d505911595e0999e7d3c0c88ec2656923/71b8826e-0086-4c96-a499-123c36872540) was able to extract it. In the following screenshot, we see Remcos is instructed to connect to 103.83[.]87.8 over port 1515 through colorcpl.exe, a standard Windows utility invoked to calibrate display color profiles that does not normally generate outbound internet traffic, let alone to public IP addresses. This behavior is among the highest-fidelity indicators of Remcos infection and should be prioritized in threat hunting queries.

![Pasted image 20260607201319](/assets/images/deobfuscating-a-javascript-based-remcos-loader/16.png)

Additionally, `Install_HKCU\Run`, `Install_HKLM\Run`, and `Install_HKLM\Explorer\Run` are set to `True`, indicating persistence is achieved by manipulating the corresponding registry `Run` keys to start Remcos on system startup or user logon. This tactic is textbook [T1547.001](https://attack.mitre.org/techniques/T1547/001/); these specific keys are often abused by threat actors so malware survives reboots and executes on boot. Despite being enabled in the configuration, I was not able to identify matching registry key modification events in AnyRun. One potential reason why changes to the registry were not observed could be anti-sandbox checks overriding this behavior even though it's enabled in the malware's settings. 

Remcos is also known to harvest credentials and keystrokes. This behavior was directly observed via file creation and write events from colorcpl.exe after executing the Remcos payload: 
![Pasted image 20260614150520](/assets/images/deobfuscating-a-javascript-based-remcos-loader/17.png)

![Pasted image 20260614165921](/assets/images/deobfuscating-a-javascript-based-remcos-loader/18.png)

Investigating the single IP address in Censys reveals a number of interesting findings: 1), port 1515 is still open and listening for Remcos connections, 2), the default remote desktop protocol (RDP) port 3389 appears to be in use and exposed to the internet, 3), the WHOIS organization address points to Wyoming in the US despite IP geolocation resolving to Istanbul, Turkey, and 4), a single forward DNS entry containing newsletter[.]moreiraclear[.]com can be observed. 

![Pasted image 20260531204504](/assets/images/deobfuscating-a-javascript-based-remcos-loader/19.png)

![Pasted image 20260607200948](/assets/images/deobfuscating-a-javascript-based-remcos-loader/20.png)

A quick search led me to White Label Services, LLC, a hosting provider that adopts a white label approach characterized by offering a service or product to be rebranded by another company. In this case, White Label Services' infrastructure is leased to third parties, including VPNs, web proxies, or other hosting providers. This type of service, while typically legitimate, is frequently abused by cybercrime syndicates to redirect blame and avoid suspicion. White-label hosting providers in areas with lax cybercrime laws (like Turkey) often do not respond to takedown requests, implement no or loosely-defined know-your-customer (KYC) policies, accept anonymous cryptocurrency payments, and implement multiple layers of upstream IP routing. These compounding factors greatly limit law enforcement's ability to interrupt malicious campaigns using these services for infrastructure, so much so they are described as "bulletproof hosters" among underground rings and the intelligence community alike.  

![Pasted image 20260531210750](/assets/images/deobfuscating-a-javascript-based-remcos-loader/21.png)

This specific IP address has substantial history of abuse. The first reported case of abuse occurred in March 2025 with significant activity ramping up in February 2026, according to [AbuseIPDB](https://www.abuseipdb.com/check/103.83.87.8?page=2):

![Pasted image 20260531211128](/assets/images/deobfuscating-a-javascript-based-remcos-loader/22.png)

Uploading to [Malware Bazaar](https://bazaar.abuse.ch/sample/f95d799399a156215867e534d0b600a3851b255d697c54e5ad4bcc47a41ac842/) and [VirusTotal](https://www.virustotal.com/gui/file/f95d799399a156215867e534d0b600a3851b255d697c54e5ad4bcc47a41ac842/detection) confirms it's a Remcos payload, further validating my findings.
![Pasted image 20260531173048](/assets/images/deobfuscating-a-javascript-based-remcos-loader/23.png)

![Pasted image 20260531173337](/assets/images/deobfuscating-a-javascript-based-remcos-loader/24.png)

Thanks for reading!
### IOCS

| Type   | Value                                                            | Note                                       |
| ------ | ---------------------------------------------------------------- | ------------------------------------------ |
| SHA256 | 89bfece0fa4499eb58fe0e112ef212e32fab31f1d14432eba8eb30dce89d1aba | Original sample from MalwareBazaar         |
| SHA256 | F95D799399A156215867E534D0B600A3851B255D697C54E5AD4BCC47A41AC842 | Remcos payload extracted from colorcpl.exe |
| IP     | 103.83[.]87.8:1515                                               | Remcos C2 |                                 | Domain | newsletter[.]moreiraclear[.]com				    | Shared infrastructure artifact

### MITRE ATT&CK v19 Mapping

| **Tactic**          | **Technique**                                                                     | **Evidence**                                                      |
| ------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Execution           | T1024.002 - User Execution: Malicious File                                         | Initial JavaScript payload executed by user for initial infection |
| Execution           | T1059.007 - Command and Scripting Interpreter: JavaScript                         | Multiple JavaScript payloads                                      |
| Stealth             | T1027.009 - Obfuscated Files or Information: Embedded Payloads                    | XOR-encrypted Remcos payloads embedded in files                   |
| Stealth             | T1027.010 - Obfuscated Files or Information: Command Obfuscation                  | Obfuscated AutoIt3 script and process calls                       |
| Stealth             | T1027.013 - Obfuscated Files or Information: Encrypted/Encoded File               | Multiple layers of encoded JavaScript and PE payloads             |
| Stealth             | T1055 - Process Injection                      | Remcos payload injected into colorcpl.exe                         |
| Persistence         | T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Registry Run key targeted for Remcos persistence on boot          |
| Command and Control | T1571 - Non-standard Port                                                         | Remcos communicates with remote C2 via TCP port 1515              |
