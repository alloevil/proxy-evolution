#!/usr/bin/env python3
"""从 index.html 的 GENS / PRESETS 数组生成 data.json(单一事实来源:HTML)。
用法: python3 build-data.py   # 覆盖写 data.json,git diff 可见漂移
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

def extract_array(src, name):
    """提取 `const NAME = [ ... ];` 的字面量,交给 node 求值。"""
    m = re.search(rf"const {name} = (\[.*?\n\];)", src, re.S)
    if not m:
        raise SystemExit(f"找不到 const {name}")
    return m.group(1)[:-1]  # 去掉尾部 ;

def strip_html(s):
    """去掉 HTML 标签与 emoji,给 LLM 一份干净纯文本。"""
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[🔴🟡🟢✅⚠️✗→←↑↓·—…]", lambda m: {"→": "->", "←": "<-", "·": "-", "—": "-", "…": "..."}.get(m.group(), ""), s)
    return re.sub(r"\s+", " ", s).strip()

gen_lit = extract_array(HTML, "GENS")
pre_lit = extract_array(HTML, "PRESETS")

# 让 node 求值 JS 字面量(比手写解析器稳,不会因格式变化失效)
node_out = __import__("subprocess").run(
    ["node", "-e", f"console.log(JSON.stringify({{GENS:{gen_lit}, PRESETS:{pre_lit}}}))"],
    capture_output=True, text=True, check=True).stdout
raw = json.loads(node_out)

GENS, PRESETS = raw["GENS"], raw["PRESETS"]

# 给每代补纯文本字段(HTML 字段对 LLM 不友好)
for i, g in enumerate(GENS, 1):
    g["index"] = i
    g["innovationText"] = strip_html(g["innovation"])
    g["encWhereText"] = strip_html(g["encWhere"])
    g["pointsText"] = [strip_html(p) for p in g["points"]]
    g["probeText"] = strip_html(g["probe"]["text"])

data = {
    "$schema-note": "proxy-evolution 数据集。single source of truth 是 index.html 内嵌的 GENS/PRESETS 数组;本文件由 build-data.py 生成,勿手改。",
    "project": {
        "name": "proxy-evolution",
        "title": "翻墙协议六代演进 · 交互图解",
        "titleEn": "Proxy Protocols: Six Generations of Evolution",
        "demo": "https://alloevil.github.io/proxy-evolution/",
        "repo": "https://github.com/alloevil/proxy-evolution",
        "license": "MIT",
        "updated": "2026-09-11",
    },
    "verdictLevels": {
        "risk": "可被识别 —— 审查者能判定这是代理流量",
        "mid": "部分暴露 —— 有真 TLS,但证书/指纹可被比对",
        "safe": "无法区分 —— 审查者看到的就是一个真实网站",
    },
    "metrics": {
        "fast": "峰值速度(0-100,相对示意值)",
        "weak": "弱网表现(0-100,相对示意值)",
        "hide": "抗主动探测(0-100,相对示意值)",
        "real": "伪装真实度(0-100,相对示意值)",
    },
    "generations": GENS,
    "scenarios": PRESETS,
}

out = ROOT / "data.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"写出 {out} ({out.stat().st_size} bytes):{len(GENS)} 代 / {len(PRESETS)} 剧本")
