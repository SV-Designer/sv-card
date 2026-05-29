#!/usr/bin/env python3
"""
StreetVoice 名片 vCard 產生器

用法:
    python3 make_vcard.py
    (資料目前 hardcoded 在 main 區，未來可改成讀 JSON)

設計概念:
    - 從一個「樣板 vCard」抽取共用欄位（公司 logo PHOTO、FAX、地址、ORG、URL）
    - 套上個人化資料產生新 .vcf
"""
import os
from pathlib import Path

# === 樣板 vCard：含公司 logo PHOTO 區塊（僅在 include_photo=True 時讀取）===
# 預設 None 代表不嵌 PHOTO（macOS 通訊錄會自動依姓氏產字母頭貼，這是建議行為）。
# 若要嵌入自訂 PHOTO，請設環境變數 SV_VCARD_TEMPLATE 指向樣板 .vcf
TEMPLATE_VCF = Path(os.environ["SV_VCARD_TEMPLATE"]).expanduser() if os.environ.get("SV_VCARD_TEMPLATE") else None


def extract_photo_block(template_path: Path) -> str:
    """從樣板 vCard 抽出 PHOTO;ENCODING=b;TYPE=JPEG:... 整段（含後續折行）"""
    text = template_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    photo_lines = []
    in_photo = False
    for line in lines:
        if line.startswith("PHOTO;"):
            in_photo = True
            photo_lines.append(line)
        elif in_photo:
            # vCard 折行：以空白開頭表示同一欄位的續行
            if line.startswith(" ") or line.startswith("\t"):
                photo_lines.append(line)
            else:
                break  # PHOTO 結束
    return "\r\n".join(photo_lines)


def build_vcard(data: dict, photo_block: str = "") -> str:
    """根據個人資料 dict 產生完整 vCard 文字

    photo_block 為空時不嵌入 PHOTO，
    macOS 通訊錄會自動依姓氏產生字母頭貼（建議的預設行為）
    """
    cn_surname = data["chinese_surname"]
    cn_given = data["chinese_given"]
    en_name = data["english_name"]      # 含 alias 如「阿明 Ming Wang」
    title = data["title"]
    email = data["email"]
    # mobile 可選：簽呈沒填手機時為空字串 / None，跳過 TEL CELL 整行
    mobile = data.get("mobile") or ""

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "PRODID:-//StreetVoice CardGen//EN",
        f"N:{cn_surname};{cn_given};;;",
        f"FN:{cn_given} {cn_surname}",
        f"NICKNAME:{en_name}",
        "ORG:街聲股份有限公司 (StreetVoice);",
        f"TITLE:{title}",
        f"EMAIL;type=INTERNET;type=pref:{email}",
        "TEL;type=WORK;type=VOICE;type=pref:02-27417065",
        "TEL;type=WORK;type=FAX:02-27488490",
    ]
    if mobile:
        lines.append(f"TEL;type=CELL;type=VOICE:{mobile}")
    lines.extend([
        "ADR;type=WORK;type=pref:;;松山區光復北路 11 巷 35 號 11 樓;松山區;台北市;105;台灣",
        "URL;type=WORK;type=pref:www.streetvoice.com",
    ])
    if photo_block:
        lines.append(photo_block)
    lines.append("END:VCARD")
    lines.append("")  # 收尾換行
    return "\r\n".join(lines)


# 公司 vCard 公開存放網址前綴（上傳後可從此 URL 取得檔案）
VCARD_URL_BASE = "http://drive.streetvoice.com/vcard/"


def make_vcard(data: dict, output_path: Path, include_photo: bool = False):
    """include_photo=False (預設): 不嵌入 PHOTO，macOS 自動產姓氏頭貼

    產出 vCard 後同時印出公司公開 URL，方便複製貼到 QR Code 產生器
    """
    if include_photo:
        if TEMPLATE_VCF is None:
            raise RuntimeError(
                "include_photo=True 但未設定 SV_VCARD_TEMPLATE 環境變數，請指向樣板 .vcf"
            )
        photo_block = extract_photo_block(TEMPLATE_VCF)
    else:
        photo_block = ""
    content = build_vcard(data, photo_block)
    output_path.write_text(content, encoding="utf-8")
    print(f"OK: 寫入 {output_path} ({output_path.stat().st_size} bytes)")
    public_url = VCARD_URL_BASE + output_path.name
    print(f"📋 vCard 上傳後 URL:  {public_url}")


if __name__ == "__main__":
    # 測試資料（範例）
    data = {
        "chinese_surname": "王",
        "chinese_given": "小明",
        "english_name": "阿明 Ming Wang",
        "title": "美術設計",
        "email": "mingwang@streetvoice.com",
        "mobile": "0900-000-000",
    }
    output_path = Path("/tmp/MingWang.vcf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    make_vcard(data, output_path)
