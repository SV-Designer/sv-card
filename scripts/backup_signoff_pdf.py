#!/usr/bin/env python3
"""簽呈 PDF 備份：裁掉「表單註釋」以下（含簽核列表），存到 DEST_DIR/簽呈編號-{號碼}.pdf

用法：
  backup_signoff_pdf.py <pdf-path> <dest-dir>

行為：
  1. pdfplumber 讀第一頁，regex 抓「表單號:XXX」
  2. 找「表單註釋」word 的 top（pdfplumber top-down 座標）
  3. pypdf 改 page.mediabox/cropbox 的 lower-left y → 隱藏下半（margin=1pt）
  4. 寫到 <dest-dir>/簽呈編號-{號碼}.pdf
"""
import sys
import re
import os
import pdfplumber
import pypdf

CUT_MARGIN_PT = 1  # 「表單註釋」word top 上方留 1pt（實測值，使用者拍板）


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: backup_signoff_pdf.py <pdf-path> <dest-dir>\n")
        sys.exit(1)

    pdf_path, dest_dir = sys.argv[1], sys.argv[2]
    if not os.path.isfile(pdf_path):
        sys.stderr.write(f"ERROR: PDF 不存在: {pdf_path}\n")
        sys.exit(1)
    if not os.path.isdir(dest_dir):
        sys.stderr.write(f"ERROR: 目標資料夾不存在: {dest_dir}\n")
        sys.exit(1)

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        page_h = page.height
        text = page.extract_text() or ""
        m = re.search(r"表單號\s*[:：]\s*(\d+)", text)
        if not m:
            sys.stderr.write("ERROR: 找不到「表單號:」欄位\n")
            sys.exit(1)
        form_no = m.group(1)

        cut_top = None
        for w in page.extract_words():
            if w["text"] == "表單註釋":
                cut_top = w["top"]
                break
        if cut_top is None:
            sys.stderr.write("ERROR: 找不到「表單註釋」word — 此 PDF 結構可能與 TW 街聲版不同\n")
            sys.exit(1)

    new_lly = page_h - cut_top - CUT_MARGIN_PT

    reader = pypdf.PdfReader(pdf_path)
    writer = pypdf.PdfWriter()
    page = reader.pages[0]
    page.mediabox.lower_left = (page.mediabox.lower_left[0], new_lly)
    page.cropbox.lower_left = (page.cropbox.lower_left[0], new_lly)
    writer.add_page(page)

    out_path = os.path.join(dest_dir, f"簽呈編號-{form_no}.pdf")
    with open(out_path, "wb") as f:
        writer.write(f)

    size = os.path.getsize(out_path)
    print(f"✅ 簽呈 PDF 已備份: {out_path} ({size} bytes)")
    print(f"   表單號={form_no} 切點 top={cut_top:.1f} margin={CUT_MARGIN_PT}pt")


if __name__ == "__main__":
    main()
