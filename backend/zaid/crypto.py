def get_top_cryptos(url1):
    # Send a GET request to the website
    response = requests.get(url1)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the cryptocurrency data
        table = soup.find('table', {'class': 'tableWrapper_web_tbl_indices__qR1nw'})

        if table:
            # Extract rows from the table
            rows = table.find_all('tr')[1:]  # Exclude header row
            

            data = []
            for row in rows:
                columns = row.find_all('td')
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

                data.append({
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
                })

            return json.dumps(data, indent=4)
        else:
            return json.dumps({'error': 'No table found on the page.'})
    else:
        return json.dumps({'error': 'Failed to retrieve the webpage.'})

url1 = 'https://www.moneycontrol.com/crypto-market/market-movers/top-cryptos/inr'
top_3_cryptos_json = get_top_cryptos(url1)
print(top_3_cryptos_json)
