import tkinter as tk
from tkinter import messagebox
import bitget.v1.mix.order_api as maxOrderApi
import bitget.v1.mix.market_api as market_api
import bitget.v1.mix.account_api as account_api
import time
import bitget.bitget_api as bitget_api
from datetime import datetime
from bitget.exceptions import BitgetAPIException
import tkinter as tk
from tkinter import ttk
import sys
import tkinter as tk
import threading
import time
import os
import datetime

#
def show_error_message(error_msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Fehler", error_msg)


if __name__ == '__main__':


    apiKey = "xxxx"
    secretKey = '''xxxx'''
    passphrase = "xxxx"



    try:
        maxOrderApi = maxOrderApi.OrderApi(apiKey, secretKey, passphrase)
        market_api = market_api.MarketApi(apiKey, secretKey, passphrase)
        account_api = account_api.AccountApi(apiKey, secretKey, passphrase)
        bitget_api = bitget_api.BitgetApi(apiKey, secretKey, passphrase)

        print("Verbunden")
    except BitgetAPIException as e:
        print("error: ", e)


# Definiere den Start- und Endzeitpunkt für den Monat
print("start:")
startyear = int(input("Jahr (z.B. 2024): "))
startmonth = int(input("Monat (1-12): "))
startday = int(input("Tag (1-31): "))
print("Ende:")
Endeyear = int(input("Jahr (z.B. 2024): "))
Endemonth = int(input("Monat (1-12): "))
Endeday = int(input("Tag (1-31): "))

start_date = datetime.datetime(startyear, startmonth, startday, 0, 0, 0)
end_date = datetime.datetime(Endeyear, Endemonth, Endeday, 23, 59, 59)

# Definiere den API-Limit
api_limit = 99

# Initialisiere die Gesamtnetto-Gewinne
total_net_profit = 0

# Schleife über jeden Tag im Monat
current_date = start_date
while current_date <= end_date:
    # Berechne den Start- und Endzeitpunkt für den aktuellen Tag
    current_day_start = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)
    current_day_end = current_date.replace(
        hour=23, minute=59, second=59, microsecond=999999)

    # Konvertiere die Start- und Endzeitpunkte in Unix-Zeitstempel (in Millisekunden)
    start_time_ms = int(current_day_start.timestamp() * 1000)
    end_time_ms = int(current_day_end.timestamp() * 1000)

    # Setze die Parameter für die API-Anfrage
    params = {
        "limit": api_limit,
        "startTime": start_time_ms,
        "endTime": end_time_ms
    }

    # Führe die API-Anfrage durch
    response = bitget_api.get("/api/v2/mix/position/history-position", params)

    # Iteriere über die Antwort und sammle die Daten
    for item in response['data']['list']:
        net_profit = float(item['netProfit'])
        total_net_profit += net_profit

        # Hier kannst du mit den Daten für jeden Tag arbeiten
        print("Symbol:", item['symbol'])
        print("PnL:", item['pnl'])
        print("Netto-Gewinn:", net_profit)
        print("Erstellungszeit:", datetime.datetime.fromtimestamp(
            int(item['ctime']) / 1000.0))
        print("Update-Zeit:",
              datetime.datetime.fromtimestamp(int(item['utime']) / 1000.0))
        print("-----------------------------")

    # Gehe zum nächsten Tag über
    current_date += datetime.timedelta(days=1)

# Gesamtnetto-Gewinn ausgeben
print("Gesamtnetto-Gewinn", total_net_profit)
