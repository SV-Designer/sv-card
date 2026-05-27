# sv-card

StreetVoice 街聲名片自動化製作。觸發「我要製作名片 / 幫我做 SV 名片」+ 提供簽呈 PDF，自動產出 5 個交付檔（.ai 原檔 / OL CS6 / JPG 預覽 2000×780 / vCard / QR SVG）。

## 結構

```
sv-card/
├── install.sh      安裝腳本（建 symlink、檢查依賴、寫使用者偏好）
├── scripts/        執行腳本（card_helper.sh / make_card_artifacts.py / place_qr.jsx 為 SOP 三件套）
├── templates/      Illustrator 模板（假名範例：20260522-王小明.ai）
├── skill/          Claude Code skill 入口（SKILL.md）
└── docs/           完整 SOP（SOP.md）
```

## 系統需求

- macOS（流程使用 `osascript`、`sips`、`open -a`）
- Adobe Illustrator CC 2024 以上（建議 2026）
- Python 3.9+
- Python 套件：`qrcode`（install.sh 會問你要不要裝）
- [spencerhhubert/illustrator-mcp-server](https://github.com/spencerhhubert/illustrator-mcp-server) — 需自行 clone 並加入 Claude Code 的 MCP 設定
- Claude Code（v2.0+）

## 快速安裝

```bash
git clone https://github.com/chensoo8911/sv-card.git
cd sv-card
bash install.sh
```

install.sh 會做：

1. 檢查 Adobe Illustrator / Python3 / qrcode 套件
2. 偵測 illustrator-mcp-server 安裝位置（若無會印提示）
3. 建立 `~/.claude/skills/sv-card/` 內的 symlink（SKILL.md、scripts、templates、docs）→ 指回本 repo
4. 互動式問你的偏好（輸出資料夾、模板路徑），寫入 `~/.config/sv-card/env`

安裝完成後**重啟 Claude Code**，在對話框說「**幫我做 SV 名片**」+ 附簽呈 PDF 即可觸發。

> 想跳過互動問題用預設值：`bash install.sh --yes`

## 設定覆寫

`~/.config/sv-card/env` 範例：

```bash
SV_OUTPUT_BASE="$HOME/Documents/SV-名片"   # 名片成品輸出資料夾
SV_TEMPLATE="$HOME/.claude/skills/sv-card/templates/20260522-王小明.ai"
```

card_helper.sh 啟動時會 source 此檔；也支援直接用環境變數覆寫（環境變數優先）。

## 產出位置

`$SV_OUTPUT_BASE/{中文姓名}_{英文名去 alias}/` 下 5 個檔案（不在本 repo）。

## 文件

- 執行手冊（精簡）：[`skill/SKILL.md`](skill/SKILL.md)
- 完整 SOP（含已知問題深度說明）：[`docs/SOP.md`](docs/SOP.md)

## 已知限制

- 僅支援 StreetVoice TW 街聲版（一般名片）。子品牌（中子、CN、EN 版）尚未泛化
- 中文路徑 saveAs 會 8700 cancel —— 流程用 /tmp 中轉繞過（card_helper.sh 已封裝）
- Illustrator 必須冷啟動（已運行時 `open` 可能被歡迎頁攔截）
