from text_split.QA_split.splitter.rules.abRule import abRule
import os
import logging


class BaseSplitter:

    def __init__(self, split_rule: abRule, source_root: str, target_root: str):
        self.rule = split_rule
        self.src = source_root
        self.target = target_root

    def split_save(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        for dir_path, dir_names, file_names in os.walk(self.src):
            for fn in file_names:
                logging.debug(f"Dealing with {fn} in {dir_path}")
                os.makedirs(os.path.join(self.target, fn), exist_ok=True)
                task = os.path.join(dir_path, fn)
                splits = self.rule.split(task)
                self.rule.save(os.path.join(self.target, fn), splits)
                logging.debug(f"Done with {fn} in {dir_path}")
