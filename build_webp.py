#!/usr/bin/env python3
"""
build_webp.py — パネルPNGを可逆WebPに変換し、manifest.json を生成する。

- panels/*.png → panels/webp/*.webp(可逆WebP。線画なので無劣化のまま軽量化)
- 変換済みのものはスキップ(再実行すると増えたぶんだけ処理)
- 変換後、webp/ 内の全ファイルから manifest.json を再生成する

【コマを増やしたとき】
新しいパネルPNGを panels/ に置き、このスクリプトを再実行 → コミットして push。
これだけで webp と manifest が更新される。

使い方:
    python3 build_webp.py
    python3 build_webp.py --limit 450     # 一度に変換する上限枚数

依存: Pillow
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser(description="パネルPNG → 可逆WebP + manifest生成")
    ap.add_argument("--src", default=str(HERE), help="PNGフォルダ(既定: このスクリプトの場所)")
    ap.add_argument("--webp-dir", default=str(HERE / "webp"), help="WebP出力先")
    ap.add_argument("--limit", type=int, default=0, help="一度に変換する上限(0=無制限)")
    args = ap.parse_args()

    src = Path(args.src)
    webp = Path(args.webp_dir)
    webp.mkdir(parents=True, exist_ok=True)

    pngs = sorted(src.glob("*.png"))
    todo = [p for p in pngs if not (webp / f"{p.stem}.webp").exists()]
    if args.limit:
        todo = todo[: args.limit]

    t0 = time.time()
    for p in todo:
        dst = webp / f"{p.stem}.webp"
        tmp = webp / f"{p.stem}.webp.tmp"          # 中断対策: 一時名で書いて原子的に置換
        Image.open(p).save(tmp, "WEBP", lossless=True, quality=100, method=4)
        os.replace(tmp, dst)
    el = time.time() - t0

    done = sorted(webp.glob("*.webp"))
    print(f"今回変換: {len(todo)}枚 ({el:.1f}秒) / WebP累計: {len(done)}枚 / PNG総数: {len(pngs)}枚")

    # manifest 再生成(webp/ にある全ファイルの相対パス一覧)
    panels = sorted(f"webp/{f.name}" for f in done)
    (HERE / "manifest.json").write_text(
        json.dumps({"count": len(panels), "panels": panels}, ensure_ascii=False),
        encoding="utf-8",
    )

    remaining = len(pngs) - len(done)
    if remaining > 0:
        print(f"未変換 残り {remaining}枚 — もう一度実行してください。")
    else:
        print(f"全 {len(done)}枚 変換済み。manifest.json を更新しました。")


if __name__ == "__main__":
    main()
