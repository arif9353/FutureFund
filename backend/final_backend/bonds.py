import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

#FETCHING BONDS DATA

async def estimate_face_value(bond_data):
    try:
        # Extract relevant details from the bond data
        coupon_rate = float(bond_data['coupon'].replace('%', '').strip()) / 100
        yield_rate = float(bond_data['yield'].replace('%', '').strip()) / 100
        maturity_date = datetime.strptime(bond_data['maturity'], '%b %Y')
        if maturity_date.year == 9999:
            print(f"Skipping bond {bond_data['name']} with maturity date of Dec 9999.")
            return None
        current_date = datetime.now()  # Use the current date
        price = float(bond_data['price'].replace('₹', '').replace(',', '').strip())
        frequency = bond_data['frequency']
        
        # Calculate the maturity period in years, including months
        maturity_period_years = (maturity_date - current_date).days / 365.25
        
        # Determine the number of payments per year based on the frequency
        if frequency == 'MONTHLY':
            payments_per_year = 12
        elif frequency == 'QUARTERLY':
            payments_per_year = 4
        elif frequency == 'SEMI ANNUAL':
            payments_per_year = 2
        elif frequency == 'CUMULATIVE AT MATURITY':
            payments_per_year = 1  # For cumulative bonds, we treat as a single payment at the end
        else:  # Assume ANNUALLY
            payments_per_year = 1
        
        # Calculate the total number of payments
        total_payments = payments_per_year * maturity_period_years
        
        # Calculate the yield per period
        yield_per_period = yield_rate / payments_per_year
        
        # Approximate the coupon payment per period
        coupon_payment_per_period = (coupon_rate / payments_per_year) * price
        
        # Calculate the face value
        face_value = coupon_payment_per_period * (1 - (1 + yield_per_period) ** -total_payments) / yield_per_period
        face_value += price / ((1 + yield_per_period) ** total_payments)
        
        return round(face_value, 2)
    except Exception as e:
        print(f"Error estimating face value for bond {bond_data['name']}: {e}")
        return None

async def calculate_bond_profit(bond_data, face_value):
    try:
        # Extract relevant details from the bond data
        name = bond_data['name']
        coupon_rate = float(bond_data['coupon'].replace('%', '').strip()) / 100
        maturity_date = datetime.strptime(bond_data['maturity'], '%b %Y')
        current_date = datetime.now()  # Use the current date
        price = float(bond_data['price'].replace('₹', '').replace(',', '').strip())
        frequency = bond_data['frequency']
        
        # Calculate the maturity period in years, including months
        maturity_period_years = (maturity_date - current_date).days / 365.25
        
        # Calculate the annual coupon payment
        annual_coupon_payment = coupon_rate * face_value
        
        # Determine the number of payments per year based on the frequency
        if frequency == 'MONTHLY':
            payments_per_year = 12
        elif frequency == 'QUARTERLY':
            payments_per_year = 4
        elif frequency == 'SEMI ANNUAL':
            payments_per_year = 2
        elif frequency == 'CUMULATIVE AT MATURITY':
            payments_per_year = 1  # For cumulative bonds, we treat as a single payment at the end
        else:  # Assume ANNUALLY
            payments_per_year = 1
        
        # Calculate the total number of payments
        total_payments = payments_per_year * maturity_period_years
        

        if frequency == 'CUMULATIVE AT MATURITY':
            total_coupon_payments = annual_coupon_payment * maturity_period_years  # Simplified for cumulative bonds
        else:
            monthly_coupon_payment = annual_coupon_payment / 12
            total_coupon_payments = monthly_coupon_payment * total_payments
        

        profit = total_coupon_payments - (price - face_value)
        
        return {
            "name": name,
            "coupon_rate": f"{coupon_rate * 100:.4f}%",
            "maturity": bond_data['maturity'],
            "yield": bond_data['yield'],
            "price": f"₹ {price:,.2f}",
            "frequency": frequency,
            "profit": f"₹ {profit:,.2f}"
        }
    except Exception as e:
        print(f"Error calculating profit for bond {bond_data['name']}: {e}")
        return None

