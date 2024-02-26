import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os 
from datetime import datetime, timedelta

#Setting working directory to file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

Data = pd.read_csv('Data/FGBTCCombined.csv').to_dict()
print(Data)

profit = {}
hold = 0

MinDate = datetime.strptime(Data["Date"].min(), "%Y-%m-%d")
MaxDate = datetime.strptime(Data["Date"].max(), "%Y-%m-%d")
Delta = timedelta(days=1)

for HODL in range (100):
    StartDate = MinDate
    EndDate = MaxDate
    while (StartDate <= EndDate):
        Today = Data[str(StartDate).removesuffix(" 00:00:00")]
        print(Today)
        StartDate += Delta