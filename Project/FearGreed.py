import requests
import json
import pandas as pd
import statistics
import datetime 
import csv
import os
import collections

#Setting working directory to file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Creating empty dictionaries
FearGreed = {}
BitcoinPrice = {}
SalesBuy = {}
SalesSell = {}
Fees = {}

#Getting fear/greed values
#https://api.alternative.me/fng/?date_format=world&limit=0
def ImportFearGreed(data):
    for row in data['data']:
        predate = datetime.datetime.strptime(row['timestamp'], "%d-%m-%Y")
        date = predate.strftime("%Y-%m-%d")
        FearGreed[date] = int(row['value'])

try:
    with open("Data/FearGreed.json") as file:
        ImportFearGreed(json.load(file))
        print("Loaded from file")
except:    
    response = requests.get("https://api.alternative.me/fng/?date_format=world&limit=0")
    ImportFearGreed(response.json())
    print("Data reloaded from API")

#Getting historical btc values
#https://www.kaggle.com/datasets/mixmore/bitcoin-historical-data
#As the fear/greed is updated at 1am UK time, the open time is used
with open("Data/BTC-USD.csv") as file:
    reader = csv.reader(file, delimiter=",")
    line_count = 0
    for row in reader:
        if line_count == 0:
            line_count += 1
        else:
            BitcoinPrice[row[0]] = float(row[1])

def FearGreedEvalAmount(Amount, Fee):
    print("Evaluating index with $" + str(Amount))
    MinDate = datetime.datetime.strptime(min(FearGreed), "%Y-%m-%d")
    MaxDate = datetime.datetime.strptime(max(FearGreed), "%Y-%m-%d")
    Delta = datetime.timedelta(days=1)
    Profits = {}
    BuyTimes = {}
    SellTimes = {}
    TransFees = {}
    
    ProfitsGrid = [[] for x in range(100)]
    
    for Buy in range (100):
        for Sell in range (100):
            Hold = 0
            Wallet = Amount
            HoldAmount = 0
            StartDate = datetime.date(int(MinDate.strftime("%Y")),int(MinDate.strftime("%m")),int(MinDate.strftime("%d")))
            EndDate = datetime.date(int(MaxDate.strftime("%Y")),int(MaxDate.strftime("%m")),int(MaxDate.strftime("%d")))
            if Buy <= Sell:
                break
            else:
                Profits[str(Buy) + "-" + str(Sell)] = float(0.00)
                
                while (StartDate < EndDate):
                    if(Buy >= Sell):
                        try:
                            if Hold == 0 and Buy <= FearGreed[str(StartDate)]:
                                #Buy if it is over/equal to buy value
                                Profits[str(Buy) + "-" + str(Sell)] -= Wallet*(1-Fee)
                                BuyTimes[str(StartDate)] = [BitcoinPrice[str(StartDate)], Wallet, Wallet*(1-Fee), Wallet*Fee]
                                HoldAmount = Wallet*(1-Fee)/BitcoinPrice[str(StartDate)]
                                TransFees[str(StartDate)] = Wallet*Fee
                                Wallet = 0
                                Hold = 1
                            elif Hold == 1 and Sell >= FearGreed[str(StartDate)]:
                                #Sell if it is over/equal to sell value
                                Profits[str(Buy) + "-" + str(Sell)] += (HoldAmount*BitcoinPrice[str(StartDate)])*(1-Fee)
                                SellTimes[str(StartDate)] = [BitcoinPrice[str(StartDate)], HoldAmount*BitcoinPrice[str(StartDate)], (HoldAmount*BitcoinPrice[str(StartDate)])*(1-Fee), (HoldAmount*BitcoinPrice[str(StartDate)])*Fee]
                                Wallet = (HoldAmount*BitcoinPrice[str(StartDate)])*(1-Fee)
                                TransFees[str(StartDate)] = (HoldAmount*BitcoinPrice[str(StartDate)])*Fee
                                HoldAmount = 0
                                Hold = 0
                            StartDate += Delta
                        except:
                            StartDate += Delta
                        if StartDate == EndDate and Hold == 1:
                            #Sell if it is the last day
                            Profits[str(Buy) + "-" + str(Sell)] += (HoldAmount*BitcoinPrice[str(StartDate)])*(1-Fee)
                            SellTimes[str(StartDate)] = [BitcoinPrice[str(StartDate)], HoldAmount*BitcoinPrice[str(StartDate)], (HoldAmount*BitcoinPrice[str(StartDate)])*(1-Fee), (HoldAmount*BitcoinPrice[str(StartDate)])*Fee]
                            Wallet = 0
                            TransFees[str(StartDate)] = (HoldAmount*BitcoinPrice[str(StartDate)])*Fee
                            HoldAmount = 0
                            Hold = 0
            if StartDate == EndDate and not BuyTimes:
                Profits[str(Buy) + "-" + str(Sell)] = 0
            SalesBuy[str(Buy) + "-" + str(Sell)] = BuyTimes
            SalesSell[str(Buy) + "-" + str(Sell)] = SellTimes
            Fees[str(Buy) + "-" + str(Sell)] = TransFees
            ProfitsGrid[Buy].append(Profits[str(Buy) + "-" + str(Sell)])
            BuyTimes = {}
            SellTimes = {}
            TransFees = {}
    return(Profits, ProfitsGrid)

