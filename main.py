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


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def processing(pconf, address):
    for p in pconf.get('print_only_then', []):
        if address[p['col']] != p['value']:
            return None

    for p in pconf.get('dont_print_then', []):
        if address[p['col']] == p['value']:
            return None

    for p in pconf.get('replace', []):
        address[p['col']] = address[p['col']].replace(p['from'], p['to'])

    for p in pconf.get('split', []):
        for i, v in enumerate(address[p['col']]):
            address[f'{p["col"]}_{i:02}'] = v

    for p in pconf.get('default', []):
        if address.get(p['col']) == '':
            address[p['col']] = p['value']

    for p in pconf.get('show_only_if_exists', []):
        if address.get(p['exists'], '') == '':
            address[p['col']] = ''

    for k, v in address.items():
        address[k] = jaconv.h2z(v, ascii=True, digit=True)

    return address


def main(config_file):
    os.makedirs('work', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    address_list = []
    with open(config['input'], 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            address = {}
            for k, v in config['csv_format'].items():
                if isinstance(v, str):
                    address[k] = row.get(v, '')
                else:
                    address[k] = ''.join([row.get(vi, '') for vi in v])

            address = processing(config['processing'], address)
            if address is not None:
                address_list.append(address)

    doc_template = Template(read(config['templates']['document']))
    page_template = Template(read(config['templates']['page']))
    break_tex = read(config['templates']['page_break'])

    pages = []
    for address in address_list:
        pages.append(page_template.substitute(address))

    tex = doc_template.substitute({'pages': f'\n{break_tex}\n'.join(pages)})

    t = 'work/tmp.tex'
    write(t, tex)
    try:
        subprocess.run(f'lualatex --halt-on-error --output-directory work {t} > work/tex_output.txt', shell=True, check=True)
    except subprocess.CalledProcessError:
        print('luatexでエラーが発生しました。')
    else:
        output = config['output']
        shutil.copy('work/tmp.pdf', output)
        print('PDFを出力しました:', output)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'config/sample01.json')
