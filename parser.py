import pandas as pd
from Transaction import Transaction
from Categories import Categories
from Month import Month
from pymongo import MongoClient
from keywords import keywords
import time
from mongostring import mongostring

client = MongoClient(mongostring, retryWrites=False)
db = client.moneymanager
db_transactions = db.transactions
db_months = db.months

# configure the date parser for european format (date first)
mydateparser = lambda x: pd.to_datetime(x, dayfirst=True)

# read the csv file with all transactions
df = pd.read_csv("./umsaetze5.csv", sep=";", decimal=",", parse_dates=['Buchungstag', 'Wertstellung'], date_parser=mydateparser)
number_of_rows = len(df.index)
parsed_transacts = 0

# group all transactions by year and init a dictonary with one entry per year
years = {n: g.reset_index() for n, g in  df.groupby(pd.Grouper(key='Buchungstag', freq='Y'))}

# iterate over all the years
for key, year in years.items():

    # group all transactions in the current year by month
    months = {n: g.reset_index() for n, g in  year.groupby(pd.Grouper(key='Buchungstag', freq='M'))}

    # iterate over all the months
    for key, month in months.items():
        months_transactions = []                                                    # move to analyzer
        months_savings = 0                                                          # move to analyzer
        totalSpendings = 0                                                          # move to analyzer

        # iterate over every transaction and parse it into a proper Transaction object
        for idx, trans in month.iterrows():
            if 0 < ((parsed_transacts / number_of_rows) * 100) % 10 < 1:
                print("currently at", ((parsed_transacts / number_of_rows) * 100), "percent")

            current_trans = Transaction(trans['Buchungstag'], trans['Buchungstext'], trans['Betrag'], trans['Währung'])

            if "ANLEGEN" in current_trans.descr:
                current_trans.isSavings = True
                months_savings += 0 - current_trans.amount # move to analyzer
            
            if "PayPal" in current_trans.descr or "Auszahlung" in current_trans.descr:
                current_trans.toBeReviewed = True

            if current_trans.amount < 0 and not "ANLEGEN" in current_trans.descr:   # move to analyzer
                totalSpendings += current_trans.amount                              # move to analyzer

            db_transactions.insert_one(current_trans.__dict__)
            parsed_transacts += 1
            
            months_transactions.append(current_trans)                               # move to analyzer
        
        # add all the transactions to the current month of the current year
        current_month = Month(key.year, key.month, months_savings, totalSpendings, months_transactions)  # move to analyzer
        db_months.insert_one(current_month.__dict__)                                                     # move to analyzer
