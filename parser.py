#pip install beautifulsoup4 requests lxml

#https://health-diet.ru/table_calorie

from os import O_RANDOM
import requests
from bs4 import BeautifulSoup
import json
import csv
#url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu§utm_medium=table_calorie"
#url = "https://health-diet.ru/table_calorie"

headers =  { 
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
} 


#req = requests.get(url,headers=headers)
#src=req.text
#print(src)
#with open("Index.html", "w") as file:
#    file.write(src)

#with open("index.html") as file:
#    src = file.read()

#soub =BeautifulSoup(src, "lxml")


#all_product_hrefs=soub.find_all(class_="mzr-tc-group-item-href")
#all_categories_dict = {}

#for item in all_product_hrefs:
#    item_text = item.text
#    item_href = "https://health-diet.ru" + item.get("href") 
#    #print(f"{item_text}:{item_href}")
#    all_categories_dict[item_text]=item_href

###-------------------Сохранение файла в Json рабочий с кирилицей
#with open("all_categories_dict.json","w") as file:
#    json.dump(all_categories_dict,file,indent=4,ensure_ascii=False)
###

with open("all_categories_dict.json") as file:
    all_categories= json.load(file)

#print(all_categories)
iteration_count = int(len(all_categories)) -1
count=0
## Замена символов на "_"
for category_name, category_href in all_categories.items():
#    if count ==0:
        rep = [",", " ","-","'",")","("]

        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item,"_")

        req= requests.get(url=category_href,headers=headers)
        src=req.text

        with open(f"data/{count}_{category_name}.html", "w") as file:
            file.write(src)

        with open(f"data/{count}_{category_name}.html") as file:
            src= file.read()
        
        soup=BeautifulSoup(src,"lxml")
        alert_block = soup.find(class_="uk-alter-danger")
        if alert_block is not None:
            continue 
        Table_head=soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
        produkt = Table_head[0].text
        colories = Table_head[1].text
        proteins = Table_head[2].text
        fats = Table_head[3].text
        carbohydrates = Table_head[4].text
        with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    produkt,
                    colories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
            
        produkt_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
        for item in produkt_data:
            produkt_tds = item.find_all("td")

            title= produkt_tds[0].find("a").text
            colories = produkt_tds[1].text
            proteins = produkt_tds[2].text
            fats = produkt_tds[3].text
            carbohydrates = produkt_tds[4].text

            with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        colories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
            
        count +=1     
        iteration_count =iteration_count -1
        if iteration_count==0:
            print("Fin")
            break
        #print("Осталось итераций {iteration_count}")
        #sleep(random.randomrange(2, 4))