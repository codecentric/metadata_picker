from bs4 import BeautifulSoup

from features.MetadataBase import MetadataBase


class ExtractLinks(MetadataBase):
    key: str = "extracted_links"

    def _start(self, html_content: str, header: dict) -> list:
        files = []
        print("_start2")
        # print(html_content)

        soup = BeautifulSoup(html_content, 'html.parser')
        links_with_text = []
        for a in soup.find_all('a', href=True):
            if a.text:
                links_with_text.append(a['href'])
        print("links_with_text: ", links_with_text)

        # TODO Remove this function
        def getURL(page):
            """

            :param page: html of web page (here: Python home page)
            :return: urls in that page
            """
            start_link = page.find("href")  # formerly "a href"
            if start_link == -1:
                return None, 0
            start_quote = page.find('"', start_link)
            end_quote = page.find('"', start_quote + 1)
            url = page[start_quote + 1: end_quote]
            return url, end_quote

        while True:
            url, n = getURL(html_content)
            html_content = html_content[n:]
            if url:
                files.append(url)
            else:
                break
        print("files: ", files)

        s = set(links_with_text)
        temp3 = [x for x in files if x not in s]
        print("temp3: ", temp3)
        print(len(files), len(links_with_text), len(temp3))
        return files
