import pylab


class CreditShoper(object):
    def __init__(self, account_balance, interest_rate, price, repay, period):
        self.account_balance = account_balance
        self.interest_rate = interest_rate
        self.price = price
        self.repay = repay
        self.period = period
        self.itemsBought = 0
        self.itemsBoughtHistory = []
        self.accountBalanceHistory = []
    
    def buyProduct(self, price):
        self.account_balance -= price
        self.itemsBought +=1
    
    def countInterst(self, interest_rate):
        self.account_balance = self.account_balance * (1 + (interest_rate/float(12))/100)
        
    def getAccountBalance(self):
        return self.account_balance
    
    def getItemsBought(self):
        return self.itemsBought
    
    def payInstalment(self, repay):
        self.account_balance += repay
    
    def updateStep(self):
        for month in range(self.period):
            if self.account_balance >= 0:
                self.buyProduct(self.price)
            self.countInterst(self.interest_rate)
            self.itemsBoughtHistory.append(self.getItemsBought())
            self.accountBalanceHistory.append(self.getAccountBalance())
            self.payInstalment(self.repay)
        return self.itemsBoughtHistory, self.accountBalanceHistory
        
class SaveUpShoper(object):
    def __init__(self, account_balance, interest_rate, price, saving, period):
        self.account_balance = account_balance
        self.interest_rate = interest_rate
        self.price = price
        self.saving = saving
        self.period = period
        self.itemsBought = 0
        self.itemsBoughtHistory = []
        self.accountBalanceHistory = []
    
    def buyProduct(self, price):
        self.account_balance -= price
        self.itemsBought +=1
    
    def countInterst(self, interest_rate):
        self.account_balance = self.account_balance * (1 + (interest_rate/float(12))/100)
        
    def getAccountBalance(self):
        return self.account_balance
    
    def getItemsBought(self):
        return self.itemsBought
    
    def saveCash(self, saving):
        self.account_balance += saving
    
    def updateStep(self):
        for month in range(self.period):
            self.saveCash(self.saving)
            self.countInterst(self.interest_rate)
            if self.account_balance >= self.price:
                self.buyProduct(self.price)
            self.itemsBoughtHistory.append(self.getItemsBought())
            self.accountBalanceHistory.append(self.getAccountBalance())
        return self.itemsBoughtHistory, self.accountBalanceHistory

def showPlot1(title, x_label, y_label):
    creditshoper = CreditShoper(0, 10.47, 50000, 1062.95, 360)
    saveupshoper = SaveUpShoper(0, 3.0, 50000, 1062.95, 360)
    creditItems, creditBalance = creditshoper.updateStep()
    saveItems, saveBalance = saveupshoper.updateStep()
    
    pylab.plot(range(360), creditItems)
    pylab.plot(range(360), saveItems)
    pylab.title(title)
    #pylab.legend(('Items bought on credit', 'Items bought from savings'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

showPlot1('x', 'y', 'z')
