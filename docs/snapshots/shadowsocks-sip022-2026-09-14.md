# snapshot — SIP022 "AEAD-2022 Ciphers" — excerpt (docs/doc/sip022.md)
# source: https://raw.githubusercontent.com/shadowsocks/shadowsocks-org/main/docs/doc/sip022.md
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# excerpt: title + Abstract + the replay-protection sentence from the Overview + the salt-
# storage requirement; the rest of the spec is not captured

# SIP022 AEAD-2022 Ciphers

## Abstract

This document defines the 2022 Edition of the Shadowsocks protocol. Improving upon Shadowsocks AEAD (2017), Shadowsocks 2022 addresses well-known issues of the previous editions, drops usage of obsolete cryptography, optimizes for security and performance, and leaves room for future extensions.

## 1. Overview

Compared to [previous editions](https://github.com/shadowsocks/shadowsocks-org/blob/master/whitepaper/whitepaper.md) of the protocol family, Shadowsocks 2022 allows and mandates full replay protection. Each message has its unique type and cannot be used for unintended purposes. The session-based UDP proxying significantly reduces protocol overhead and improves reliability and efficiency. Obsolete cryptographic functions have been replaced by their modern counterparts.

Servers MUST store all incoming salts for 60 seconds. When a new TCP session is established, the first received message is decrypted and its timestamp MUST be checked against system time. If the time difference is within 30 seconds, then the salt is checked against all stored salts. If no repeated salt is discovered, then the salt is added to the pool and the session is successfully established.
