# snapshot — Xray-core docs — REALITY transport (`password`, unauthenticated traffic) excerpt
# source: https://xtls.github.io/config/transports/reality.html
# fetched:2026-09-14
# note: point-in-time capture committed so claims.json can check the quote offline; the gate does not re-fetch it, freshness is not checked.
# doc repo: https://github.com/XTLS/Xray-docs-next
# excerpt: the `password` field and the warning about traffic that fails REALITY auth

- `password`: password : string 必填，服务端私钥对应的公钥。使用 ./xray x25519 -i "服务器私钥" 生成。旧称 publicKey, 为防止误解更名

- WARNING 为了伪装的效果考虑，Xray 对于鉴权失败（非合法 REALITY 请求）的流量，会 直接转发 至 target. 如果 target 网站的 IP 地址特殊（如使用了 CloudFlare CDN 的网站） 则相当于你的服务器充当了 CloudFlare 的端口转发，可能造成被扫描后偷跑流量的情况。
