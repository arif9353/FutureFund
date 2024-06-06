#FETCHING THE DATA FOR FRONTEND

async def get_bank_names_for_RD():
    try:
        bank_interest_data = {
            "sbi_bank": "6.5 - 7",
            "icici_bank": "4.75 - 7.20",
            "hdfc_bank": "4.50 - 7.25",
            "kotak_mahindra_bank": "6.00 - 7.40",
            "axis_bank": "5.75 - 7.20",
            "bank_of_baroda": "5.75 - 7.25",
            "punjab_national_bank": "6.00 - 7.25",
            "idbi_bank": "6.25 - 7.00",
            "canara_bank": "6.15 - 7.25",
            "union_bank_of_india": "5.75 - 6.50",
            "yes_bank": "6.10 - 7.75",
            "bandhan_bank": "4.50 - 7.85",
            "bank_of_maharashtra": "5.50 - 6.25",
            "indusind_bank": "7.00 - 7.75",
            "jammu_and_kashmir_bank": "5.75 - 7.10",
            "karnataka_bank": "5.80 - 7.40",
            "saraswat_bank": "7.00 - 7.50",
            "federal_bank": "5.75 - 7.50",
            "dbs_bank": "6.00 - 7.50",
            "rbl_bank": "5.00 - 8.00",
            "indian_bank": "4.50 - 7.25",
            "indian_overseas_bank": "5.75 - 7.30",
            "tmb_bank": "6.75 - 7.75"
        }
        return bank_interest_data
    except Exception as e:
        print(f"Error occured while trying to get bank names for recurrent deposit {str(e)}")
        return f"Error occured while trying to get bank names for recurrent deposit {str(e)}"


#CALCULATING RECURRENT DEPOSIT PROFIT AND OTHER ASPECTS 

async def calculate_rd_maturity(monthly_deposit, tenure_months, annual_interest_rate):
    try:
        total_principal = monthly_deposit * tenure_months
        quarterly_interest_rate = annual_interest_rate / 4 / 100
        quarters = tenure_months // 3
        maturity_amount = 0

        for i in range(1, tenure_months + 1):
            remaining_months = tenure_months - i + 1
            quarters_remaining = remaining_months // 3
            maturity_amount += monthly_deposit * (1 + quarterly_interest_rate) ** quarters_remaining

        profit = maturity_amount - total_principal
        answer=[]
        answer.append(maturity_amount)
        return maturity_amount, profit
    except Exception as e:
        print(f"error occurred in calculate_rd_maturity function: {str(e)}")


async def recurrent_deposit_give(investment_amount,years,bank,recurrent_deposit_main):
    try:
        if investment_amount>=100:
            tenure_months=None
            if years>10:
                tenure_months = 10*12
            else:
                tenure_months = years*12
            interest_rate = recurrent_deposit_main[bank]
            # Split the string to get the individual numbers
            rates = interest_rate.split(' - ')
            # Convert the split strings to float
            rate_min = float(rates[0])
            rate_max = float(rates[1])
            # Calculate the mean of the range
            annual_interest_rate = (rate_min + rate_max) / 2
            maturity_amount, profit = await calculate_rd_maturity(investment_amount, tenure_months, annual_interest_rate)

            answer = {
                "investment_amount":investment_amount,
                "maturity_amount": maturity_amount,
                "profit_amount": profit,
                "tenure_months":tenure_months,
                "interest_rate":annual_interest_rate
            }
            return answer
        else:
            return None
    except Exception as e:
        print(f"error while running recurrent_deposit_give function {str(e)}")