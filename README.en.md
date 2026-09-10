# Proxy Protocols: Six Generations of Evolution

[English](./README.en.md) | **简体中文**

> From Shadowsocks to XHTTP: six generations of anti-censorship protocols, turned into a page you can play with.

**[▶ Live Demo](https://alloevil.github.io/proxy-evolution/)** · Single file · Zero dependencies · No build step

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
Gen 1  Shadowsocks (2012)             Make proxy traffic look like ordinary encrypted traffic
  ↓
Gen 2  SSR / VMess (2015)             Add obfuscation and replay protection
  ↓
Gen 3  VLESS / Trojan (2020)          Hand encryption to outer TLS; Trojan impersonates a real HTTPS site
  ↓
Gen 4  Hysteria2 / TUIC (2021)        QUIC-based; crushes TCP stacks on weak/high-latency links
  ↓
Gen 5  REALITY / AnyTLS (2023)        Borrow a real site's TLS identity to defeat active probing
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
| Deep packet inspection | Classifier scans packet-length distribution / timing / JA3 fingerprints | SS/SSR 🔴; real TLS + ECH/CDN makes the detection target vanish |
| UDP blockade | udp/443 throttled to 50kbps | Hysteria2 drops → falls back to REALITY/XHTTP (TCP) and recovers |
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

## Notes & disclaimer

- Comparison scores are **relative illustrative values** meant to build intuition, not benchmark data.
- Weak-network behavior follows each protocol's congestion control and transport: TCP (TLS stacks) blocks the whole connection on loss and backs off on retransmit; QUIC (Hysteria2 / TUIC) retransmits per-stream over UDP, and Hysteria2's Brutal congestion control refuses to slow down on loss.
- "Probe resistance" means whether the server, when connected to directly, can return a response identical to a real website.
- This project is for studying and researching technical principles only.

## License

[MIT](./LICENSE)