async def get_bond_details(url1):
    try:
        response = requests.get(url1)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            bond_rows = soup.find_all('tr', class_='clickable-row')
            bonds = []
            
            for bond_row in bond_rows:
                bond_name = bond_row.find('p', class_='company-title-f-cata').text.strip()
                bond_coupon = bond_row.find_all('td', class_='table-data')[1].find('p').text.strip()
                bond_maturity = bond_row.find_all('td', class_='table-data')[2].find('p').text.strip()
                bond_frequency = bond_row.find_all('td', class_='table-data')[4].find('p').text.strip()
                bond_yield = bond_row.find_all('td', class_='table-data')[5].find('p').text.strip()
                bond_price_str = bond_row.find_all('td', class_='table-data')[6].find('p').text.strip()
                bond_price = float(bond_price_str.replace('₹', '').replace(',', '').strip())
                logo_div = bond_row.find('div', class_='company-logo-f-cata-table')
                style_attr = logo_div['style']
                match = re.search(r'url\(\s*(.*?)\s*\)', style_attr)
                logo_url = match.group(1) if match else None

                try:
                    float(bond_coupon.replace('%', '').strip())
                    maturity_date = datetime.strptime(bond_maturity, '%b %Y')
                    
                    if maturity_date.year == 9999:
                        print(f"Skipping bond {bond_name} with maturity date of Dec 9999.")
                        continue
                except ValueError:
                    print(f"Skipping bond {bond_name} due to invalid data.")
                    continue
                
                bond_details = {
                    'name': bond_name,
                    'coupon': bond_coupon,
                    'maturity': bond_maturity,
                    'yield': bond_yield,
                    'price': bond_price_str,
                    'frequency': bond_frequency,
                    'logo': logo_url
                }
                
                bonds.append(bond_details)
            
            bonds.sort(key=lambda x: (float(x['price'].replace('₹', '').replace(',', '').strip()), 
                                      -float(x['yield'].replace('%', '').strip())))
            
            return bonds
        else:
            return None
    except Exception as e:
        print(f"Error fetching bond details: {e}")
        return None

async def get_bonds_data(url):
    try:
        all_bond_details = await get_bond_details(url)
        if not all_bond_details:
            return json.dumps({"bonds": [], "success": False})
        
        final_answer = []
        for bond in all_bond_details:
            estimated_face_value = await estimate_face_value(bond)
            if estimated_face_value is None:
                continue
            bond_profit = await calculate_bond_profit(bond, estimated_face_value)
            if bond_profit is None:
                continue
            bond['estimated_face_value'] = estimated_face_value
            bond['bond_profit'] = bond_profit['profit']
            final_answer.append(bond)
        
        final_answer.sort(key=lambda x: float(x['bond_profit'].replace('₹', '').replace(',', '').strip()), reverse=True)
        answer = []
        answer.append(final_answer[:25])
        answer.append(final_answer)
        return answer
    except Exception as e:
        print(f"Error fetching bond details: {str(e)}")
        return f"Error fetching bond details: {str(e)}"


#SHORTLISTING BONDS AS PER THEIR AFFORDABILITY

async def shortlist_bonds(bond_data, max_price):
    try:
        shortlisted_bonds = []
        bond_price = None
        max = 0
        quantity = 0
        for bond in bond_data:
            if bond['frequency'] == 'QUARTERLY':
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/4
            elif bond['frequency'] == "SEMI ANNUALLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/6
            elif bond['frequency'] == "ANNUALLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/12
            elif bond['frequency'] == "MONTHLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))
            else:
                bond_price = 10000000000
            if bond_price <= max_price:
                curr_quantity = int(max_price/bond_price)
                if bond_price>=max:
                    max = bond_price
                    quantity = curr_quantity
                bond["quantity"] = curr_quantity
                shortlisted_bonds.append(bond)
        if not shortlisted_bonds:
            return None,None,None
        return shortlisted_bonds[:3],max,quantity
    except Exception as e:
        print(f"error occurred in shortlist_bonds fn {str(e)}")
