import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re




# Dictionary mapping locations to their respective URLs
async def get_url(location):
    location_url_map = {
        'pune': 'https://www.nobroker.in/property/sale/pune/multiple?searchParam=W3sibGF0IjoxOC41NTc3NDQ2LCJsb24iOjczLjkxMjQ2NzQsInBsYWNlSWQiOiJDaElKaVNGeWVzWEF3anNScmN5RkZzUHlzTkUiLCJwbGFjZU5hbWUiOiJQdW5lIn0seyJsYXQiOjE4LjUwNzM1MTQsImxvbiI6NzMuODA3NjU0MywicGxhY2VJZCI6IkNoSUpuWVN2TXJlX3dqc1I4RVQtczBpTEI5USIsInBsYWNlTmFtZSI6IktvdGhydWQifSx7ImxhdCI6MTguNTA4NjQyOSwibG9uIjo3My44MzE0MDkxLCJwbGFjZUlkIjoiQ2hJSndfQnlYNHVfd2pzUmVwc1U0Z3RNX3drIiwicGxhY2VOYW1lIjoiRXJhbmR3YW5lIn1d&radius=2.0&city=pune&locality=Pune,Kothrud,Erandwane',
        'mumbai': 'https://www.nobroker.in/property/sale/mumbai/multiple?searchParam=W3sibGF0IjoxOS4yNDY3MjE4LCJsb24iOjcyLjk3NTk3MTMsInBsYWNlSWQiOiJDaElKNjQwYUNCSzU1enNSaWZwc0V5U1kydU0iLCJwbGFjZU5hbWUiOiJUaGFuZSBXZXN0In0seyJsYXQiOjE5LjIzODA2ODMsImxvbiI6NzIuODUyMjUxMiwicGxhY2VJZCI6IkNoSUo5eGZSUE02dzV6c1JrdlpibFl0VlhWRSIsInBsYWNlTmFtZSI6IkJvcml2YWxpIFdlc3QifSx7ImxhdCI6MTkuMDE3Nzk4OSwibG9uIjo3Mi44NDc4MTE5OTk5OTk5OSwicGxhY2VJZCI6IkNoSUpEODJnRHR2TzV6c1IwRnVaT1ZCR2lrSSIsInBsYWNlTmFtZSI6IkRhZGFyIn1d&radius=2.0&city=mumbai&locality=Thane%20West,Borivali%20West,Dadar',
        'bangalore': 'https://www.nobroker.in/property/sale/bangalore/multiple?searchParam=W3sibGF0IjoxMi45OTY2MDg3LCJsb24iOjc3LjU0NTQ2MiwicGxhY2VJZCI6IkNoSUpEOUE3MUpBOXJqc1JOeWdnZFU4cDdmWSIsInBsYWNlTmFtZSI6IkluZGlyYW5hZ2FyIn0seyJsYXQiOjEzLjAwNTQxMDQsImxvbiI6NzcuNTM3NTc5NCwicGxhY2VJZCI6IkNoSUpvZThQWDU4OXJqc1JUY1VDNHQ1elRkSSIsInBsYWNlTmFtZSI6Ik1hcnV0aGkgTmFnYXIifSx7ImxhdCI6MTIuOTEyMTE4MSwibG9uIjo3Ny42NDQ1NTQ4LCJwbGFjZUlkIjoiQ2hJSnpXN2N2NUVVcmpzUmVjajdPWVJ4TXZJIiwicGxhY2VOYW1lIjoiSFNSIExheW91dCJ9XQ==&radius=2.0&city=bangalore&locality=Indiranagar,Maruthi%20Nagar,HSR%20Layout',
        'chennai': 'https://www.nobroker.in/property/sale/chennai/multiple?searchParam=W3sibGF0IjoxMi45MjA0NDkxLCJsb24iOjgwLjIwOTgyMTksInBsYWNlSWQiOiJDaElKZVl6bGVaaGRVam9SM21pTk1GaTBNalkiLCJwbGFjZU5hbWUiOiJDaGVubmFpIFNvdXRoIiwic2hvd01hcCI6ZmFsc2V9LHsibGF0IjoxMy4wODYwNTQ1LCJsb24iOjgwLjI5MjIzMzA5OTk5OTk5LCJwbGFjZUlkIjoiQ2hJSk9acElUa3R2VWpvUlJ6STBORTY1NkRvIiwicGxhY2VOYW1lIjoiQ2hlbm5haSBQb3J0IFRydXN0Iiwic2hvd01hcCI6ZmFsc2V9LHsibGF0IjoxMy4wOTY4NTcxLCJsb24iOjgwLjI4NjUzNTMsInBsYWNlSWQiOiJDaElKcjNKRG4xQnZVam9SUHdDQW0tQm5UN0kiLCJwbGFjZU5hbWUiOiJHZW9yZ2UgVG93biIsInNob3dNYXAiOmZhbHNlfV0=&radius=2.0&city=chennai&locality=Chennai%20South&isMetro=false',
        'delhi': 'https://www.nobroker.in/property/sale/delhi/multiple?searchParam=W3sibGF0IjoyOC43MTczMDkxLCJsb24iOjc3LjE3MTM0MzEsInBsYWNlSWQiOiJDaElKa2ROcHNvd0JEVGtSRTQ0ZVNPbjlMY00iLCJwbGFjZU5hbWUiOiJJbmRpcmEgTmFnYXIifSx7ImxhdCI6MjguNzE0Njk1OSwibG9uIjo3Ny4xNzcwNDYxLCJwbGFjZUlkIjoiQ2hJSlZaTnF4eDhDRFRrUnZSOGtsTHFXYnlFIiwicGxhY2VOYW1lIjoiQXphZHB1ciJ9LHsibGF0IjoyOC43Mjk2MTcxLCJsb24iOjc3LjE2NjYzMTI5OTk5OTk5LCJwbGFjZUlkIjoiQ2hJSlRhcmVHdW9CRFRrUkxBckFiLXdLMzJvIiwicGxhY2VOYW1lIjoiSmFoYW5naXJwdXJpIn1d&radius=2.0&city=delhi&locality=Indira%20Nagar,Azadpur,Jahangirpuri',
        'gurgaon': 'https://www.nobroker.in/property/sale/gurgaon/multiple?searchParam=W3sibGF0IjoyOC40Nzk1NywibG9uIjo3Ny4wODAwNiwicGxhY2VJZCI6IkNoSUpyWW9WRXlJWkRUa1JjbU00X3JSb19PRSIsInBsYWNlTmFtZSI6Ik1HIFJvYWQifSx7ImxhdCI6MjguMzkzNTkwOSwibG9uIjo3Ni45NDg0NTYxLCJwbGFjZUlkIjoiQ2hJSko2T0xYNVk5RFRrUm5zaGJRazZYLW1NIiwicGxhY2VOYW1lIjoiTmV3IEd1cmdhb24ifV0=&radius=2.0&city=gurgaon&locality=MG%20Road,New%20Gurgaon',
        'hyderabad': 'https://www.nobroker.in/property/sale/hyderabad/multiple?searchParam=W3sibGF0IjoxNy40NDAwODAyLCJsb24iOjc4LjM0ODkxNjgsInBsYWNlSWQiOiJDaElKMzg3ZWRxS1R5enNSNGtTVGI1N25FaXciLCJwbGFjZU5hbWUiOiJHYWNoaWJvd2xpIn0seyJsYXQiOjE3LjQ0MzQ2NDYsImxvbiI6NzguMzc3MTk1MywicGxhY2VJZCI6IkNoSUozMmxkak55VHl6c1I3cUJfVmV1TGFCayIsInBsYWNlTmFtZSI6IkhJVEVDIENpdHkifSx7ImxhdCI6MTcuNDY5ODU3NywibG9uIjo3OC4zNTc4MjQ2LCJwbGFjZUlkIjoiQ2hJSmE2TkpLTW1UeXpzUi1oSlZrRFRBRGQ0IiwicGxhY2VOYW1lIjoiS29uZGFwdXIifV0=&radius=2.0&city=hyderabad&locality=Gachibowli,HITEC%20City,Kondapur',
        'noida': 'https://www.nobroker.in/property/sale/noida/multiple?searchParam=W3sibGF0IjoyOC40MjIzMjI1LCJsb24iOjc3LjQ5MDI3MjYsInBsYWNlSWQiOiJDaElKaGVEWDlwdkJERGtSbnlMOUhqWXJXNDQiLCJwbGFjZU5hbWUiOiJTZWN0b3IgMTUwIn0seyJsYXQiOjI4LjQzOTI3NCwibG9uIjo3Ny40ODIyMzE1LCJwbGFjZUlkIjoiQ2hJSkNUZ2djWTdCRERrUnJYb3ZHcXN1QnUwIiwicGxhY2VOYW1lIjoiU2VjdG9yIDE0OSJ9LHsibGF0IjoyOC40Mjc3MTY1LCJsb24iOjc3LjUxNDk2NjEsInBsYWNlSWQiOiJDaElKSzJna29hekJERGtSZDI3dUhIWEtveG8iLCJwbGFjZU5hbWUiOiJMaXR0bGUgTnVydHVyZSBTY2hvb2wgLSBHcmVhdGVyIE5vaWRhIn1d&radius=2.0&city=noida&locality=Sector%20150,Sector%20149,Little%20Nurture%20School%20-%20Greater%20Noida',
        'greater Noida': 'https://www.nobroker.in/property/sale/greater-noida/multiple?searchParam=W3sibGF0IjoyNy41NjQwNTY3LCJsb24iOjc3LjcwMTcwNTYsInBsYWNlSWQiOiJFaTlaWVcxMWJtRWdSWGh3Y21WemMzZGhlU0JNYVc1cklGSmtMQ0JWZEhSaGNpQlFjbUZrWlhOb0xDQkpibVJwWVNJdUtpd0tGQW9TQ1hmVkdsalljWE01RVM5MUdpOU1yMDc0RWhRS0Vnbm5FbEVIS201ek9SR05KbmZxaTl0TS1nIiwicGxhY2VOYW1lIjoiWWFtdW5hIEV4cHJlc3N3YXkgTGluayBSb2FkIn0seyJsYXQiOjI4LjQ2NTI1NTQsImxvbiI6NzcuNTEwOTI3OSwicGxhY2VJZCI6IkVqWlFZWEpwSUVOb2IzZHJMQ0JIY21WaGRHVnlJRTV2YVdSaExDQlZkSFJoY2lCUWNtRmtaWE5vSURJd01UTXhNQ3dnU1c1a2FXRWlMaW9zQ2hRS0Vna3IyOGJPMWNFTU9SR2tDcWpPb1BWZFZoSVVDaElKNzVyNHVHVHFERGtSTHBZWFU3dktET3ciLCJwbGFjZU5hbWUiOiJQYXJpIENob3drIn0seyJsYXQiOjI4LjQ3MTM4ODcsImxvbiI6NzcuNTA3NDgxMywicGxhY2VJZCI6IkVrbEJiSEJvWVNBeElFSnNiMk5ySUVFZ1VtUXNJRUpzYjJOcklFRXNJRUZzY0doaElFa3NJRWR5WldGMFpYSWdUbTlwWkdFc0lGVjBkR0Z5SUZCeVlXUmxjMmdzSUVsdVpHbGhJaTRxTEFvVUNoSUpjU2ZFNFhqcUREa1JvR3VqMXB0RlNXSVNGQW9TQ1lfT2dnMTU2Z3c1RWJ6Qk9iSDg3eHdXIiwicGxhY2VOYW1lIjoiQWxwaGEgMSBCbG9jayBBIFJvYWQifV0=&radius=2.0&city=greater-noida&locality=Yamuna%20Expressway%20Link%20Road,Pari%20Chowk,Alpha%201%20Block%20A%20Road',
        'ghaziabad': 'https://www.nobroker.in/property/sale/ghaziabad/multiple?searchParam=W3sibGF0IjoyOC42NDYwMTc2LCJsb24iOjc3LjM2OTUxNjYsInBsYWNlSWQiOiJDaElKUFlReHJydjZERGtSOXloRkVIUjhoZlUiLCJwbGFjZU5hbWUiOiJJbmRpcmFwdXJhbSJ9LHsibGF0IjoyOC42NjIzNzU4LCJsb24iOjc3LjM3MzQ0LCJwbGFjZUlkIjoiQ2hJSkVZeFF3YUg2RERrUmRNTzlFUjQxUTkwIiwicGxhY2VOYW1lIjoiVmFzdW5kaGFyYSJ9LHsibGF0IjoyOC42NTA4MTIxLCJsb24iOjc3LjM3MDU2MTEsInBsYWNlSWQiOiJFbDVUYUdGcmRHa2dTMmhoYm1Rc0lGTm9ZV3QwYVNCTGFHRnVaQ0EwTENCSmJtUnBjbUZ3ZFhKaGJTd2dSMmhoZW1saFltRmtMQ0JIYUdGNmFXRmlZV1FnWkdsemRISnBZM1FzSUZWMGRHRnlJRkJ5WVdSbGMyZ3NJRWx1WkdsaElpNHFMQW9VQ2hJSjlWWEd0ckQ2RERrUkd1SnpoY2ZHN2RRU0ZBb1NDZU5mUWZHbC1ndzVFYTd3MjZ1OU94QXciLCJwbGFjZU5hbWUiOiJTaGFrdGkgS2hhbmQifV0=&radius=2.0&city=ghaziabad&locality=Indirapuram,Vasundhara,Shakti%20Khand',
        'faridabad': 'https://www.nobroker.in/property/sale/faridabad/multiple?searchParam=W3sibGF0IjoyOC40MjE0MzQ3LCJsb24iOjc3LjMzNDk3OTE5OTk5OTk5LCJwbGFjZUlkIjoiQ2hJSk8tYlB1dzdkRERrUmxlbVRXLVQyRkU0IiwicGxhY2VOYW1lIjoiTmVoYXJwYXIgRmFyaWRhYmFkIn0seyJsYXQiOjI4LjQxMzgwNDUsImxvbiI6NzcuMzIyMzkxNSwicGxhY2VJZCI6IkNoSUpoNGwxNDYzZEREa1I5eVl4TXNjdGp6dyIsInBsYWNlTmFtZSI6IlNlY3RvciAxNiJ9LHsibGF0IjoyOC40MjIxMTk0LCJsb24iOjc3LjMyNTczNTksInBsYWNlSWQiOiJDaElKbVNZdHBIUGRERGtSUUZSUF96NWdpdGMiLCJwbGFjZU5hbWUiOiJPbGQgRmFyaWRhYmFkIn1d&radius=2.0&city=faridabad&locality=Neharpar%20Faridabad,Sector%2016,Old%20Faridabad'
    }
    if location in location_url_map:
        return location_url_map[location]
    
