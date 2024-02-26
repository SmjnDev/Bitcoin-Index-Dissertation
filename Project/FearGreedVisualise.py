import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime 
import os

#File path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Import data
FGData = pd.read_csv('Data/ProfitsNormalised.csv')
#FGData["Value"] = FGData["Value"]-1000
FGDataRenamed = FGData.rename(columns={"Buy":"Buy Index Value","Sell":"Sell Index Value","Value":"Profit Generated ($)"}) 
FGDistribution = pd.read_csv('Data/FGDistribution.csv')
FGValues = pd.read_csv('Data/FearGreed.csv')
BTCPrice = pd.read_csv('Data/BitcoinPrice.csv')
BTCPriceFull = pd.read_csv('Data/BitcoinPriceFull.csv')

#Profit plot
fig = px.scatter(FGDataRenamed, x='Buy Index Value', y='Sell Index Value', color="Profit Generated ($)", color_continuous_scale=px.colors.sequential.Blackbody,
                 title="FGI Profit Generated After 5 Years From 1000 USD Investment<br><sup> 01/02/2018 - 08/04/2023 </sup>",
                 range_color=(-1000,10000))
fig.update_traces(marker_size=10, marker_symbol="square")
fig.update_layout(xaxis = dict(
    tickmode = "linear",
    tick0 = 0,
    dtick = 10,
    title="Sell Index Value",
    
), yaxis = dict(
    tickmode = "linear",
    tick0 = 0,
    dtick = 10,
    title="Buy Index Value",
), coloraxis_colorbar_title="Profit Generated (USD)")
#fig.show()

#Concentrated profit plot
FGDataConc = FGData.drop(FGData[FGData["Buy"] < 35].index)
FGDataConc = FGDataConc.drop(FGDataConc[FGDataConc["Buy"] > 75].index)
FGDataConc = FGDataConc.drop(FGDataConc[FGDataConc["Sell"] < 20].index)
FGDataConc = FGDataConc.drop(FGDataConc[FGDataConc["Sell"] > 45].index)
FGDataConc = FGDataConc.rename(columns={"Buy":"Buy Index Value","Sell":"Sell Index Value","Value":"Profit Generated ($)"}) 
fig5 = px.scatter(FGDataConc, x='Buy Index Value', y='Sell Index Value', color="Profit Generated ($)", color_continuous_scale=px.colors.sequential.Blackbody,
                 title="Concentrated FGI Profit Generated After 5 Years From 1000 USD Investment<br><sup> 01/02/2018 - 08/04/2023 </sup>",
                 range_color=(-1000,10000))
fig5.update_traces(marker_size=15, marker_symbol="square")
fig5.update_layout(xaxis = dict(
    tickmode = "linear",
    tick0 = 0,
    dtick = 10,
    title="Sell Index Value",
), yaxis = dict(
    tickmode = "linear",
    tick0 = 0,
    dtick = 10,
    title="Buy Index Value",
), coloraxis_colorbar_title="Profit Generated (USD)")
#fig5.show()

#Profit by buy value
FGData["BarX"] = FGData["Buy"].astype(str) + "-" + FGData["Sell"].astype(str)
fig2 = px.bar(FGData, x="Buy", y="Value", color="Value", title="Fear/Greed Overall Profitability Per Sell Index Value<br><sup> 01/02/2018 - 08/04/2023 </sup>", labels={"Buy":"Buy Index Value", "Value":"Overall Profit Generated ($)"})
fig2.layout.update(showlegend=False)
#fig2.show()

#Profit by sell value
fig3 = px.bar(FGData, x="Sell", y="Value", color="Value", title="Fear/Greed Overall Profitability Per Buy Index Value<br><sup> 01/02/2018 - 08/04/2023 </sup>", labels={"Buy":"Buy Index Value", "Value":"Overall Profit Generated ($)"})
fig3.layout.update(showlegend=False)
#fig3.show()

#Profit area chart
BarData = FGData.sort_values(["Value"])
BarData = BarData.reset_index()
fig4 = px.area(BarData, x=BarData.index, y="Value",
               title="FGI Profit Generated After 5 Years From 1000 USD Investment<br><sup>Sorted From Lowest To Highest Profit: 01/02/2018 - 08/04/2023 </sup>")
fig4.update_layout(xaxis=dict(tickmode = "linear", tick0 = 0, dtick = 500),
                   xaxis_title="FGI Pair Count", yaxis_title="Profit Generated (USD)",
                   yaxis_range=[-1000,10000])
fig4.add_hline(y=0, line_width=3, line_dash="longdash", line_color="red",
               annotation_text="<b>    Break-even</b>", annotation_position="top left")
fig4.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
#fig4.show()

#Overall profit percentage
ProfitAmount = {"Type": ["Profit","Loss"],"Amount": [len(FGData[FGData["Value"] > 0]),len(FGData[FGData["Value"] <= 0])]}
ProfitAmount = pd.DataFrame(data=ProfitAmount)
fig6 = px.pie(ProfitAmount, values="Amount", names="Type", color="Type",
              color_discrete_map={"Profit":"lime","Loss":"crimson"}, title="Overall Fear/Greed Index Pairs In Profit")
#fig6.show()

#Average profit per buy/sell value
BuyProfit = pd.DataFrame(FGData.groupby(["Buy"])["Value"].mean())
fig7 = px.bar(BuyProfit, x=BuyProfit.index, y="Value", title="Fear/Greed Average Profit Per Sell Index Value<br><sup> 01/02/2018 - 08/04/2023 </sup>", labels={"Buy":"Buy Index Value", "Value":"Average Profit Generated ($)"})
fig7.update_layout(xaxis=dict(title="Sell Index Value"),yaxis=dict(title="Average Profit Generated (USD)"))
fig7.update_xaxes(range=[0, 100])
#fig7.show()

