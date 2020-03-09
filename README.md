# Get The Bag

an automated personal finance analysis tool  

## Brainstorm

1. get transaction list (csv file) from online banking (chromedriver?)
2. get latest transaction from db (mongodb?)
3. figure out the latest affected month and keep those transactions locally
4. parse all new transactions from csv to transaction object (panda?)
5. add all transactions to their respective month
6. start processing month by month
   1. sum up all income/expenses (excluding the ones marked as savings)
   2. split up transaction if needed (e.g. Paypal- or cash payments)
7. Output:
   1. Monthly balance
   2. Monthly Expenses divided in categories (Food, Rent, Mobile, ...)
   3. Yearly savings (so far)
8. Save all changes to the database

```python
class Transaction:
  def __init__(self, date, reason, amount, currency):
    self.date = date
    self.reason = reason
    self.amount = amount
    self.currency = currency
    self.isSavings = false
    self.isSplit = false
    self.subTrans = {}

class Month:
  def __init__ (self, transactions):
    self.transactions = transactions

  def calcBalance(self):
    # do magic (step 6)
    self.balance = 0
```
