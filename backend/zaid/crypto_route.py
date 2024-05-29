import requests
import json

def fetch_and_map_crypto_data(url, exclude_fields=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            headers = data['body']['tableHeaders']
            table_data = data['body']['tableData']['inr']
            mapped_data = map_data_to_headers(table_data, headers, exclude_fields)
            return mapped_data
        except requests.exceptions.JSONDecodeError:
            return None
    else:
        return None

def map_data_to_headers(data, headers, exclude_fields=None):
    mapped_data = []
    for entry in data:
        mapped_entry = {}
        for index, header in enumerate(headers):
            if exclude_fields and header['name'] in exclude_fields:
                continue
            mapped_entry[header['name']] = entry[index]
        mapped_data.append(mapped_entry)
    return mapped_data

def print_crypto_details(name, details):
    print("Cryptocurrency:", name)
    for key, value in details.items():
        print(f"{key}: {value}")
    print()

def calculate_profit_details(entry):
    r2_str = entry.get('R2', '0').replace(',', '')
    last_price_str = entry.get('lastPrice', '0').replace(',', '')
    
    if r2_str and last_price_str:
        r2 = float(r2_str)
        last_price = float(last_price_str)
        profit_percentage = ((r2 - last_price) / last_price) * 100
        profit_amount = r2 - last_price
        entry['profit_percentage'] = round(profit_percentage, 3)
        entry['profit_amount'] = round(profit_amount, 3)
    else:
        entry['profit_percentage'] = 0
        entry['profit_amount'] = 0
        
    return entry

url1 = "https://priceapi.moneycontrol.com/technicalCompanyData/cryptoCurrency/topCrypto?section=pivot&quote=inr&deviceType=W"
mapped_data1 = fetch_and_map_crypto_data(url1)

url2 = "https://priceapi.moneycontrol.com/technicalCompanyData/cryptoCurrency/topCrypto?section=overview&quote=inr&deviceType=W"
exclude_fields = [
    "PerChange1W", "PerChange1M", "PerChange3M", "PerChange6M", 
    "PerChangeYTD", "PerChange1Y", "PerChange2Y", "PerChange3Y", "PerChange5Y"
]
mapped_data2 = fetch_and_map_crypto_data(url2, exclude_fields)

merged_data = {}
for entry in mapped_data1:
    name = entry.get('currencyName')
    if name:
        merged_data[name] = entry
for entry in mapped_data2:
    name = entry.get('currencyName')
    if name:
        merged_data[name].update(entry)

for name, details in merged_data.items():
    merged_data[name] = calculate_profit_details(details)

print(json.dumps(merged_data, indent=4))
