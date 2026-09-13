# snapshot — Hysteria 2 docs — "Full Server Config", Bandwidth/Brutal excerpt
# source: https://hysteria.network/docs/advanced/Full-Server-Config/
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# site: https://hysteria.network
# excerpt: the sentences about Brutal's loss compensation and when Brutal applies

> Brutal congestion control has a "loss compensation" mechanism: when there is packet loss, it attempts to send slightly faster than the set bandwidth to compensate and still reach the target speed. This may or may not help depending on the network conditions, and can sometimes make things worse. Set this to true to disable the compensation and always send at exactly the set speed.

> Brutal: This is Hysteria's custom congestion control algorithm. Unlike BBR, Brutal operates on a fixed rate model and does not reduce its speed in response to packet loss or RTT changes. If it fails to meet the predetermined target rate, the algorithm calculates the rate of packet loss and compensates by increasing speed. This only works if you know (and accurately specify) the theoretical maximum speed of your current connection. It's particularly effective at seizing bandwidth in congested, best-effort delivery networks, hence its name.

> From the client's point of view, if the user doesn't provide a bandwidth value for download (but provides one for upload), the Hysteria server will send data to the client using its configured non-Brutal controller, while the client will upload data to the server using Brutal, and vice versa. The client can provide both, so both directions will use Brutal, or neither, so both directions will use the configured non-Brutal controller (default: BBR).

> The server's bandwidth limit only applies to Brutal at the moment. It has no effect on BBR or Reno.
