import os
import re
import zipfile
from urllib.parse import urlparse

import requests

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

    def _extract_docx(self, filename):
        document = zipfile.ZipFile(filename)

        content = document.read("word/document.xml", pwd=None).decode()
        regex = re.compile(r"<w:t>(.*?)\<\/w:t>")
        matches = regex.findall(content)
        print(matches)
        return matches

    def _remove_file(self, file):
        os.remove(file)

    def _work_docx(self, docx_files):
        values = {}

        for file in docx_files:
            filename = os.path.basename(urlparse(file).path)
            print(filename)
            self._load_docx(file, filename)
            data = self._extract_docx(filename)
            print(data)
            values.update({filename: {"content": data}})
            self._remove_file(filename)

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

        print(content)

        return content
