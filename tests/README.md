# Tests

煙霧測試（smoke test）— 不需 Adobe Illustrator、不需 FTP server 就能跑的健康檢查。

## 怎麼跑

### 本地（需要 macOS + bash + python3）

```bash
# 完整跑
bash tests/smoke.sh

# 想跑全部檢查（含 shellcheck + jsonschema），先裝套件
brew install shellcheck
pip3 install jsonschema
```

### CI

每次 push 到 `main` 或 PR 時，GitHub Actions 會自動跑（見 `.github/workflows/ci.yml`）。

## 涵蓋什麼

| 檢查 | 跑的工具 | 必跑 / 可跳過 |
|---|---|---|
| Shell 語法 | `bash -n` | 必跑（內建工具）|
| Shell lint | `shellcheck` | 可跳過（未安裝跳過，CI 自動裝）|
| Python 語法 | `python3 -m py_compile` | 必跑（系統內建）|
| Sidecar JSON schema | `jsonschema` + `tests/validate_sidecar.py` | 可跳過（未安裝跳過，CI 自動裝）|

「可跳過」的項目本地沒裝套件不會擋你跑，但 CI 上會強制裝。

## 不涵蓋什麼

需要實機環境才能跑的整合測試**沒做**：

- ❌ `mcp__illustrator__run` 跑 ExtendScript（需 Adobe Illustrator）
- ❌ `card_helper.sh upload-vcard` FTP 連線（需 drive.streetvoice.com 帳號）
- ❌ macOS 系統 API（`sips`、`osascript`、`open`、Keychain）
- ❌ 端到端做一張完整名片

未來想擴充這層測試請考慮分到 `tests/integration/`。

## 怎麼擴充

### 加新 fixture

在 `tests/fixtures/` 加 JSON 檔。命名規則：

- `sidecar_valid.json`、`sidecar_valid_*.json` — 應該通過 schema
- `sidecar_invalid_*.json` — 應該被 schema 抓到（負面樣本，檔名含 `_invalid_` 就會自動被 `validate_sidecar.py` 視為負面樣本）

### 加新檢查 phase

編輯 `tests/smoke.sh`，照既有 `# ─── Phase N` 模式加。如果新檢查依賴某套件，**讓它「未安裝就跳過」**（warn 不 fail），這樣本地裸機跑也不會擋人。

### 改 sidecar 規格

改 `tests/sidecar_schema.json` 後，**務必**對應更新 `tests/fixtures/sidecar_valid.json` 和 `card_helper.sh init` 的 sidecar 寫入邏輯。三者要同步。
