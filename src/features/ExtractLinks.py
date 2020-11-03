import os

from bs4 import BeautifulSoup

from features.MetadataBase import MetadataBase


class ExtractLinks(MetadataBase):
    key: str = "extracted_links"

    @staticmethod
    def __extract_raw_links(html_content: str) -> list:
        soup = BeautifulSoup(html_content, 'html.parser')
        return list({a['href'] for a in soup.find_all(href=True)})

    @staticmethod
    def __extract_extensions(links: list):
        file_extensions = [os.path.splitext(link)[-1] for link in links]
        file_extensions = [x for x in list(set(file_extensions)) if x != ""]
        return file_extensions

    @staticmethod
    def __extract_images(links: list) -> list:
        filenames = [os.path.splitext(link)[0] for link in links]
        file_extensions = [os.path.splitext(link)[-1] for link in links]
        image_extension_whitelist = [".png", ".jpg", ".bmp"]
        proper_files = [filename + file_extension for filename, file_extension in zip(filenames, file_extensions) if
                        file_extension in image_extension_whitelist]
        return proper_files

    @staticmethod
    def __extract_malicious_extensions(extensions: list):
        return []

    def _start(self, html_content: str, header: dict) -> list:
        raw_links = self.__extract_raw_links(html_content)
        image_links = self.__extract_images(raw_links)
        extensions = self.__extract_extensions(raw_links)
        malicious_extensions = self.__extract_malicious_extensions(extensions)

        return {"images": image_links, "malicious_extensions": malicious_extensions, "extensions": extensions,
                "raw_links": raw_links}
