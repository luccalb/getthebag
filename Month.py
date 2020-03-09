class Month:
  def __init__ (self, year, month, savings, totalSpendings, transacts):
      self.year = year
      self.month = month
      self.savings = savings
      self.totalSpendings = totalSpendings
      self.balance = self.calcBalance(transacts)


  def calcBalance(self, transacts):
    balance = 0
    for trans in transacts:
        if not trans.isSavings:
            balance += trans.amount
    return balance