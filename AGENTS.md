# proxy-evolution

翻墙协议六代演进的单文件交互图解。单一事实来源是 `index.html` 内嵌的 `GENS` / `PRESETS` 数组；`data.json` 由它生成（含 `innovationText` / `pointsText` / `probeText` 等去 HTML 纯文本字段），供 LLM 直接引用。零依赖、零构建，推 main 即部署 GitHub Pages。

**规则：机制层断言必须有一手来源（规范 / 参考实现 / RFC / 官方发布说明）。** 机械版本是 `claims.json`：每条断言带来源原文引用与 `check`（哪个文件里必须出现/必须不出现什么），由 `verify.py` 执行；被证伪的措辞列在 `banned_phrases`，复发即失败。

## 常用命令

| 用途 | 命令 |
|---|---|
| 收据门禁（断言 × 禁用措辞 × data.json 漂移） | `python3 verify.py`（加 `--json` 出机器可读） |
| 重新生成 data.json | `python3 build-data.py` |
| 校验 data.json 与 index.html 同步（漂移即失败） | `python3 build-data.py && git diff --exit-code -- data.json` |
| 本地预览 | `python3 -m http.server 8000` → http://localhost:8000 |

## 边界

### never

- 不读取、不提交 `.env`
- 不手改 `data.json`——它是生成物；改 `index.html` 后重跑 `build-data.py`
- 不单独改 `claims.json` 里的 `source.quote` / `check`：那是收据本体，改断言要连出处一起改
- 不引入 `banned_phrases` 里的措辞（`verify.py` 拦）

### ask-first

- 新增运行时依赖
- 修改 CI 配置
- 对任何分支 force push

<!-- 这是起点：agent 犯一次错就补一条边界，定期跑 agentsmd-lint。 -->
