標的場所にあるpdfファイルの標的ページに長方形を塗った画像を出力します

popplerに依存しているpdf2imageを使用していますので、popplerが必要です

----
config.iniの書式

```
[setting]
poppler_path = ./ #popplerフォルダの場所
input_path = input/test/ #標的場所
output_path = output/test/ #出力場所
page_start = 1 #最初の標的ページ（1から数える）
page_end = 999 #最後の標的ページ（ページ数より大きい場合は最終ページまで）
layout = test.ini #長方形の情報を記述したファイル名
```

----

長方形の情報の書式（例としてはtest.ini参照）

```
[ラベル名] #ラベル名は重複しなければ何でも良い
left = 434
top = 134
right = 585
bottom = 200 #上下左右の位置（px単位）, 必須
color_r = 255
color_g = 0
color_b = 0 #色の指定, 任意（指定が無ければ0, すべて指定が無ければ黒になる）
```
