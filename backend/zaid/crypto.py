import requests
from bs4 import BeautifulSoup
import json
import time 

def get_top_cryptos(url):
    time.sleep(3)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Send a GET request to the website
    response = requests.get(url, headers=headers) 
    time.sleep(5)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(5)
        main_data = {}
        r1_r2_s1_data = {}
        time.sleep(5)
      
        main_table = soup.find('table', {'class': 'tableWrapper_web_tbl_indices__qR1nw'})
    
        r1_r2_s1_table = soup.find('table', {'class': 'tableWrapper_web_tbl_indices__qR1nw sortdatatable'})
        time.sleep(5)
        if main_table:
           
            rows = main_table.find_all('tr')[1:]  # Exclude header row

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 10:  # Ensure there are enough columns
                    name = columns[0].get_text(strip=True)
                    price = columns[1].get_text(strip=True).replace(',', '')
                    change = columns[2].get_text(strip=True)
                    chg_percent = columns[3].get_text(strip=True)
                    high_24h = columns[4].get_text(strip=True).replace(',', '')
                    low_24h = columns[5].get_text(strip=True).replace(',', '')
                    high_52_week = columns[6].get_text(strip=True).replace(',', '')
                    low_52_week = columns[7].get_text(strip=True).replace(',', '')
                    perf_3m = columns[8].get_text(strip=True)
                    technical_review = columns[9].get_text(strip=True)

                    entry = {
                        'Name': name,
                        'Price': f'Rs. {price}',
                        'Change': change,
                        'Change Percent': chg_percent,
                        '24H High': f'Rs. {high_24h}',
                        '24H Low': f'Rs. {low_24h}',
                        '52 Week High': f'Rs. {high_52_week}',
                        '52 Week Low': f'Rs. {low_52_week}',
                        '3M Performance': perf_3m,
                        'Technical Review': technical_review
                    }

                    main_data[name] = entry

        if r1_r2_s1_table:
           
            rows = r1_r2_s1_table.find_all('tr')[1:]  # Exclude header row

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 9:  # Ensure there are enough columns
                    name = columns[0].get_text(strip=True)
                    ltp = columns[1].get_text(strip=True).replace(',', '')
                    pivot_point = columns[2].get_text(strip=True).replace(',', '')
                    r1 = columns[3].get_text(strip=True).replace(',', '')
                    r2 = columns[4].get_text(strip=True).replace(',', '')
                    r3 = columns[5].get_text(strip=True).replace(',', '')
                    s1 = columns[6].get_text(strip=True).replace(',', '')
                    s2 = columns[7].get_text(strip=True).replace(',', '')
                    s3 = columns[8].get_text(strip=True).replace(',', '')

                    entry = {
                        'Name': name,
                        'LTP': f'Rs. {ltp}',
                        'Pivot Point': f'Rs. {pivot_point}',
                        'R1': f'Rs. {r1}',
                        'R2': f'Rs. {r2}',
                        'R3': f'Rs. {r3}',
                        'S1': f'Rs. {s1}',
                        'S2': f'Rs. {s2}',
                        'S3': f'Rs. {s3}'
                    }

                    r1_r2_s1_data[name] = entry

        # Combine the two dictionaries based on the 'Name'
        combined_data = []
        for name, main_entry in main_data.items():
            if name in r1_r2_s1_data:
                combined_entry = {**main_entry, **r1_r2_s1_data[name]}
                combined_data.append(combined_entry)

        return json.dumps(combined_data, indent=4)
    else:
        return json.dumps({'error': 'Failed to retrieve the webpage.'})

url = 'https://www.moneycontrol.com/crypto-market/market-movers/top-cryptos/inr'
top_cryptos_json = get_top_cryptos(url)
print(top_cryptos_json)
