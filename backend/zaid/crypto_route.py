import requests
#note : dont remove change headers : (error : access denied)
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
    print_crypto_details(name, details)

