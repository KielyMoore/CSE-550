import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def loadData(filter):
    filePath = filter["file_label"] +"/"+ datetime.strptime(filter["start_date"], '%m/%d/%Y').strftime('%Y%m%d') +"/"+ filter["user"] + "/summary.csv"
    data = pd.read_csv(filePath)
    # Ideally data is loaded from a sever and stored locally
    return data