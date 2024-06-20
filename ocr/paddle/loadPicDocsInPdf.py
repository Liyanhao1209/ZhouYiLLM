from ocr.paddle.document_loader.pdfLoader import RapidOCRPDFLoader
from ocr.paddle.configs.document_config import target_doc

if __name__ == '__main__':
    roots = target_doc["root"]
    target = target_doc["target"]

    import os

    for root in roots:
        for dir_path, dir_names, filenames in os.walk(root):
            for filename in filenames:
                path = os.path.join(dir_path, filename)
                loader = RapidOCRPDFLoader(file_path=str(path))
                print(f'正在处理{path}')
                with open(os.path.join(target, filename.replace('.pdf', '.txt')), 'w', encoding='utf-8') as f:
                    content = loader.load()[0].page_content
                    f.write(content)
                print(f'处理{path}完毕')
