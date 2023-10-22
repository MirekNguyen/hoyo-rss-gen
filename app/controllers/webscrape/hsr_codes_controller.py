from app.models import HoyoCode, WebScrape, FeedItem
from datetime import datetime
import re


class HsrCodesController():
    def __init__(self, url):
        self.webscrape = WebScrape(url)
        self.data = self.find_data()
    def find_data(self):
        try:
            tables = self.webscrape.soup.find_all("table")
            data = []
            target_table = None
            for table in tables:
                # Find the previous sibling <h2> element of the table
                title_element = table.find_previous_sibling("h2").find(id="All_Codes")
                if title_element and title_element.get_text() == "All Codes":
                    target_table = table
                    break
            if not target_table or not target_table.find("tbody"):
                self.webscrape.trigger_error("Element 'table' not found.")
                return

            tbody = target_table.find("tbody")
            for row in tbody.find_all("tr"):
                row_data = []
                if "expired" not in row.text.lower():
                    for cell in row.find_all("td"):
                        code = cell.find("code")
                        if code:
                            row_data.append(code.text.strip())
                        else:
                            row_data.append(cell.text.strip())
                    if row_data:
                        data.append(row_data)
            if not data:
                self.webscrape.trigger_error("Element 'table' not found.")
                return []
            return self.__export_data(data)
        except:
            self.webscrape.trigger_error("Element 'tbody' not found.")
            return
    def __export_data(self, data):
        try:
            codes = []
            for item in reversed(data):
                match = re.search(r"Discovered: ([A-Za-z]+ \d{1,2}, \d{4})", item[3])
                if match:
                    title = match.group()
                    date_string = match.group(1)
                    initialization = datetime.strptime(date_string, "%B %d, %Y")
                else:
                    title = item[3]
                    initialization = datetime.now()
                match = re.search(r"Valid until: ([A-Za-z]+ \d{1,2}, \d{4})", item[3])
                if match:
                    date_string = match.group(1)
                    expiration = datetime.strptime(date_string, "%B %d, %Y")
                else:
                    expiration = datetime.now()
                code = HoyoCode(title, item[0], item[3], initialization, expiration)
                codes.append(code)
            if not codes:
                self.webscrape.trigger_error("Error parsing data")
            return codes
        except:
            self.webscrape.trigger_error("Error parsing data")
    def getFeedConfig(self):
        items = []
        if not self.data:
            return items
        sorted_data = sorted(self.data, key=lambda item: item.initiation)
        for item in sorted_data:
            description = (
                "Title: "
                + item.title
                + "<br>"
                + "Code: "
                + item.code
                + "<br>"
                + "Description: "
                + item.description
                + "<br>"
                + "Initiation: "
                + item.initiation.strftime("%y-%m-%d")
                + "<br>"
                + "Expiration: "
                + item.expiration.strftime("%y-%m-%d")
            )
            id = item.title
            title = item.title
            link = "https://hsr.hoyoverse.com/gift?code=" + item.code
            pubDate = item.initiation
            fe = FeedItem(id, title, link, description, pubDate)
            items.append(fe)
        return items
