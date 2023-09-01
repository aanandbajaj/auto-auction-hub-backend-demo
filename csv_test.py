import pandas as pd

file_path = r'C:\Users\aanan\Documents\Projects\Auto Auction Hub\auto-auction-hub\src\assets\auctions.csv'
try:
    df = pd.read_csv(file_path)
    print(df)
except Exception as e:
    print('Error reading CSV:', e)