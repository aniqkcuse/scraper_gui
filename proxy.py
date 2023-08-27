import requests
import random
from bs4 import BeautifulSoup

def search_proxies(user_agents):
    search_proxies = requests.get("https://free-proxy-list.net/", headers={"User-Agent": random.choice(user_agents)})
    get_html_proxies = BeautifulSoup(search_proxies.content, "lxml")

    tbody = get_html_proxies.find("tbody")
    trs_content = tbody.find_all("tr")
    proxies_list = []
    for tr in trs_content:
        td = tr.find_all("td")
        proxies_list.append(f"{td[0].text}:{td[1].text}")
    return proxies_list