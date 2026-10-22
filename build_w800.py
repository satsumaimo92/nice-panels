#!/usr/bin/env python3
"""
build_w800.py — 軽量配信用の w800/ を作る(グレー・幅800px・非可逆WebP q60)。

- 入力: webp/*.webp(可逆WebP。こちらが原本。消さない)
- 出力: w800/*.webp (約1/3の容量。サイトの「ランダム1コマ」はこちらを配信)
- 変換済みはスキップ(コマを増やしたあと再実行すれば増えたぶんだけ処理)

【コマを増やしたとき】
1. python3 build_webp.py   (PNG → webp/ と manifest.json)
2. python3 build_w800.py   (webp/ → w800/)
3. コミットして push

依存: Pillow
"""
from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "webp"
DST = HERE / "w800"
WIDTH = 800
QUALITY = 60


def convert(name: str) -> tuple[str, int]:
    src, dst = SRC / name, DST / name
    tmp = DST / (name + ".tmp")
    im = Image.open(src).convert("L")          # 元画像は完全な白黒(色情報なし)
    w, h = im.size
    if w > WIDTH:
        im = im.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
    im.save(tmp, "WEBP", quality=QUALITY, method=6)
    os.replace(tmp, dst)
    return name, dst.stat().st_size


def main() -> None:
    DST.mkdir(exist_ok=True)
    names = sorted(p.name for p in SRC.glob("*.webp"))
    todo = [n for n in names if not (DST / n).exists()]
    print(f"対象 {len(names)}枚 / 今回変換 {len(todo)}枚", flush=True)
    done = 0
    with ProcessPoolExecutor() as ex:
        for _name, _size in ex.map(convert, todo, chunksize=16):
            done += 1
            if done % 500 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    total = sum(p.stat().st_size for p in DST.glob("*.webp"))
    print(f"完了: w800/ {len(list(DST.glob('*.webp')))}枚 / 合計 {total/1024/1024:.0f}MB")


if __name__ == "__main__":
    sys.exit(main())
