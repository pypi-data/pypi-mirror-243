import io
import os.path
import re

from fastapi import UploadFile
from FourthDimension.doc.loader import Docx2txtLoader

from FourthDimension.parser.files import File
from .common import process_file


def replace_multiple_newlines(text):
    pattern = r'\n{1,}'  # 匹配连续一个以上的换行符
    replacement = '\n'  # 替换为一个换行符
    updated_text = re.sub(pattern, replacement, text)
    return updated_text


def process_docx(file: File):
    document = process_file(
        file=file,
        loader_class=Docx2txtLoader
    )
    for i, d in enumerate(document):
        document[i].page_content = replace_multiple_newlines(document[i].page_content)
        document[i].metadata['source'] = os.path.basename(document[i].metadata['source'])
    return document


def parse_docx(file_path, file_name):
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Create a file-like object in memory using BytesIO
    file_object = io.BytesIO(file_content)
    upload_file = UploadFile(
        file=file_object, filename=file_name, size=len(file_content)
    )
    file_instance = File(file=upload_file)
    file_instance.content = file_content

    document = process_docx(file_instance)

    for i, doc in enumerate(document):
        document[i].metadata['source'] = file_name
    return document
