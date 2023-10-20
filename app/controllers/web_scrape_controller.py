from app.models import HoyoCode, WebScrape
from datetime import datetime
import re


class WebScrapeController():
    def __init__(self, url):
        self.webscrape = WebScrape(url)
        self.data = self.find_data()
    def find_data(self):
        try:
            tbody = self.webscrape.soup.find("tbody")
            data = []
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
                self.webscrape.trigger_error("Element 'tbody' not found.")
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
                print(item[0])

                code = HoyoCode(title, item[0], item[3], initialization, expiration)
                codes.append(code)
            if not codes:
                self.webscrape.trigger_error("Error parsing data")
            return codes
        except:
            self.webscrape.trigger_error("Error parsing data")