async def get_soup_data(location):
    try:
        driver = webdriver.Chrome()  # Ensure the ChromeDriver is in your PATH
        city = location
        url = await get_url(city)
        driver.get(url)

        SCROLL_PAUSE_TIME = 2
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        driver.quit()

        return soup
    except Exception as e:
        print(f"Error fetching gold value: {str(e)}")

async def extract_property_details(location):
    try:
        properties = []
        soup = get_soup_data(location)
        property_articles = soup.find_all('article', {'aria-label': 'article'})
        for article in property_articles:
            try:
                title_tag = article.find('span', {'itemprop': 'description'})
                title = title_tag.get('title') if title_tag else 'N/A'
                
                price_tag = article.find('span', {'itemprop': 'price'})
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                area_tag = article.find('div', {'class': 'heading-7 flex'})
                area = area_tag.text.strip() if area_tag else 'N/A'
                
                address_tag = article.find('div', class_='mt-0.5p overflow-hidden overflow-ellipsis whitespace-nowrap max-w-70 text-gray-light leading-4 po:mb-0.1p po:max-w-95')
                address = address_tag.text.strip() if address_tag else 'N/A'
                
                latitude_tag = article.find('meta', {'itemprop': 'latitude'})
                latitude = latitude_tag.get('content') if latitude_tag else 'N/A'
                
                longitude_tag = article.find('meta', {'itemprop': 'longitude'})
                longitude = longitude_tag.get('content') if longitude_tag else 'N/A'
                
                builtup_tag = article.find('div', id='unitCode')
                builtup = builtup_tag.text.strip() if builtup_tag else 'N/A'
                
                emi_tag = article.find('div', id='roomType')
                emi = emi_tag.text.strip() if emi_tag else 'N/A'
                
                details = {
                    'title': title,
                    'price': price,
                    'area': area,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'builtup': builtup,
                    'estimated_emi': emi
                }
                properties.append(details)
            except AttributeError:
                continue
        return properties
    
    except Exception as e:
        print(f"Error fetching gold value: {str(e)}")


