標的場所にあるpdfファイルの標的ページに長方形を塗った画像を出力します
ページ左上がテンプレートフォルダのtemplete_{N}.pngに一致したときに、
layout_{N}.iniを適用します。
popplerに依存しているpdf2imageを使用していますので、popplerが必要です

----
pdf_rect_files/config.iniの書式

```
[setting]
page_start = 1 #最初の標的ページ（1から数える）、空なら1
page_end = 1 #最後の標的ページ（ページ数より大きい場合は最終ページまで）、空なら1
input_path = input/ # 標的場所、必須
output_path = output/ # 出力場所、必須
failed_output_path = output_failed/ # テンプレート一致しなかった場合の出力場所（空なら出力しない）
template_path = pdf_rect_files/templates/ # テンプレート場所、必須
poppler_path = pdf_rect_files/ # popplerフォルダの場所、必須
log_file = pdf_rect_files/log.txt # ログ出力ファイル（空なら出力しない）
```

----

layout_{N}.iniの書式

```
[ラベル名] #ラベル名は重複しなければ何でも良い
left = 400
top = 100
right = 500
bottom = 200 #上下左右の位置（px単位）, 4つ必須
```