SellProfit = pd.DataFrame(FGData.groupby(["Sell"])["Value"].mean())
fig8 = px.bar(SellProfit, x=SellProfit.index, y="Value", title="Fear/Greed Average Profit Per Buy Index Value<br><sup> 01/02/2018 - 08/04/2023 </sup>", labels={"Sell":"Sell Index Value", "Value":"Average Profit Generated ($)"})
fig8.update_layout(xaxis=dict(title="Buy Index Value"),yaxis=dict(title="Average Profit Generated (USD)"))
fig8.update_xaxes(range=[0, 100])
#fig8.show()

#Distribution of fear/greed index values
#print(FGDistribution)
fig9 = px.bar(FGDistribution, x="FG", y="Amount", title="Count Of Fear/Greed Index Occurance Between 01/02/2018 - 08/04/2023", labels={"FG":"Fear/Greed Index Value", "Amount":"Amount Of Times Occurred"})
#fig9.show()

#FG index over time (2022)
#print(FGValues)
BTCPrice2022 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2019-01-01"].index)
BTCPrice2022 = BTCPrice2022.drop(BTCPrice2022[BTCPrice2022["Date"] < "2018-02-01"].index)
FGValues2022 = FGValues.drop(FGValues[FGValues["Date"] >= "2019-01-01"].index)
FGValues2022 = FGValues2022.drop(FGValues2022[FGValues2022["Date"] < "2018-02-01"].index)
fig10 = go.Figure()
fig10.add_trace(go.Scatter(x=BTCPrice2022["Date"], y=BTCPrice2022["Price"], yaxis="y"))
fig10.add_trace(go.Scatter(x=FGValues2022["Date"], y=FGValues2022["FG"], yaxis="y2"))
fig10.data[-1].name = "Bitcoin Price"
fig10.data[-2].name = "Fear/Greed Index"
fig10.update_layout(yaxis=dict(
    title="Bitcoin Price ($)", side="left"),
    yaxis2=dict(title="Fear/Greed Index Value", overlaying="y",
                side="right", range = [0,100]),
    xaxis=dict(title="Date"),
    legend=dict(x=1.1),
    title="Correlation Between Bitcoin Price and Fear/Greed Index Value In 2018")
#fig10.show()

#Average BTC price depending on fear/greed values
FGBTC = pd.merge(FGValues, BTCPrice, on="Date")
FGBTCAve = pd.DataFrame(FGBTC.groupby(["FG"])["Price"].mean())
fig11 = px.bar(FGBTCAve, x=FGBTCAve.index, y="Price", title="Average Bitcoin Price Per Fear/Greed Index Value")
fig11.update_layout(yaxis=dict(title="Bitcoin Price ($)"),
                    xaxis=dict(title="Fear/Greed Index Value", range = [0,100]))
#fig11.show()

#Highest and lowest fear/greed index values

#Fear/Greed over years
BTCPriceTimeLim = FGBTC.drop(FGBTC[FGBTC["Date"] >= "2022-01-01"].index)
BTCPriceTimeLim = BTCPriceTimeLim.drop(BTCPriceTimeLim[BTCPriceTimeLim["Date"] < "2020-01-01"].index)
fig13 = px.line(BTCPriceTimeLim, x="Date", y="FG")
#fig13.show()

#Bitcoin price over years
FGTimeLim = FGBTC.drop(FGBTC[FGBTC["Date"] >= "2022-01-01"].index)
FGTimeLim = BTCPriceTimeLim.drop(BTCPriceTimeLim[BTCPriceTimeLim["Date"] < "2020-01-01"].index)
fig14 = px.line(FGTimeLim, x="Date", y="Price")
#fig14.show()

#FGI HODL
FGHODLData = pd.read_csv('Data/HODLFGIProfits.csv')

#HODL FGI to Profit
fig15 = px.bar(FGHODLData, x="HODLFGI", y="Profit", title="HODL Profit Generated After 5 Years Using The Fear/Greed Index<br><sup> 01/02/2018 - 08/04/2023 </sup>", 
               color="Profit", color_continuous_scale=px.colors.sequential.Blues, range_color=(1000,3000))
fig15.update_layout(yaxis=dict(title="Profit Generated ($)"),
                    xaxis=dict(title="Fear/Greed Index Value"))
fig15.update_xaxes(range=[4.5, 95.5])
fig15.add_hline(x0=0, y=1673.05, line_width=3, line_dash="dot", line_color="rgb(170,207,229)",
               annotation_text="<b>$1673.05        </b>", annotation_position="top right")
fig15.add_hline(y=1993.22, line_width=3, line_dash="dot", line_color="rgb(108,175,214)",
               annotation_text="<b>$1993.22        </b>", annotation_position="top right")
fig15.add_hline(y=2308.71, line_width=3, line_dash="dot", line_color="rgb(58,138,194)",
               annotation_text="<b>$2308.71        </b>", annotation_position="top right")
fig15.add_hline(y=2880.58, line_width=3, line_dash="dot", line_color="rgb(8,64,130)",
               annotation_text="<b>$2880.58        </b>", annotation_position="top right")               
#fig15.show()

#Bitcoin price
fig16 = px.line(BTCPriceFull, x="Date", y="Open", title="Logarithmic Price History of Bitcoin <br><sup>01/01/2010 - 19/07/2023</sup>", log_y=True, range_y=[0.1,100000])
fig16.update_layout(yaxis=dict(title="Bitcoin Price ($)"),
                    xaxis=dict(title="Year",tickmode='array', tickvals=[2010,2011,
2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]))
fig16.update_xaxes(
    dtick="Y1",
    tickformat="%Y")
fig16.show()