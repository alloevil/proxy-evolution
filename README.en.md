# Proxy Protocols: Six Generations of Evolution

[English](./README.en.md) | **简体中文**

> From Shadowsocks to XHTTP: six generations of anti-censorship protocols, turned into a page you can play with.

**[▶ Live Demo](https://alloevil.github.io/proxy-evolution/)** · Single file · Zero dependencies · No build step

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Six generations of anti-censorship protocols: packets on a rail past the censor node — Shadowsocks (2012), SSR / VMess (2015–2019), VLESS / Trojan (2018–2020), Hysteria2 / TUIC (2022–2023), REALITY / AnyTLS (2023–) and XHTTP + post-quantum REALITY (2024–)">
</p>

![Main view: 6th generation XHTTP, packets flowing past the censor node](./screenshot-main.png)

<details>
<summary>▲ Main view: packets travel past the "censor node" at each protocol's real speed</summary>

Clicking "Launch Probe" triggers the **probe theater** — in the 6th generation, unauthenticated requests are handed to the CDN edge; the censor gets the CDN's real certificate and cached content, and never even sees the origin server:

![Probe theater: 6th-gen requests treated as ordinary visitors by the CDN](./screenshot-probe.png)

</details>

---

## What is this

One page that makes clear why first-generation proxies get identified — and how sixth-generation ones leave an active probe looking at "a normal website that isn't even your server."

The abstract protocol arms race is made concrete in three ways:

| Concrete visual | Real mechanism behind it |
|---|---|
| **Packets flowing along a track** | True speed differences between generations; retransmits and head-of-line blocking under packet loss |
| **A censor node wedged in the middle of the link** | Passive identification (statistical classification) + active probing (connecting directly as a fake client) |
| **Probe packets flying at the server** | What the censor gets back — which decides a protocol's fate |

## Six generations

```
Gen 1  Shadowsocks (2012)             Replace plaintext SOCKS5 forwarding with symmetric encryption (no protocol imitation)
  ↓
Gen 2  SSR / VMess (2015)             Add obfuscation and replay protection
  ↓
Gen 3  VLESS (2020) / Trojan (2018)   Hand encryption to outer TLS; Trojan falls back to a preset site (usually a real HTTPS one)
  ↓
Gen 4  Hysteria2 / TUIC (2022–2023)        QUIC-based; crushes TCP stacks on weak/high-latency links
  ↓
Gen 5  REALITY (2023) / AnyTLS (2025)        Borrow a real site's TLS identity to defeat active probing
  ↓
Gen 6  XHTTP + post-quantum REALITY   Split into plain HTTP requests hidden in CDN traffic;
       (2024)                          post-quantum key exchange + ECH
```

## Interactive features

### Live traffic animation
Packets continuously stream past the "censor node." **Speed is evidence**: SS 80px/s, QUIC 95px/s; under packet loss TCP stacks halve and show `⚠ retransmit` markers, while QUIC actually speeds up — Brutal congestion control refuses to back off. Flip the "weak network" switch and the difference is visible to the naked eye.

### Active probe experiment
Click "Launch Probe" to watch what a censor gets by connecting directly to the server as a fake client. Three verdicts:

- 🔴 **Identifiable** — returns meaningless encrypted garbage, no website structure
- 🟡 **Partially exposed** — real TLS, but certificate/fingerprint can be cross-checked
- 🟢 **Indistinguishable** — what the censor sees *is* a real website

Generation 5 has its own theater: the probe packet is forwarded to the real-website node and returns "real website certificate." That is exactly how it resists probing.

### Six-generation sweep
One click probes all six in sequence, stringing the six verdicts into a single evolutionary line — you can see how "resistance to active probing" was achieved, step by step.

### Censorship scenario scripts
Four canned attack sequences that auto-play while narrating in real time:

| Scenario | Plot | Ending |
|---|---|---|
| Active probe attack | Censor connects to each generation, comparing certificates and content | Gen 1–4 🔴/🟡; REALITY and XHTTP 🟢 |
| Deep packet inspection | Classifier scans packet-length entropy / timing / TLS fingerprints (JA3/JA4, only where a ClientHello exists) | SS/SSR 🔴; real TLS + ECH/CDN makes the detection target vanish |
| UDP blockade | udp/443 throttled to 50kbps | Hysteria2 is throttled → the client switches to a REALITY/XHTTP (TCP) node and recovers (a client-side fallback, not an automatic protocol downgrade) |
| Weak long-haul link | RTT 300ms + 8% packet loss | TCP stacks collapse; QUIC barely affected |

### Protocol stack panel
Marks **where encryption happens** in each generation — instantly showing Gen 3 moving encryption up into TLS, Gen 5 having a real website vouch for its identity, and Gen 6 hiding that identity inside a CDN.

### Comparison panel
Four metrics (peak speed / weak-network performance / probe resistance / realism). Hovering a row brightens it and reveals values; clicking a row header re-sorts all generations by that metric (with FLIP animation).

## Quick start

```bash
# Option 1: just open it
open index.html            # macOS
xdg-open index.html        # Linux
start index.html           # Windows

# Option 2: serve locally
python3 -m http.server 8000
# → http://localhost:8000

# Option 3: deploy to GitHub Pages
# This repo has Pages enabled (Settings → Pages → main branch); pushing deploys automatically
```

## Controls

| Action | How |
|---|---|
| Switch generation | Click a generation card · `←` `→` |
| Pause/resume traffic | `Space` |
| Deep-link sharing | URL hash, e.g. `#reality`, `#xhttp` |
| Auto-play | "▷ Auto-play" — good for demos |

## Technical notes

- **Single file** `index.html`: vanilla JS + CSS, zero dependencies, zero build, works offline
- **Animation engine**: `requestAnimationFrame` plus a watchdog (self-heals within 1s if the rAF loop dies); tick body wrapped in try/catch so a single-frame exception can't kill the loop
- **Visuals**: glassmorphism + mesh gradients + film grain; each generation's accent drives the site-wide CSS variable; generation switches use crossfades; the comparison panel uses FLIP animation (Web Animations API)
- **Data-driven**: all six generations' parameters (speed, loss rate, weak-network multiplier, probe verdicts, scenario steps) live in a single `GENS` / `PRESETS` array, so adding a new protocol is one array entry

## Agent / machine-readable

| Endpoint | Purpose |
|---|---|
| [`data.json`](https://alloevil.github.io/proxy-evolution/data.json) | Full dataset: all six generations (protocol stack layers, badges, explanation points, animation parameters, probe verdicts, comparison scores) plus all four scenario scripts as step-by-step events. Includes `innovationText` / `pointsText` / `probeText` — **HTML-stripped plain-text fields** an LLM can quote directly |
| [`llms.txt`](https://alloevil.github.io/proxy-evolution/llms.txt) | LLM-oriented summary: six-generation evolution, key concepts, parameter comparison table, scenario outcome table |
| `robots.txt` | Explicitly allows GPTBot / ClaudeBot / PerplexityBot / Google-Extended / Bytespider / CCBot |

`data.json` is generated from the `GENS` / `PRESETS` arrays embedded in `index.html` by `build-data.py` — the HTML stays the single source of truth, so the JSON can never drift:

```bash
python3 build-data.py    # regenerate data.json after editing data in index.html
```

## Notes & disclaimer

- Mechanism-level claims (what each protocol actually does) were verified line by line on 2026-09-11 against primary sources: the Shadowsocks specs (sip004 / sip022), the SSR and VMess sources and docs, the Trojan protocol doc, Xray-core (VLESS / REALITY / XHTTP and its release notes), XTLS/REALITY, anytls-go, Hysteria, TUIC and RFC 9000. That pass corrected the REALITY handshake key source (the server's own keypair, not the target site's public key), Trojan's fallback semantics (a preset endpoint, not "the real site"), the attribution of JA3/JA4 (a ClientHello fingerprint, not a certificate check), the granularity of QUIC head-of-line blocking (per stream, not per packet), Brutal's semantics (over-sends slightly past the configured bandwidth, and only when one is configured), AnyTLS's era (2025, not 2023), the VLESS/Trojan/Hysteria2/TUIC years, and the anachronism in the Shadowsocks entry (the 2012 protocol used stream ciphers; AEAD and full replay protection only arrived in 2017 and 2022). It also dropped the "disguised as ordinary encrypted traffic" framing for Shadowsocks: the spec describes plain encrypted forwarding, with no protocol imitation. The 2012 start year is a community record (earliest PyPI release 2013-06, earliest GitHub tag 2015) and is kept as the conventional dating.
- Comparison scores are **relative illustrative values** meant to build intuition, not benchmark data.
- Weak-network behavior follows each protocol's congestion control and transport: TCP (TLS stacks) blocks the whole connection on loss and backs off on retransmit; QUIC (Hysteria2 / TUIC) retransmits per-stream over UDP, and Hysteria2's Brutal congestion control refuses to slow down on loss (it slightly over-sends past the configured bandwidth).
- The four scenario endings are illustrative too, and promise nothing about any protocol's fate under a real censor.
- "Probe resistance" means whether the server, when connected to directly, can return a response identical to a real website.
- This project is for studying and researching technical principles only.

## License

[MIT](./LICENSE)
