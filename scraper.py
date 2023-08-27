from bs4 import BeautifulSoup
from PySide6.QtWidgets import QWidget
import requests
import random
import pandas as pd

def scraping(window: QWidget):
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"]

    link_next = "https://www.eneba.com/us/store/all?page=1"
    dictionary = {"image":[], "titlePromotion":[], "region":[], "price":[], "whiteList":[], "link":[]}
    counter = 1
    while(counter < 501):
        headers = {"User-Agent": random.choice(user_agents)}

        response = requests.get(link_next, headers=headers, timeout=None)
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