import time
import psycopg2.extras
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
from bs4 import BeautifulSoup
from settings import URL_TRIP_RU, URL_TRIP_EN, PASSWORD

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

driver = webdriver.Chrome('/Users/gg.khachatryan/Desktop/chromedriver')

# cursor.execute('select url from reviews')
# urls = cursor.fetchall()
# urls_ru = [URL_TRIP_RU+i[0] for i in urls]
urls = ['/Attraction_Review-g187497-d190624-Reviews-Parc_Guell-Barcelona_Catalonia.html',
        '/Attraction_Review-g187497-d244218-Reviews-Poble_Espanyol-Barcelona_Catalonia.html#REVIEWS',
        '/Attraction_Review-g562814-d667082-Reviews-PortAventura-Salou_Costa_Dorada_Province_of_Tarragona_Catalonia.html#REVIEWS',
        '/Attraction_Review-g298570-d447384-Reviews-Chinatown-Kuala_Lumpur_Wilayah_Persekutuan.html#REVIEWS',
        '/Attraction_Review-g190502-d532762-Reviews-Fish_Market-Bergen_Hordaland_Western_Norway.html#REVIEWS',
        '/Attraction_Review-g297930-d2454044-Reviews-Patong_Beach-Patong_Kathu_Phuket.html#REVIEWS',
        '/Attraction_Review-g293916-d317603-Reviews-The_Grand_Palace-Bangkok.html#REVIEWS',
        '/Attraction_Review-g293916-d546013-Reviews-Khaosan_Road-Bangkok.html#REVIEWS',
        '/Attraction_Review-g667417-d553587-Reviews-Maya_Bay-Ko_Phi_Phi_Lee_Krabi_Province.html#REVIEWS,'
        '/Attraction_Review-g293919-d1441352-Reviews-Walking_Street_Pattaya-Pattaya_Chonburi_Province.html#REVIEWS']
urls_en = [URL_TRIP_EN+i for i in urls]
print(len(urls_en))
for index, url in enumerate(urls_en[1:]):

    print(index, url)
    driver.get(url)
    status = True
    while status is True:
        review_star = []
        # time.sleep(10)
        try:
            driver.find_element(By.XPATH, "//*[@class='ui_icon caret-down location-review-review-list-parts-ExpandableReview__caret--3Ud_i']").click()

        except ElementNotInteractableException:
            time.sleep(0.3)
            continue
        except NoSuchElementException:
            break
        except:
            time.sleep(0.4)
            continue
        json_user = driver.page_source
        soup = BeautifulSoup(json_user, features="html.parsering")
        a = soup.findAll("div", {"class": "location-review-review-list-parts-SingleReview__mainCol--1hApa"})
        for i in a:
            text = i.find("q", {"class": "location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"}).text
            star = i.find("div", {"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"}).span['class'][1][-2:-1]
            review_star.append((text, star))
        cursor.executemany('insert into dataset_en (text,star) values (%s,%s)', review_star)
        connection.commit()

        try:
            driver.find_element(By.XPATH, "//*[@class='ui_button nav next primary ']").click()
        except:
            status = False

driver.quit()

