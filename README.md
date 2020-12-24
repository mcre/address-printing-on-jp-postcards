address-printing-on-jp-postcards
=================================

はがきの宛名印刷のために、csvの住所録をPDFに変換します。

configやテンプレートを変更することで、柔軟な入出力が可能です。

## Requirements

* Docker

## Usage

```
git clone 
cd address-printing-on-jp-postcards
docker build -t texlive-python .
```

### サンプルの実行

```
docker run -it --rm -v $(pwd):/workdir --rm texlive-python sh -c "python3 main.py config/sample01.json"
docker run -it --rm -v $(pwd):/workdir --rm texlive-python sh -c "python3 main.py config/sample02.json"
```

### カスタマイズ

1. [input/](input/) に住所録のcsvファイルを配置します。
2. サンプル([1](config/sample01.json), [2](config/sample02.json))と下記configのフォーマット説明を参考にconfigを作成してください。
3. 必要に応じて [templates/](templates/) も書き換えます。
4. 下記のコードで実行します。

```
docker run -it --rm -v $(pwd):/workdir --rm texlive-python sh -c "python3 main.py config/{ファイル名}.json"
```

## configのフォーマット説明

* input
  - 入力csvファイルのパス
* output
  - 出力pdfファイルのパス
* templates: LuaLaTeX形式のテンプレートファイル
  - document
    - ドキュメント全体のフォーマットを設定したファイルです。
    - pageを埋め込む部分には`@{pages}`を記載する必要があります。
    - pages以外の変数の埋め込みはできません。
  - page
    - 各ページ(1枚のはがき)のフォーマットを設定したファイルです。
    - `@{hoge}`の形式でcsvの各行の項目を埋め込むことができます。
  - page_break
    - ページの区切りに入る行を記載したファイルです。
    - 変数の埋め込みはできません。
* csv_format
  - `"tex埋め込み変数名": "csvの項目名"`を記載します。
  - "csvの項目名"はリストで複数指定することができます。その場合各項目がスペースなしで並びます。
    - 例: `["都道府県", "市区町村", "町域", "番地"]`
* processing
  - csvの項目に下記の処理を行います。それぞれリスト形式で複数設定できます。下記の順で処理します。
    - print_only_then
      - `col`が`value`と等しいときのみ、そのページを出力します。
    - dont_print_then
      - `col`が`value`と等しいときは、そのページを出力しません。
    - replace
      - `col`の文字列のうち`from`の文字を`to`に置換します。
    - split
      - `col`の文字列を1文字ずつに分解し`{col}_XX`のtex埋め込み変数を生成します。XXはゼロから始まるゼロ埋めの2桁の数値です。
    - default
      - `col`がcsvで空文字列の場合または指定されていない場合に、`col`に`value`を設定します。
    - show_only_if_exists
      - `exists`がcsvで空文字列の場合または指定されていない場合に、`col`に空文字列を設定します。

## Acknowledgments

* texファイルの一部はこちらのリポジトリのソースコードを使用させていただいています
  - https://github.com/rago1975/atena-sashikomi

## Contacts

* [twitter: @m_cre](https://twitter.com/m_cre)

## License

* MIT
  + see LICENSE