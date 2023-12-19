import os
import sys
import requests
import mysql.connector
import json
# add the directory containing the db module to the Python path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(db_path)
from db.db_actions import insert_data


api_url = "https://www.fahasa.com/fahasa_catalog/product/loadCatalog"

headers = {
  'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'www.fahasa.com',
  'Cookie': 'frontend=25ce42b62fba4fba87697a462a1d7add; frontend_cid=4oERUjGNSzVdg4un'
}

def get_data():
    page_num = 1
    try:
        while True:
            # Demo 20 page 
            if page_num > 20:
                break
            params = {'category_id': 2, 'currentPage': page_num}
            response = requests.get(api_url,headers=headers,params=params)
            
            api_data = json.loads(response.text)['product_list']
            # break if no more data
            if not api_data:
                break

            for item in api_data:
                insert_data(item)  

            page_num += 1
    except Exception as e:
            print("\n\nSập !!")
            
if __name__ == '__main__':
    get_data()