def HODL():
    MinDate = datetime.datetime.strptime(min(FearGreed), "%Y-%m-%d")
    MaxDate = datetime.datetime.strptime(max(FearGreed), "%Y-%m-%d")
    Delta = datetime.timedelta(days=1)
    Profits = pd.DataFrame(columns=["Date","Profit"])
    row = {"Date":2,"Profit":3}
    for HODLNum in range (100):
        Hold = 0
        HoldAmount = 0
        Sale = ""
        row = {}
        StartDate = datetime.date(int(MinDate.strftime("%Y")),int(MinDate.strftime("%m")),int(MinDate.strftime("%d")))
        EndDate = datetime.date(int(MaxDate.strftime("%Y")),int(MaxDate.strftime("%m")),int(MaxDate.strftime("%d")))
        while (StartDate <= EndDate):
            try:
                if(HODLNum >= FearGreed[str(StartDate)] and Hold == 0):
                    HoldAmount = 990/BitcoinPrice[str(StartDate)]
                    Hold = 1
                    Sale = str(StartDate)
                if StartDate == EndDate and Hold == 1:
                    row = {"Date":Sale,"Profit":(HoldAmount * BitcoinPrice[str(StartDate)]) * 0.99 - 1000}
                    Profits = pd.concat([Profits, pd.DataFrame(row, index=[HODLNum])])
            except:
                pass
            StartDate += Delta
    return(Profits)
        
    

#Evaluating index  
Profits, ProfitsGrid = FearGreedEvalAmount(1000, 0.01)
print(max(Profits, key=Profits.get))
print("$" + str(Profits[max(Profits, key=Profits.get)]))
#print(str(Fees[max(Profits, key=Profits.get)]))
print(sum(Fees[max(Profits, key=Profits.get)].values()))
#print(SalesBuy[max(Profits, key=Profits.get)])
#print(SalesSell[max(Profits, key=Profits.get)])



#print(min(Profits, key=Profits.get))
#print("$" + str(Profits[min(Profits, key=Profits.get)]))
#print(str(Fees[min(Profits, key=Profits.get)]))
#print(SalesBuy[min(Profits, key=Profits.get)])
#print(SalesSell[min(Profits, key=Profits.get)])

#Export results
#Export = pd.DataFrame(ProfitsGrid)
#df = Export.melt(id_vars=[], value_vars=[], var_name="Y", value_name="Profit")
#Export.to_csv("Data/Profits.csv")

#Export Distribution of FG index
#FGAve = collections.Counter(FearGreed.values())
#FGAve = collections.OrderedDict(sorted(FGAve.items()))
#FGAve = pd.DataFrame(FGAve.items(), columns=['FG', 'Amount'])
#FGAve.to_csv("Data/FGDistribution.csv")

#Export FG data
#FearGreed = pd.DataFrame(FearGreed.items(), columns=['Date', 'FG'])
#FearGreed.to_csv("Data/FearGreed.csv")

#Export BTC price data
#BitcoinPrice = pd.DataFrame(BitcoinPrice.items(), columns=['Date', 'Price'])
#BitcoinPrice.to_csv("Data/BitcoinPrice.csv")

#HODl Test
#Profits = HODL()
#print(Profits)
#Profits.to_csv("Data/HODLFGIProfits.csv")