import requests

kb_id = "5d03ee4424704be0be845688d06cad3c"

upload_doc_paths = [
    "C:\\Users\\Administrator\\Desktop\\upload.txt", "C:\\Users\\Administrator\\Desktop\\《周易》大模型.pptx",
    "C:\\Users\\Administrator\\Desktop\\college\\junior2\\项目实训\\开题阶段\\《周易》大模型开题答辩.pptx"]  # ["C:\\Users\\Administrator\\Desktop\\《周易》大模型.pptx"]  # ,"C:\\Users\\Administrator\\Desktop\\college\\junior2\\项目实训\\开题阶段\\《周易》大模型开题答辩.pptx"]

api_url = "http://127.0.0.1:9090/knowledge_base/upload-knowledge-files"

if __name__ == '__main__':

    def request_upload_doc(file_path: str, url: str):

        with open(file_path, "rb") as file:
            files = {"files": (file_path, file)}
            form_data = {
                "kb_id": kb_id
            }
            response = requests.post(url, files=files, data=form_data)

        print(response.text)


    for upload_doc_path in upload_doc_paths:
        request_upload_doc(upload_doc_path, api_url)
