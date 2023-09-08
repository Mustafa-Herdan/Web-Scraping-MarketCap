import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

page_num = 1
page_end = 2

rank, name, code, country, market, price, one_day, links, description = [], [], [], [], [], [], [], [], []
url = ""

while page_end >= page_num:
    url = f"https://companiesmarketcap.com/page/{page_num}/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    company_rank = soup.find_all("td", {"class": "td-right"})[::3]
    company_name = soup.find_all("div", {"class": "company-name"})
    company_code = soup.find_all("div", {"class": "company-code"})
    company_country = soup.find_all("span", {"class": "responsive-hidden"})[1:]
    company_market = soup.find_all("td", {"class": "td-right"})[1::3]
    company_price = soup.find_all("td", {"class": "td-right"})[2::3]
    company_1d = soup.find_all("td", {"class": "rh-sm"})
    company_link = soup.find_all("div", {"class": "name-div"})

    for i in range(len(company_name)):
        rank.append(company_rank[i].text.strip())
        name.append(company_name[i].text.strip())
        code.append(company_code[i].text.strip())
        country.append(company_country[i].text.strip())
        market.append(company_market[i].text.strip())
        price.append(company_price[i].text.strip())
        one_day.append(company_1d[i].text.strip())
        links.append(company_link[i].a.attrs["href"])

    page_num += 1


for link in links:
    pages = requests.get(f"https://companiesmarketcap.com{link}")
    soups = BeautifulSoup(pages.content, "lxml")
    desc = soups.find("div", {"class": "col-lg-4 company-description"})
    if desc:
        description.append(desc.text.strip())
    else:
        description.append("")

header = ["Rank", "Name", "Code", "Market Cap", "Price", "1d", "Country", "Description"]
data = [rank, name, code, market, price, one_day, country, description]
exported = zip_longest(*data)

with open("Top Companies.csv", "w", newline="", encoding="UTF8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(exported)
