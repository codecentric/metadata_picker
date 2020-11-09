import os
import re
import zipfile
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from features.metadata_base import MetadataBase


class ExtractFromFiles(MetadataBase):
    def _load_docx(self, docx, filename):
        result = requests.get(docx)
        if result.status_code == 200:
            self.tag_list = result.text.splitlines()
        else:
            self._logger.warning(
                f"Downloading tag list from '{docx}' yielded status code '{result.status_code}'."
            )

        open(filename, "wb").write(result.content)

    def _extract_docx(self, filename) -> list:
        document = zipfile.ZipFile(filename)

        xml_files = document.filelist

        extracted_content = []

        for xml_file in xml_files:
            if xml_file.filename.find(".xml") >= 0:
                content = document.read(xml_file, pwd=None).decode()
                text_pieces = []

                soup = BeautifulSoup(content, "xml")

                if xml_file.filename == "word/document.xml":
                    body = soup.document.body
                elif xml_file.filename == "word/footer1.xml":
                    body = soup.ftr
                elif xml_file.filename == "word/header1.xml":
                    body = soup.hdr
                else:
                    body = None

                if body:
                    text_pieces = [tag.string for tag in body.find_all("t")]

                extracted_content += text_pieces

        return extracted_content

    def _work_docx(self, docx_files):
        values = {}

        for file in docx_files:
            filename = os.path.basename(urlparse(file).path)
            # self._load_docx(file, filename)
            data = self._extract_docx(filename)
            values.update({filename: {"content": data}})
            # os.remove(filename)

        return values

    def _start(self, html_content: str, header: dict) -> dict:
        soup = self._create_html_soup(html_content)

        raw_links = self._extract_raw_links(soup)

        file_extensions = [os.path.splitext(link)[-1] for link in raw_links]

        docx_files = [
            file
            for file, extension in zip(raw_links, file_extensions)
            if extension == ".docx"
        ]

        values = self._work_docx(docx_files=docx_files)

        content = {**values}

        return content
