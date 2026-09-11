# proxy-evolution

翻墙协议六代演进的单文件交互图解。单一事实来源是 `index.html` 内嵌的 `GENS` / `PRESETS` 数组；`data.json` 由它生成（含 `innovationText` / `pointsText` / `probeText` 等去 HTML 纯文本字段），供 LLM 直接引用。零依赖、零构建，推 main 即部署 GitHub Pages。

## 常用命令

| 用途 | 命令 |
|---|---|
| 重新生成 data.json | `python3 build-data.py` |
| 校验 data.json 与 index.html 同步（漂移即失败） | `python3 build-data.py && git diff --exit-code -- data.json` |
| 本地预览 | `python3 -m http.server 8000` → http://localhost:8000 |

## 边界

### never

- 不读取、不提交 `.env`
- 不手改 `data.json`——它是生成物；改 `index.html` 后重跑 `build-data.py`

### ask-first

- 新增运行时依赖
- 修改 CI 配置
- 对任何分支 force push

<!-- 这是起点：agent 犯一次错就补一条边界，定期跑 agentsmd-lint。 -->
