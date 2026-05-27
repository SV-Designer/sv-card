# sv-card

StreetVoice 街聲名片自動化製作。觸發「我要製作名片 / 幫我做 SV 名片」+ 提供簽呈 PDF，自動產出 5 個交付檔（.ai 原檔 / OL CS6 / JPG 預覽 2000×780 / vCard / QR SVG）。

## 結構

```
sv-card/
├── scripts/        執行腳本（card_helper.sh / make_card_artifacts.py / place_qr.jsx 為 SOP 三件套）
├── templates/      Illustrator 模板（假名範例：20260522-王小明.ai）
├── skill/          Claude Code skill 入口（SKILL.md）
└── docs/           完整 SOP（SOP.md）
```

## 預設路徑（symlink 指回本 repo，請勿移動）

| 原路徑 | → 指向 |
|---|---|
| `~/mcp-servers/illustrator-mcp-server/scripts/*.{sh,py,jsx}` | `scripts/` |
| `~/Claude_Owner/SV/1_名片/名片範例/一般名片/1_SV/20260522-王小明.ai` | `templates/20260522-王小明.ai` |
| `~/.claude/skills/sv-card/SKILL.md` | `skill/SKILL.md` |
| `~/Claude_Owner/SV/1_名片/SV_名片自動化製作/SOP.md` | `docs/SOP.md` |

## 使用

詳細流程見 [`docs/SOP.md`](docs/SOP.md)。Claude Code session 中說「幫我做 SV 名片」即可自動觸發。

## 產出位置

名片成品輸出在 `~/Documents/02_街聲/6 名片/SV/{中文姓名}_{英文名去 alias}/`（不在本 repo）。
