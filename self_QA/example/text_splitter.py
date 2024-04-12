with open('./self_QA/test/test.txt', 'r', encoding="UTF-8") as f:
    state_of_the_union = f.read()
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0,
    add_start_index=True,
    is_separator_regex=True,
    separators=["(?<=。)", "\n", "\n\n", " "]
)

texts = text_splitter.create_documents(state_of_the_union)
print(texts)
