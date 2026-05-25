# nice-panels

漫画「nice」の全コマ画像ホスティング用リポジトリ。Webサイトの「ランダム1コマ表示(ガチャ的サムネ)」ウィジェットの画像配信元になる。

## 構成

- `webp/` — 全パネル画像(可逆WebP、1コマ1ファイル)。線画なので無劣化のまま軽量。
- `manifest.json` — 全パネルの一覧。ウィジェットはこれを読んでランダムに1枚選ぶ。
- `build_webp.py` — PNG→WebP変換と manifest 再生成スクリプト。
- `widget.html` — サイト埋め込み用のランダム表示ウィジェット。
- 元PNGはローカルにのみ保持し、リポジトリには含めない(`.gitignore` で除外)。

## コマを増やすとき

1. 新しいパネルPNG(`nice_xxx_x.png`)をこのフォルダに置く
2. `python3 build_webp.py` を実行(増えたぶんだけ変換し、manifest を更新)
3. コミットして push

これだけで `webp/` と `manifest.json` が最新化される。

## 画像URL(jsDelivr)

```
https://cdn.jsdelivr.net/gh/<ユーザー名>/<リポジトリ名>@main/webp/nice_001_1.webp
https://cdn.jsdelivr.net/gh/<ユーザー名>/<リポジトリ名>@main/manifest.json
```

jsDelivr が配信対象にするのは public リポジトリのみ。

## ウィジェットの設置(STUDIO)

1. `widget.html` を開き、先頭の `BASE` を実際の jsDelivr URL に差し替える
   (例: `https://cdn.jsdelivr.net/gh/<ユーザー名>/<リポジトリ名>@main/`)
2. STUDIO の Embed ボックスに `widget.html` の中身を貼り付ける
3. サイトを公開する(Embed/カスタムコードは公開サイトでのみ動作。エディタ内では動かない)

クリックまたは「引き直す」ボタンで別のコマに切り替わる。
