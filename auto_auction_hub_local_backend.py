import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="usertemp",
  password="password",
  database="auto_auction_hub_local"
)

data = pd.read_csv('your_file.csv')
