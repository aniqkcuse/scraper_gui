from bs4 import BeautifulSoup
from PySide6.QtWidgets import QWidget
import requests
import random
import pandas as pd
from proxy import search_proxies

def scraping(window: QWidget):
    get_user_agents = requests.get("https://user-agents.net/", timeout=None)
    user_agents_html = BeautifulSoup(get_user_agents.content, "lxml")
    user_agents = []
    ul_main = user_agents_html.find(class_="agents_list")
    lis = ul_main.find_all("li")
    print(lis)
    for li in lis:
        user_agents.append(li.text)
    print(user_agents)
    proxies = search_proxies(user_agents)
    link_next = "https://www.eneba.com/us/store/all?page=1"
    dictionary = {"image":[], "titlePromotion":[], "region":[], "price":[], "whiteList":[], "link":[]}
    counter = 1
    while(counter < 501):
        s = requests.Session()
        headers = {"User-Agent": random.choice(user_agents)}
        proxies_random = {"http": random.choice(proxies)}

        response = s.get(link_next, headers=headers, proxies=proxies_random, timeout=None)
        get_content = BeautifulSoup(response.content, "lxml")

        divs_content = get_content.find_all("div", class_="pFaGHa")
        for div in divs_content:
            try:
                image = div.find("img", class_="LBwiWP")["src"]
                titlePromotion = div.find("span", class_="YLosEL").text
                region = div.find("div", class_="Pm6lW1").text
                price = div.find("span", class_="L5ErLT").text
                whiteList = div.find("span", class_="BwtiXe").text
                link = f"https://www.eneba.com{div.find('a', class_='oSVLlh')['href']}"
                
                dictionary["image"].append(image)
                dictionary["titlePromotion"].append(titlePromotion)
                dictionary["region"].append(region)
                dictionary["price"].append(price)
                dictionary["whiteList"].append(whiteList)
                dictionary["link"].append(link)
            except:
                pass
        try:
            if "disabled" in get_content.find("a", attrs={"rel":"next"}):
                break
            else:
                link_next = get_content.find("a", attrs={"rel":"next"})["href"]
                link_passed = f"Link Passed {counter} \n"
                window.script_log.setText(link_passed)
                window.repaint()
                counter += 1
        except:
            counter += 1
            link_passed = f"Link {counter} error. Not included \n"
            window.script_log.setText(link_passed)
            window.repaint()
            link_next = f"https://www.eneba.com/us/store/all?page={counter}"
            pass

    window.script_log.setText("All link scraped!")

    df = pd.DataFrame(dictionary)
    df.to_csv("data.csv", index=False, sep=";")