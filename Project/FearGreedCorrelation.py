import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os 

#File path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

FGValues = pd.read_csv('Data/FearGreed.csv')
BTCPrice = pd.read_csv('Data/BitcoinPrice.csv')

#BTC Price Change
BTCIncrease = {"2018":[((float(BTCPrice.loc[BTCPrice["Date"] == "2018-12-31", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2018-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2018-01-01", "Price"])*100],
               "2019":[((float(BTCPrice.loc[BTCPrice["Date"] == "2019-12-31", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2019-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2019-01-01", "Price"])*100],
               "2020":[((float(BTCPrice.loc[BTCPrice["Date"] == "2020-12-31", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2020-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2020-01-01", "Price"])*100],
               "2021":[((float(BTCPrice.loc[BTCPrice["Date"] == "2021-12-31", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2021-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2021-01-01", "Price"])*100],
               "2022":[((float(BTCPrice.loc[BTCPrice["Date"] == "2022-12-31", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2022-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2022-01-01", "Price"])*100],
               "2023":[((float(BTCPrice.loc[BTCPrice["Date"] == "2023-04-08", "Price"]))-float(BTCPrice.loc[BTCPrice["Date"] == "2023-01-01", "Price"]))/float(BTCPrice.loc[BTCPrice["Date"] == "2023-01-01", "Price"])*100]}
BTCIncrease = pd.DataFrame(BTCIncrease, index = ["Increase"])
BTCAverage = {}

#2018 Correlation
BTCPrice2018 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2019-01-01"].index)
BTCPrice2018 = BTCPrice2018.drop(BTCPrice2018[BTCPrice2018["Date"] < "2018-02-01"].index)
FGValues2018 = FGValues.drop(FGValues[FGValues["Date"] >= "2019-01-01"].index)
FGValues2018 = FGValues2018.drop(FGValues2018[FGValues2018["Date"] < "2018-02-01"].index)
BTCAverage.update({"2018":BTCPrice2018.loc[:,"Price"].mean()})

FGBTC2018 = pd.merge(FGValues2018, BTCPrice2018, on="Date")
FGBTC2018.drop(FGBTC2018.columns[FGBTC2018.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2018 = FGBTC2018.corr()

#2019 Correlation
BTCPrice2019 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2020-01-01"].index)
BTCPrice2019 = BTCPrice2019.drop(BTCPrice2019[BTCPrice2019["Date"] < "2019-01-01"].index)
FGValues2019 = FGValues.drop(FGValues[FGValues["Date"] >= "2020-01-01"].index)
FGValues2019 = FGValues2019.drop(FGValues2019[FGValues2019["Date"] < "2019-01-01"].index)
BTCAverage.update({"2019":BTCPrice2019.loc[:,"Price"].mean()})

FGBTC2019 = pd.merge(FGValues2019, BTCPrice2019, on="Date")
FGBTC2019.drop(FGBTC2019.columns[FGBTC2019.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2019 = FGBTC2019.corr()

#2020 Correlation
BTCPrice2020 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2021-01-01"].index)
BTCPrice2020 = BTCPrice2020.drop(BTCPrice2020[BTCPrice2020["Date"] < "2020-01-01"].index)
FGValues2020 = FGValues.drop(FGValues[FGValues["Date"] >= "2021-01-01"].index)
FGValues2020 = FGValues2020.drop(FGValues2020[FGValues2020["Date"] < "2020-01-01"].index)
BTCAverage.update({"2020":BTCPrice2020.loc[:,"Price"].mean()})

FGBTC2020 = pd.merge(FGValues2020, BTCPrice2020, on="Date")
FGBTC2020.drop(FGBTC2020.columns[FGBTC2020.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2020 = FGBTC2020.corr()

#2021 Correlation
BTCPrice2021 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2022-01-01"].index)
BTCPrice2021 = BTCPrice2021.drop(BTCPrice2021[BTCPrice2021["Date"] < "2021-01-01"].index)
FGValues2021 = FGValues.drop(FGValues[FGValues["Date"] >= "2022-01-01"].index)
FGValues2021 = FGValues2021.drop(FGValues2021[FGValues2021["Date"] < "2021-01-01"].index)
BTCAverage.update({"2021":BTCPrice2021.loc[:,"Price"].mean()})

FGBTC2021 = pd.merge(FGValues2021, BTCPrice2021, on="Date")
FGBTC2021.drop(FGBTC2021.columns[FGBTC2021.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2021 = FGBTC2021.corr()

#2022 Correlation
BTCPrice2022 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2023-01-01"].index)
BTCPrice2022 = BTCPrice2022.drop(BTCPrice2022[BTCPrice2022["Date"] < "2022-01-01"].index)
FGValues2022 = FGValues.drop(FGValues[FGValues["Date"] >= "2023-01-01"].index)
FGValues2022 = FGValues2022.drop(FGValues2022[FGValues2022["Date"] < "2022-01-01"].index)
BTCAverage.update({"2022":BTCPrice2022.loc[:,"Price"].mean()})

FGBTC2022 = pd.merge(FGValues2022, BTCPrice2022, on="Date")
FGBTC2022.drop(FGBTC2022.columns[FGBTC2022.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2022 = FGBTC2022.corr()

#2023 Correlation
BTCPrice2023 = BTCPrice.drop(BTCPrice[BTCPrice["Date"] >= "2023-04-08"].index)
BTCPrice2023 = BTCPrice2023.drop(BTCPrice2023[BTCPrice2023["Date"] < "2023-01-01"].index)
FGValues2023 = FGValues.drop(FGValues[FGValues["Date"] >= "2023-04-08"].index)
FGValues2023 = FGValues2023.drop(FGValues2023[FGValues2023["Date"] < "2023-01-01"].index)
BTCAverage.update({"2023":BTCPrice2023.loc[:,"Price"].mean()})

FGBTC2023 = pd.merge(FGValues2023, BTCPrice2023, on="Date")
FGBTC2023.drop(FGBTC2023.columns[FGBTC2023.columns.str.contains("unnamed",case=False)],axis = 1, inplace = True)
Coeff2023 = FGBTC2023.corr()

#Adding to dataframe
BTCIncrease.loc["Correlation"] = {"2018":Coeff2018.iloc[0,1],"2019":Coeff2019.iloc[0,1],"2020":Coeff2020.iloc[0,1],"2021":Coeff2021.iloc[0,1],"2022":Coeff2022.iloc[0,1],"2023":Coeff2023.iloc[0,1]}
BTCIncrease.loc["Average"] = BTCAverage
BTCIncrease = BTCIncrease.T
print(BTCIncrease)

#Plot
#fig = px.bar(BTCIncrease, x=BTCIncrease.index, y="Correlation")
#fig.update_layout(xaxis_title="Year", yaxis_title="Correlation Coefficient",
#                   yaxis_range=[-1,1], title="Correlation Coefficient Between Fear/Greed Index And Price Of Bitcoin Per Year <br><sup> 2018 - 2023 </sup>")
#fig.add_hline(y=0, line_width=3, line_dash="dot", line_color="red")
#fig.show()

#fig2 = make_subplots(specs=[[{"secondary_y": True}]])
#fig2.add_trace(go.Bar(x=BTCIncrease.index, y=BTCIncrease["Correlation"], name="Bitcoin/FG Correlation"),secondary_y=False)
#fig2.add_trace(go.Scatter(x=BTCIncrease.index, y=BTCIncrease["Average"], name="Bitcoin Price Increase (%)"),secondary_y=True)
#fig2.show()

#fig10 = go.Figure()
#fig10.add_trace(go.Scatter(x=BTCPrice2021["Date"], y=BTCPrice2021["Price"], yaxis="y"))
#fig10.add_trace(go.Scatter(x=FGValues2021["Date"], y=FGValues2021["FG"], yaxis="y2"))
#fig10.data[-1].name = "Fear/Greed Index"
#fig10.data[-2].name = "Bitcoin Price"
#fig10.update_layout(yaxis=dict(
#    title="Bitcoin Price ($)", side="left"),
#    yaxis2=dict(title="Fear/Greed Index Value", overlaying="y",
#                side="right", range = [0,100]),
#    xaxis=dict(title="Date"),
#    legend=dict(x=1.1),
#    title="Correlation Between Bitcoin Price and Fear/Greed Index Value In 2021")
#fig10.show()