# snapshot — trojan-gfw protocol.md — excerpt ("Other Protocols" + "Active Detection")
# source: https://raw.githubusercontent.com/trojan-gfw/trojan/master/docs/protocol.md
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# repo: https://github.com/trojan-gfw/trojan
# excerpt: the fallback/preset-endpoint sections

## Other Protocols

Because typically a trojan server is to be assumed to be an `HTTPS` server, the listening socket is always a `TLS` socket. After performing `TLS` handshake, if the trojan server decides that the traffic is "other protocols", it opens a tunnel between a preset endpoint (by default it is `127.0.0.1:80`, the local `HTTP` server) to the client so the preset endpoint takes the control of the decrypted `TLS` traffic.

## Anti-detection

### Active Detection

All connection without correct structure and password will be redirected to a preset endpoint, so the trojan server behaves exactly the same as that endpoint (by default `HTTP`) if a suspicious probe connects (or just a fan of you connecting to your blog XD).
