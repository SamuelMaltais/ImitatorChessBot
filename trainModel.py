from getData import *
import pandas as pd

inputPositions, outputPositons = getData()
inputDf = pd.Series(inputPositions)
print(len(inputDf))