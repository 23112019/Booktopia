import random
import numpy as np
import requests
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


def get_site_data(hit_input):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        input_url = "https://www.booktopia.com.au/safe-haven-shankari-chandran/book/"+str(hit_input)+".html"
        driver = webdriver.Chrome(r'chromedriver.exe',chrome_options=chrome_options)
        driver.get(input_url)
        time.sleep(2)
        page_data = driver.page_source
        return page_data
    except:
        "Data Not Found"

def get_parsing_data(main_data,single_dict):
    try:
        single_dict['Title']  = main_data.find('h1',{'class':'MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk'}).text.strip()
    except:
        single_dict['Title'] = ''

    try:
        single_dict['Author']  = main_data.find('span',{'class':'MuiTypography-root MuiTypography-body1 mui-style-1plnxgp'}).text.strip()
    except:
        single_dict['Author'] = ''

    try:
        single_dict['Original Price']  = main_data.find('div',{'class':'MuiStack-root BuyBox_rrp__poxjK mui-style-a6l0c3'}).text.replace('RRP $','').strip()
    except:
        single_dict['Original Price'] = ''

    try:
        single_dict['Discounted price']  = main_data.find('p',{'class':'MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox'}).text.replace('$','').strip()
    except:
        single_dict['Discounted price'] = ''

    try:
        other_data = main_data.find('div',{'class':'MuiBox-root mui-style-h3npb'}).find_all('p')

        for j in other_data:
            try:
                col_name = j.find('span').text.replace(':','').strip()
                col_data = j.find('span').nextSibling.text.replace(':','').strip()
                single_dict[col_name]  = col_data
            except:
                continue
    except:
        pass
    return single_dict

def get_csv_file(final_data):
    try:
        df = pd.DataFrame(final_data)
        df.to_csv('output.csv',index=None)
        return 'file out'
    except:
        return 'file not out'

if __name__ == "__main__":
    final_data = []
    read_input_file = pd.read_csv('input_list.csv').replace(np.nan,'')
    for i,row in read_input_file.iterrows():

        print('Total_input:-',len(read_input_file),' --------------- | ----------- ','Running:-',int(i)+1)

        single_dict = {}
        hit_input = row[0]
        if hit_input !='':
            hit_input = int(hit_input)
        print(hit_input)
        single_dict['ISBN'] = hit_input
        try:
            time.sleep(random.randint(1,2))
            Hit_site = get_site_data(hit_input)
        except:
            try:
                for i in range(1,3):
                    time.sleep(random.randint(1,2))
                    Hit_site = get_site_data(hit_input)
                    if Hit_site != 'Data Not Found':
                        break
            except:
                final_data.append(single_dict)
                continue
        try:
            main_data = BeautifulSoup(Hit_site, 'html.parser')
            parsing_data = get_parsing_data(main_data,single_dict)
            final_data.append(parsing_data)
        except:
            final_data.append(single_dict)

final_csv_out = get_csv_file(final_data)
print(final_csv_out)
