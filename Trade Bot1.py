# region imports
from AlgorithmImports import *
# endregion

class PensiveLightBrownSalmon(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 8, 17)  # Set Start Date
        self.SetEndDate(2022, 8, 17)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash

        # self.AddEquity("BND", Resolution.Minute)
        spy = self.AddEquity("SPY", Resolution.Daily) # add the stock name you want to trade

        spy.SetDataNormalizationMode(DataNormalizationMode.Raw) # some thing with data normalization, not necessary, is already assigned a default value

        self.spy = spy.Symbol
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin) # the name of your broker will go here, to calculate its margin

        self.entryPrice = 0   # to track entry price
        self.period = timedelta(31) # 31days time period
        self.nextEntryTime = self.Time


    def OnData(self, data):
        if not self.spy in data:
            return 

        # they all do basically the same thing
        # price = data.Bars[self.spy].Close
        price = data[self.spy].Close
        # price = self.Securities[self.spy].Close

        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.spy, 1) # 1  means we want to allocate 100% of our portfolio
                # self.MarketOrder(self.spy, int(self.Portfolio.Cash / price))
                self.Log("BUY SPY @" + str(price)) #good for debugging, prints to the screen
                self.entryPrice = price
            elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
                self.Liquidate()
                self.Log("SELL SPY @" + str(price))
                self.nextEntryTime = self.Time + self.period

            
