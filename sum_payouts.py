import csv
import datetime
from dateutil.parser import parse
from decimal import Decimal
import glob
import sys


# EXCHANGE_RATE = Decimal('1.3269')  # 2019
# EXCHANGE_RATE = Decimal('1.3415')  # 2020
# EXCHANGE_RATE = Decimal('1.2535')  # 2021
# EXCHANGE_RATE = Decimal('1.3013')  # 2022
# EXCHANGE_RATE = Decimal('1.3497')  # 2023
EXCHANGE_RATE = Decimal('1.3698')  # 2024


def main():
    filename = '{}/FX_RATES_DAILY-sd-2017-01-03.csv'.format(sys.argv[1])
    xchange_rates = {}

    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            x_date = parse(row['date'])
            x_rate = Decimal(row['FXUSDCAD'])
            # print(x_date, x_rate)
            xchange_rates[x_date] = x_rate
            
    file_path = '{}/*2024-01_2024-12.csv'.format(sys.argv[1])

    us_sum = Decimal('0')
    cad_sum = Decimal('0')
    for filename in glob.glob(file_path):
        print(filename)
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                p_date = parse(row['Payout Date'])
                while p_date not in xchange_rates:
                    p_date = p_date + datetime.timedelta(days=1)
                amount = Decimal(row['Payout Amount'])
                cad_amount = amount * xchange_rates[p_date]
                us_sum += amount
                cad_sum += cad_amount

    cad = us_sum * EXCHANGE_RATE
    results = '{} USD, {} CAD (annualized), {} CAD (daily)'.format(us_sum, cad, cad_sum)
    print(results)


if __name__ == "__main__":
    main()


"""
data/Arc_Codementor_Payout_Histories_2021-01_2021-12.csv
44651.51 USD, 55970.667785 CAD

data/Arc_Codementor_Payout_Histories_2022-01_2022-12.csv
45597.24 USD, 59335.688412 CAD

data/Arc_Codementor_Payout_Histories_2023-01_2023-12.csv
15077.96 USD, 20350.722612 CAD

data/Arc_Codementor_Payout_Histories_2024-01_2024-12.csv
12047.08 USD, 16502.090184 CAD
89882.140184 CAD


I tried reading the penalty calculation page for revenue canada and I have no idea what math they are doing.
I do have a lot of unused rrsp contribution room, and if I use some or all of that I should be able to bring my taxes down fairly low.
Surely they can only charge me interest on the actual tax I owe, not the amount they estimated based on last year?
I will say they could make this a lot more fucking obvious.
There is a line on the 2023 return, in the summary, that shows installments due in the coming year.
It is buried in a tiny paragraph at the end of page 3 in my 6 page notice of assessment. 
I feel like something that important should maybe be up top, in bigger font.
Especially when it's a change from the previous year.
I have gotten all notices by email for years, but in this case I wish it had been paper mail. I would have seen that.
I did have notice reminders, unopened in my inbox when I searched. I can't explain why I never saw them 😦
But I saw literally none of them, so maybe they were being filtered somehow.
"""