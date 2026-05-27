#!/usr/bin/env python3
"""
SV 名片產生流程的「資料層」：vCard + QR Code SVG + 預處理 SVG

由 Claude Code 在 SV_名片自動化製作 SOP 的 Step 7 呼叫。
取代原本內嵌在對話中的 python3 heredoc，目的：
  1. 程式碼存進檔案，使用者可一次性審閱
  2. settings.json 允許清單只放這個特定腳本路徑，安全性高

用法（由 Claude Code 自動呼叫）：

    python3 make_card_artifacts.py \\
        --surname "王" --given "小明" --en "Ming Wang" \\
        --title "美術設計" \\
        --email "mingwang@streetvoice.com" \\
        --mobile "+886 900 000 000" \\
        --folder "/Users/owner/Documents/02_街聲/6 名片/SV/王小明_Ming Wang" \\
        --vcf-name "MingWang.vcf"

執行內容（只做這三件事，不會碰其他位置）：
  1. 在 {folder} 內產生 {vcf-name}（呼叫 make_vcard.make_vcard）
  2. 在 {folder} 內產生 "QR Code.svg"（make_qr.make_qr，
     URL = http://drive.streetvoice.com/vcard/{vcf-name}）
  3. 預處理「QR Code.svg」剝 id="bg" 背景白底 → 寫到 /tmp/qr_processed.svg
     供 place_qr.jsx 在 Illustrator 中匯入

不會做：開檔、改 Illustrator、覆寫資料夾外檔案、發送網路請求。
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_vcard import make_vcard
from make_qr import make_qr


def main():
    p = argparse.ArgumentParser(
        description="Generate vCard + QR SVG + preprocess for SV business card",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--surname", required=True, help="中文姓，例如「王」")
    p.add_argument("--given", required=True, help="中文名，例如「小明」")
    p.add_argument("--en", required=True, help="英文名（含 alias），例如「Ming Wang」或「阿明 Ming Wang」")
    p.add_argument("--title", required=True, help="職稱")
    p.add_argument("--email", required=True)
    p.add_argument("--mobile", required=True, help="沿用簽呈原格式，例如「+886 900 000 000」或「0900-000-000」")
    p.add_argument("--folder", required=True, type=Path, help="輸出資料夾（必須已存在）")
    p.add_argument("--vcf-name", required=True, help="vCard 檔名，例如「MingWang.vcf」（無空格英文名 + .vcf）")
    args = p.parse_args()

    if not args.folder.is_dir():
        sys.exit(f"ERROR: 資料夾不存在或不是目錄: {args.folder}")

    data = {
        "chinese_surname": args.surname,
        "chinese_given": args.given,
        "english_name": args.en,
        "title": args.title,
        "email": args.email,
        "mobile": args.mobile,
    }

    # 1. vCard
    vcf_path = args.folder / args.vcf_name
    make_vcard(data, vcf_path)

    # 2. QR Code SVG
    qr_path = args.folder / "QR Code.svg"
    qr_url = f"http://drive.streetvoice.com/vcard/{args.vcf_name}"
    make_qr(qr_url, qr_path)

    # 3. 預處理 SVG（剝 id="bg" 背景白底）→ /tmp
    svg = qr_path.read_text(encoding="utf-8")
    svg = re.sub(r'<rect id="bg"[^/>]*/>', "", svg)
    Path("/tmp/qr_processed.svg").write_text(svg, encoding="utf-8")
    print("✅ 預處理 SVG → /tmp/qr_processed.svg")


if __name__ == "__main__":
    main()
