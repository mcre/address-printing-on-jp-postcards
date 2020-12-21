import csv
import json
import os
import shutil
import string
import subprocess
import sys

import jaconv


class Template(string.Template):
    delimiter = '@'


def main(input_file, config_file):
    os.makedirs('work', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    address_list = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            address = {}
            for k, v in config['csv_format'].items():
                if isinstance(v, str):
                    address[k] = row.get(v, '')
                else:
                    address[k] = ''.join([row.get(vi, '') for vi in v])
                address[k] = jaconv.h2z(address[k], ascii=True, digit=True)
            for i in range(4):
                fn = f'first_name_{i + 1}'
                ht = f'honorific_title_{i + 1}'
                if address.get(fn, '') != '' and address.get(ht, '') == '':
                    address[ht] = '様'
            for i in range(7):
                address[f'pc{i + 1}'] = address['postal_code'].replace('－', '')[i]

            address_list.append(address)

    with open('templates/page.tex', 'r', encoding='utf-8') as f:
        page_template = f.read()

    pages_tex = ''
    for address in address_list:
        pages_tex += Template(page_template).substitute(address) + '\\newpage\n'

    with open('templates/document.tex', 'r', encoding='utf-8') as f:
        doc_template = f.read()

    tex = Template(doc_template).substitute({'pages': pages_tex})
    with open('work/tmp.tex', 'w', encoding='utf-8') as f:
        f.write(tex)

    try:
        subprocess.run('lualatex --halt-on-error --output-directory work work/tmp.tex > tex_output.txt', shell=True, check=True)
    except subprocess.CalledProcessError:
        print('luatexでエラーが発生しました。')
    else:
        output = f'output/{os.path.basename(input_file)}.pdf'
        shutil.copy('work/tmp.pdf', output)
        print('PDFを出力しました:', output)


if __name__ == '__main__':
    input_file = 'input/sample01.csv'
    config_file = 'config/sample01.json'
    ln = len(sys.argv)
    if ln > 1:
        input_file = sys.argv[1]
    if ln > 2:
        config_file = sys.argv[2]
    main(input_file, config_file)
