#!/bin/zsh
cd "$(dirname "$0")" || exit 1
python3 scripts/build.py || exit 1
printf '本地预览：http://127.0.0.1:5680/\n停止预览：按 Ctrl+C\n'
python3 -m http.server 5680 --bind 127.0.0.1 --directory dist
