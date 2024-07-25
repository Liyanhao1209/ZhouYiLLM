import json

from text_split.QA_split.splitter.BaseSplitter import BaseSplitter
from text_split.QA_split.splitter.rules.impl.word_limit_Rule import word_limit_Rule

if __name__ == '__main__':
    with open('.\\config\\config.json', 'r', encoding='utf-8') as f:
        cons = json.load(f)

    wl = int(cons["word_limit"])
    src = cons["source_root"]
    target = cons["target_root"]

    docx_wl_rule = word_limit_Rule(wl)
    splitter = BaseSplitter(docx_wl_rule, src, target)
    splitter.split_save()
