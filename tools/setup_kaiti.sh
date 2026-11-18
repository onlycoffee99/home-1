#!/bin/bash
# 函文預覽 PDF 用楷書:安裝 AR PL UKai 並把「標楷體」對應過去(雲端容器每次新開需跑一次)
set -e
fc-list | grep -qi "UKai TW" || { apt-get install -y -q fonts-arphic-ukai >/dev/null 2>&1 || { apt-get update -q >/dev/null 2>&1; apt-get install -y -q fonts-arphic-ukai >/dev/null 2>&1; }; }
mkdir -p /etc/fonts/conf.d
cp "$(dirname "$0")/fonts/99-kaiti-alias.conf" /etc/fonts/conf.d/99-kaiti-alias.conf
fc-cache -f >/dev/null
echo "標楷體 → $(fc-match 標楷體)"
