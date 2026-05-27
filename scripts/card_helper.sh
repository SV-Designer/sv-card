#!/bin/bash
#
# SV 名片自動化流程的 Bash 操作合集
# 由 Claude Code 在 SV_名片自動化製作 SOP 中呼叫
#
# 用法：
#   card_helper.sh init <chinese-full-name> <english-name>
#       建資料夾 + 複製模板 + 開 Illustrator + 輪詢直到 doc 就緒
#
#   card_helper.sh save-original <dest-folder> <basename>
#       從 /tmp 搬 output_original.ai 到 <dest-folder>/<basename>.ai
#       並產生 <dest-folder>/<basename>.jpg（2000×780 預覽）
#
#   card_helper.sh save-ol <dest-folder> <basename>
#       從 /tmp 搬 output_ol.ai 到 <dest-folder>/OL-<basename>.ai
#
# basename 格式範例：20260527-王小明_Ming Wang
# dest-folder 格式範例：/Users/owner/Documents/02_街聲/6 名片/SV/王小明_Ming Wang

set -e

SV_TEMPLATE="/Users/owner/Claude_Owner/SV/1_名片/名片範例/一般名片/1_SV/20260522-王小明.ai"
SV_OUTPUT_BASE="/Users/owner/Documents/02_街聲/6 名片/SV"

cmd="$1"
shift || true

case "$cmd" in
    init)
        chinese_full="$1"
        english_name="$2"
        if [ -z "$chinese_full" ] || [ -z "$english_name" ]; then
            echo "ERROR: init 需要 <chinese-full> <english-name>" >&2
            exit 1
        fi

        name_folder="${chinese_full}_${english_name}"
        dest_dir="$SV_OUTPUT_BASE/$name_folder"
        today=$(date +%Y%m%d)
        new_file="$dest_dir/${today}-${name_folder}.ai"

        mkdir -p "$dest_dir"
        cp "$SV_TEMPLATE" "$new_file"
        echo "✅ 模板已複製: $new_file"

        if pgrep -x "Adobe Illustrator" > /dev/null; then
            echo "⚠️ Illustrator 已在運行，open 可能被歡迎頁攔截。建議冷啟動。"
        fi

        open -a "Adobe Illustrator" "$new_file"
        echo "✅ open 已發送，輪詢 doc 就緒中..."

        for i in $(seq 1 60); do
            sleep 1
            name=$(osascript -e 'tell application "Adobe Illustrator" to if (count of documents) > 0 then return name of current document' 2>/dev/null || echo "")
            if [ -n "$name" ]; then
                echo "✅ ${i}s: doc=$name"
                echo "BASENAME=${today}-${name_folder}"
                echo "DEST_DIR=$dest_dir"
                exit 0
            fi
        done
        echo "❌ 60s 內 Illustrator 未就緒" >&2
        exit 1
        ;;

    save-original)
        dest="$1"
        basename="$2"
        if [ -z "$dest" ] || [ -z "$basename" ]; then
            echo "ERROR: save-original 需要 <dest-folder> <basename>" >&2
            exit 1
        fi

        mv /tmp/output_original.ai "$dest/${basename}.ai"
        cp "$dest/${basename}.ai" /tmp/temp.pdf
        sips -s format jpeg --resampleHeightWidth 780 2000 -s formatOptions 90 /tmp/temp.pdf --out /tmp/preview.jpg > /dev/null
        mv /tmp/preview.jpg "$dest/${basename}.jpg"
        rm /tmp/temp.pdf
        echo "✅ 原檔 + JPG → $dest/"
        ;;

    save-ol)
        dest="$1"
        basename="$2"
        if [ -z "$dest" ] || [ -z "$basename" ]; then
            echo "ERROR: save-ol 需要 <dest-folder> <basename>" >&2
            exit 1
        fi

        mv /tmp/output_ol.ai "$dest/OL-${basename}.ai"
        echo "✅ OL → $dest/OL-${basename}.ai"
        ;;

    *)
        echo "Usage:" >&2
        echo "  $0 init <chinese-full> <english-name>" >&2
        echo "  $0 save-original <dest-folder> <basename>" >&2
        echo "  $0 save-ol <dest-folder> <basename>" >&2
        exit 1
        ;;
esac
