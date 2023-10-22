from app.models import HoyoVersion, WebScrape, FeedItem
from datetime import datetime
import re


class GenshinVersionsController():
    def __init__(self, url):
        self.webscrape = WebScrape(url)
        self.data = self.find_data()
    def find_data(self):
        try:
            tables = self.webscrape.soup.find_all("table")
            target_tables = []
            data = []
            for table in tables:
                # Find the previous sibling <h3> element of the table
                prev = table.find_previous_sibling("h3")
                if (prev != None):
                    title_element = prev.findAll(id=re.compile(r"Version_\d+"))
                    if (title_element):
                        target_tables.append(table)
            for target_table in target_tables:
                if not target_table or not target_table.find("tbody"):
                    self.webscrape.trigger_error("Element 'tbody' not found.")
                    return []
                tbody = target_table.find("tbody")
                for row in tbody.find_all("tr"):
                    row_data = []
                    for cell in row.find_all("td"):
                        row_data.append(cell.text.strip())
                    if row_data:
                        data.append(row_data)
            if not data:
                self.webscrape.trigger_error("Element 'table' not found.")
                return []
            return self.__export_data(data)
        except:
            self.webscrape.trigger_error("Error processing 'data'.")
            return

    def __export_data(self, data):
        try:
            versions = []
            for item in data:
                if (item[2] == "TBA"):
                    continue
                version = HoyoVersion(item[1], item[0], datetime.strptime(item[2], "%B %d, %Y"))
                versions.append(version)
            return versions
        except:
            self.webscrape.trigger_error("Error parsing data")

    def getFeedConfig(self):
        items = []
        if not self.data:
            return items
        sorted_data = sorted(self.data, key=lambda item: item.release_date)
        for item in sorted_data:
            description = (
                "Title: " 
                + item.title
                + "<br>" 
                + "Version: " 
                + item.version
                + "<br>"
                + "Release date: "
                + item.release_date.strftime("%y-%m-%d")
            )
            id = item.title
            title = item.version + " | " + item.title
            link = ""
            release_date = item.release_date
            fe = FeedItem(id, title, link, description, release_date)
            items.append(fe)
        return items
