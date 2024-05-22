# Databricks notebook source
import random
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_site_data(hit_input):
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            # 'cache-control': 'max-age=0',
            # 'priority': 'u=0, i',
            # 'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            # 'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'sec-fetch-dest': 'document',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'same-origin',
            # 'sec-fetch-user': '?1',
            # 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        response = requests.get(
            'https://www.booktopia.com.au/safe-haven-shankari-chandran/book/'+str(hit_input)+'.html',
            headers=headers,
        )
        return response

    except:
        return 'Data Not Found'

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
        if hit_input != '':
            hit_input = int(hit_input)
        single_dict['ISBN'] = hit_input
        try:
            time.sleep(random.randint(1,2))
            Hit_site = get_site_data(hit_input)
            Hit_site = Hit_site.text
        except:

            try:
                for i in range(1,3):
                    time.sleep(random.randint(1,2))
                    Hit_site = get_site_data(hit_input)
                    if Hit_site != 'Data Not Found' or Hit_site.status_code == 200 :
                        Hit_site = Hit_site.text
                        break
            except:
                final_data.append(single_dict)
                continue
        try:
            main_data = BeautifulSoup(Hit_site, 'html.parser')
            parsing_data = get_parsing_data(main_data,single_dict)
            final_data.append(parsing_data)
        except:
            pass

final_csv_out = get_csv_file(final_data)
print(final_csv_out)