async def extract_bhk(title):
    match = re.search(r'(\d+)\s+BHK', title)
    return int(match.group(1)) if match else None

async def remove_bhk_from_title(title):
    return re.sub(r'\d+\s+BHK\s*', '', title).strip()

async def extract_location(title):
    parts = re.split(r'\s{2,}', title)
    return parts[1] if len(parts) > 1 else title

async def preprocessing(location):
    try:
        property_details = await extract_property_details(location)
        df = pd.DataFrame(property_details)

        df['title'] = df['title'].replace('For Sale  In', '', regex=True)
        df['title'] = df['title'].replace('Flat In ', '', regex=True)
        df['title'] = df['title'].replace('In ', '', regex=True)
        df['title'] = df['title'].replace('Flat In ', '', regex=True)
        df['title'] = df['title'].replace('House ', '', regex=True)
        df['title'] = df['title'].replace('Flat ', '', regex=True)

        df['bhk'] = df['title'].apply(await extract_bhk)
        df['title'] = df['title'].apply(await remove_bhk_from_title)

        df['location'] = df['title'].apply(extract_location)

        df['title'] = df['title'].replace(f'{df['location']}', '', regex=True)

        df['location'] = df['location'].replace(' East', '', regex=True)
        df['location'] = df['location'].replace(' West', '', regex=True)

        df['area'] = df['area'].replace('₹', '', regex=True)
        df['area'] = df['area'].replace(' per sq.ft.', '', regex=True)
        df['area'] = df['area'].replace(',', '', regex=True)

        df['builtup'] = df['builtup'].replace(' sqft', '', regex=True)
        df['builtup'] = df['builtup'].replace(',', '', regex=True)

        df['estimated_emi'] = df['estimated_emi'].replace('₹', '', regex=True)
        df['estimated_emi'] = df['estimated_emi'].replace('/Month', '', regex=True)
        df['estimated_emi'] = df['estimated_emi'].replace(' Lacs', '', regex=True)
        df['estimated_emi'] = df['estimated_emi'].replace(',', '', regex=True)

        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['area'] = pd.to_numeric(df['area'], errors='coerce')
        df['builtup'] = pd.to_numeric(df['builtup'], errors='coerce')
        df['bhk'] = pd.to_numeric(df['bhk'], errors='coerce')
        df['estimated_emi'] = pd.to_numeric(df['estimated_emi'], errors='coerce')

        return df

    except Exception as e:
        print(f"Error fetching gold value: {str(e)}")

async def calculate_inflated_price(current_price, rate, years):
    return current_price * (1 + rate) ** years
    
async def get_top_properties(location, average_cpi, years):
    try:
        df = await preprocessing(location)
        df['goal_price'] = df['price'].apply(await calculate_inflated_price, args=(average_cpi, years))
        df['goal_price'] = df['goal_price'].map('{:,.2f}'.format)
        df['goal_price'] = df['goal_price'].replace(',', '', regex=True)
        df['goal_price'] = pd.to_numeric(df['goal_price'])
        df['profit'] = df['goal_price'] - df['price']
        df['profit_percentage'] = (df['profit'] / df['price']) * 100
        df_sorted_25 = df.sort_values(by='profit_percentage', ascending=False).head(25)
        return df_sorted_25
    except Exception as e:
        print(f"Error fetching gold value: {str(e)}")

async def property_json(location, average_cpi, years):
    try:
        df_top_25 = await get_top_properties(location, average_cpi, years)
        properties_list = df_top_25.to_dict(orient='records')
        properties = json.dumps(properties_list, indent=2)
        return properties
    except Exception as e:
        print(f"Error fetching gold value: {str(e)}")