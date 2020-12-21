address-printing-on-jp-postcards
=================================

はがきの宛名印刷のために、csvの住所録をPDFに変換します。

## Requirements

* Docker

## Usage

```
git clone 
cd address-printing-on-jp-postcards
docker build -t texlive-python .
```

サンプル実行

```
docker run -it --rm -v $(pwd):/workdir --rm texlive-python sh -c "python3 main.py input/sample01.csv config/sample01.json"
docker run -it --rm -v $(pwd):/workdir --rm texlive-python sh -c "python3 main.py input/sample02.csv config/sample02.json"
```

## Acknowledgments

* texファイルの構成等はこちらのリポジトリを参考にさせていただきました。
  - https://github.com/rago1975/atena-sashikomi

## Contacts

* [twitter: @m_cre](https://twitter.com/m_cre)

## License

* MIT
  + see LICENSE