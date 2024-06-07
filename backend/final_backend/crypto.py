import requests

## FETCHING CRYPTO DATA

async def fetch_and_map_crypto_data(url, exclude_fields=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                headers = data['body']['tableHeaders']
                table_data = data['body']['tableData']['inr']
                mapped_data = await map_data_to_headers(table_data, headers, exclude_fields)
                return mapped_data
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON")
                return None
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching crypto data: {str(e)}")
        return None

async def map_data_to_headers(data, headers, exclude_fields=None):
    try:
        mapped_data = []
        for entry in data:
            mapped_entry = {}
            for index, header in enumerate(headers):
                if exclude_fields and header['name'] in exclude_fields:
                    continue
                mapped_entry[header['name']] = entry[index]
            mapped_data.append(mapped_entry)
        return mapped_data
    except Exception as e:
        print(f"An error occurred while mapping data to headers: {str(e)}")
        return []

async def calculate_profit_details(entry):
    try:
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
    except Exception as e:
        print(f"An error occurred while calculating profit details: {str(e)}")
        entry['profit_percentage'] = 0
        entry['profit_amount'] = 0
        return entry

async def get_crypto_data():
    try:
        url1 = "https://priceapi.moneycontrol.com/technicalCompanyData/cryptoCurrency/topCrypto?section=pivot&quote=inr&deviceType=W"
        mapped_data1 = await fetch_and_map_crypto_data(url1)

        url2 = "https://priceapi.moneycontrol.com/technicalCompanyData/cryptoCurrency/topCrypto?section=overview&quote=inr&deviceType=W"
        exclude_fields = [
            "PerChange1W", "PerChange1M", "PerChange3M", "PerChange6M", 
            "PerChangeYTD", "PerChange1Y", "PerChange2Y", "PerChange3Y", "PerChange5Y"
        ]
        mapped_data2 = await fetch_and_map_crypto_data(url2, exclude_fields)

        merged_data = {}
        for entry in mapped_data1:
            name = entry.get('currencyName')
            if name:
                merged_data[name] = entry
        for entry in mapped_data2:
            name = entry.get('currencyName')
            if name and name in merged_data:
                merged_data[name].update(entry)

        for name, details in merged_data.items():
            merged_data[name] = await calculate_profit_details(details)

        # Filter, sort the data, and exclude negative profit percentages
        filtered_data = {
            name: details for name, details in merged_data.items()
            if details.get('technicalRating') in ['Bullish', 'Very Bullish'] and details.get('profit_percentage', 0) > 0
        }
        sorted_data = sorted(filtered_data.items(), key=lambda x: x[1]['profit_percentage'], reverse=True)

        # Return only currencyName and lastPrice
        result = [{'name': details['currencyName'], 'last_price': details['lastPrice'], 'expected_price': details['R2'], 'logourl': details['logoUrl'],'changePercent':details['changePercent'],'profit_amount':details['profit_amount'],'profit_percentage':details['profit_percentage']} for tag, details in sorted_data]
        answer=[]
        answer.append(result[:25])
        answer.append(result)
        return answer
    except Exception as e:
        print(f"An error occurred while getting filtered and sorted crypto data: {str(e)}")
        return f"An error occurred while getting filtered and sorted crypto data: {str(e)}"
    
#CRYPTO VALUES GIVER AS PER AFFORDABILITY AND RISK

async def crypto_values_giver(crypto_data, investment_amount):
    try:
        affordable_cryptos = []
        for crypto in crypto_data:
            last_price = float(crypto['last_price'].replace(',', ''))
            if last_price <= investment_amount:
                crypto["quantity"] = round(float(investment_amount/last_price),2)
                affordable_cryptos.append(crypto)
        max_profit = affordable_cryptos[0]["profit_amount"]
        max_profit_quantity = affordable_cryptos[0]["quantity"]
        categorized_cryptos = {'High':[],'Medium':[],'Low':[]}
        for crypto in affordable_cryptos:
            change_percent = abs(float(crypto['changePercent']))
            if change_percent > 6:
                categorized_cryptos['High'].append(crypto)
            elif 3<=change_percent<=6:
                categorized_cryptos['Medium'].append(crypto)
            else:
                categorized_cryptos['Low'].append(crypto)
            for category in categorized_cryptos:
                categorized_cryptos[category] = sorted(categorized_cryptos[category], key=lambda x: x['profit_percentage'], reverse=True)[:3]
        if not categorized_cryptos["High"] and categorized_cryptos["Medium"] and categorized_cryptos["Low"]:
            return None, None, None
        return categorized_cryptos,max_profit,max_profit_quantity
    except Exception as e:
        print(f"error occurred in crypto_values_giver function: {str(e)}")