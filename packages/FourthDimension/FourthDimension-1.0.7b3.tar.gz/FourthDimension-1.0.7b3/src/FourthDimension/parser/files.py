import os
import tempfile
from typing import Any, Optional
from uuid import UUID

from fastapi import UploadFile
from FourthDimension.doc.spliter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from FourthDimension.utils.file import compute_sha1_from_file
from FourthDimension.config.config import config_setting

chunk_size = config_setting['para_config']['chunk_size']
chunk_overlap = config_setting['para_config']['overlap']


class File(BaseModel):
    id: Optional[UUID] = None
    file: Optional[UploadFile]
    file_name: Optional[str] = ""
    file_size: Optional[int] = None
    file_sha1: Optional[str] = ""
    vectors_ids: Optional[list] = []
    file_extension: Optional[str] = ""
    content: Optional[Any] = None
    chunk_size: int = chunk_size
    chunk_overlap: int = chunk_overlap
    documents: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.file:
            self.file_name = self.file.filename
            self.file_size = self.file.size  # pyright: ignore reportPrivateUsage=none
            self.file_extension = os.path.splitext(
                self.file.filename  # pyright: ignore reportPrivateUsage=none
            )[-1].lower()

    async def compute_file_sha1(self):
        """
        Compute the sha1 of the file using a temporary file
        """
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            await self.file.seek(0)  # pyright: ignore reportPrivateUsage=none
            self.content = (
                await self.file.read()  # pyright: ignore reportPrivateUsage=none
            )
            tmp_file.write(self.content)
            tmp_file.flush()
            self.file_sha1 = compute_sha1_from_file(tmp_file.name)

        os.remove(tmp_file.name)

    def compute_documents(self, loader_class):
        """
        Compute the documents from the file

        Args:
            loader_class (class): The class of the loader to use to load the file
        """

        documents = []
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            tmp_file.write(self.content)  # pyright: ignore reportPrivateUsage=none
            tmp_file.flush()
            loader = loader_class(tmp_file.name)
            documents = loader.load()

        os.remove(tmp_file.name)

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        self.documents = text_splitter.split_documents(documents)
