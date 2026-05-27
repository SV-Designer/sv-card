#!/usr/bin/env python3
"""
StreetVoice 圓點風格 QR Code 產生器

產出 SVG 格式的 QR Code，body 為小圓點（模仿 qrcode-monkey 的 circle body shape）
輸出尺寸 1147×1147 px viewBox 以匹配既有 Illustrator 處理流程

用法:
    from make_qrcode import make_qrcode_svg
    make_qrcode_svg("http://drive.streetvoice.com/vcard/MingWang.vcf", "/path/to/qr.svg")
"""
from pathlib import Path
import qrcode


def make_qrcode_svg(url: str, output_path: Path, dot_ratio: float = 0.45):
    """產生圓點風格 QR Code SVG

    Args:
        url: 要編碼的 URL
        output_path: 輸出 .svg 路徑
        dot_ratio: 圓點半徑相對於格子尺寸的比例（0.4-0.5 看起來最自然）
    """
    qr = qrcode.QRCode(
        version=None,                                       # 自動選版本
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # 中等容錯
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.modules
    size = len(matrix)

    # 匹配 qrcode-monkey 的 1147×1147 viewBox（含 62px 邊距）
    viewbox = 1147
    border = 62
    inner = viewbox - 2 * border  # 1023
    cell = inner / size           # 每個模組像素大小
    radius = cell * dot_ratio

    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
        f'width="{viewbox}px" height="{viewbox}px" '
        f'viewBox="0 0 {viewbox} {viewbox}">',
        # 白色背景（後續 Illustrator 處理流程會自動移除）
        f'<rect x="0" y="0" width="{viewbox}" height="{viewbox}" fill="rgb(255,255,255)"/>',
        '<g fill="rgb(0,0,0)">',
    ]

    # 每個 true 模組畫成圓點（包括 finder pattern 區域）
    # 視覺效果：finder 變成「圓點群集」，類似 qrcode-monkey circle body 模式
    count = 0
    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                cx = border + (x + 0.5) * cell
                cy = border + (y + 0.5) * cell
                parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}"/>')
                count += 1

    parts.append('</g>')
    parts.append('</svg>')

    Path(output_path).write_text("\n".join(parts), encoding="utf-8")
    print(f"OK: {output_path}")
    print(f"  URL: {url}")
    print(f"  QR 版本: {(size - 17) // 4} (size {size}×{size})")
    print(f"  圓點數: {count}")


if __name__ == "__main__":
    make_qrcode_svg(
        "http://drive.streetvoice.com/vcard/MingWang.vcf",
        "/tmp/test_qr.svg",
    )
