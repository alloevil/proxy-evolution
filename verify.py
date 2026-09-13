#!/usr/bin/env python3
"""收据门禁:文档与已核实的事实是否还一致。

用法: python3 verify.py            # 逐条检查,任一失败退出码 1
      python3 verify.py --json     # 机器可读输出

检查三件事:
1. 每条 claim 的 receipts:指定文件里必须出现/必须不出现指定文本;
   (claims.json 里另有可执行的 check(cmd/expect),那是对外数字的收据,由 verify-claims 跑,
    见 .github/workflows/claims.yml;本脚本只管文档措辞与生成物一致)
2. banned_phrases:被证伪的措辞不得在任何文本文件里复发;
3. data.json 是否与 index.html 同步(index.html 是唯一事实源,data.json 由 build-data.py 生成)。
它不重新判断协议本身(那是上游来源的事),只保证「改过的错不再回来、生成物不漂移」。
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
DOC = json.loads((ROOT / "claims.json").read_text(encoding="utf-8"))
# claims.json is deliberately NOT scanned for banned phrases: it must be allowed to name them.
TEXT_FILES = ["index.html", "README.md", "README.en.md", "llms.txt", "AGENTS.md"]

SECTIONS = {c["id"]: c for c in DOC["claims"]}


def load():
    return {f: (ROOT / f).read_text(encoding="utf-8") for f in TEXT_FILES if (ROOT / f).exists()}


def run_checks():
    files = load()
    results, failures = [], 0

    # 1. per-claim checks
    for c in DOC["claims"]:
        problems = []
        src = c.get("source", {})
        if not src.get("url") or not src.get("quote"):
            problems.append("receipt incomplete: source url/quote missing")
        for chk in c.get("receipts", []):
            name = chk["file"]
            if name not in files:
                problems.append(f"unknown file: {name}")
                continue
            text = files[name]
            for s in chk.get("must_contain", []):
                if s not in text:
                    problems.append(f"{name}: missing {s!r}")
            for s in chk.get("must_not_contain", []):
                if s in text:
                    problems.append(f"{name}: should be gone {s!r}")
        if problems:
            failures += 1
        results.append({"id": c["id"], "level": "error" if problems else "ok",
                        "generation": c.get("generation", ""), "problems": problems})

    # 2. banned phrases must not reappear anywhere
    for phrase in DOC.get("banned_phrases", []):
        where = [name for name, text in files.items() if phrase in text]
        if where:
            failures += 1
            results.append({"id": f"banned:{phrase}", "level": "error", "generation": "",
                            "problems": [f"found in {', '.join(where)}"]})

    # 3. data.json must be exactly what build-data.py produces from index.html
    before = hashlib.sha256((ROOT / "data.json").read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(ROOT / "build-data.py")], cwd=ROOT,
                   capture_output=True, check=True)
    after = hashlib.sha256((ROOT / "data.json").read_bytes()).hexdigest()
    if before != after:
        failures += 1
        results.append({"id": "data.json-drift", "level": "error", "generation": "",
                        "problems": ["data.json was out of sync with index.html and has been regenerated - commit it"]})
    else:
        results.append({"id": "data.json-drift", "level": "ok", "generation": "", "problems": []})

    return results, failures


def main():
    results, failures = run_checks()
    if "--json" in sys.argv:
        print(json.dumps({"tool": "proxy-evolution-verify", "target": str(ROOT),
                          "summary": {"ok": len(results) - failures, "error": failures},
                          "results": results}, ensure_ascii=False))
        return 1 if failures else 0
    print(f"proxy-evolution-verify  {ROOT}")
    print(f"updated: {DOC.get('updated', '?')} · {len(DOC['claims'])} claims · "
          f"{len(DOC.get('banned_phrases', []))} banned phrases\n")
    for r in results:
        mark = "✓" if r["level"] == "ok" else "✗"
        gen = f"{r['generation']} · " if r["generation"] else ""
        print(f"  {mark} [{gen}{r['id']}]")
        for p in r["problems"]:
            print(f"      → {p}")
    print(f"\nverified: ok {len(results) - failures} · error {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
