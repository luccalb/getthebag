class Transaction:
  def __init__(self, date, descr, amount, currency):
    self.date = date
    self.descr = descr
    self.amount = amount
    self.currency = currency
    self.isSavings = False
    self.isSplit = False
    self.toBeReviewed = False
    self.subTrans = []
