# snapshot — madeye/sssniff README — excerpt ("How it works?")
# source: https://raw.githubusercontent.com/madeye/sssniff/master/README.md
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# repo: https://github.com/madeye/sssniff
# excerpt: title + the detection method paragraph

ss(r)Sniff

### How it works?

It computes entropy of the first 32 packet lengths of each TCP connection. When the entropy is larger than a threshold, the
connection is detected as a SSR connection.

### Why it works?

The traffic of SS(R) looks randomized with a relative high entropy of the first 2 to 3 packets. As a result, SS(R) can be detected by computing the entropy of these packets. The drawback is this approach shows high false positive rate and is very expensive.
