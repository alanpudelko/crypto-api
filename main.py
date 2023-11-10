import os
import requests
from tkinter import *

API_KEY = os.environ["API_KEY"]


def fetch_data(currency_name):
    if value.get() != currency_name:
        return

    url = f"https://rest.coinapi.io/v1/exchangerate/{currency_name}/USD"
    headers = {
        "X-CoinAPI-Key": API_KEY
    }
    response = requests.get(url, headers=headers)
    time = response.json()["time"]
    time = time.split("T")

    date = time[0]
    hour = time[1].strip(".0000000Z")

    asset_id_base = response.json()["asset_id_base"]
    rate = round(response.json()["rate"], 2)
    exchange_label.config(text=f"1 {asset_id_base} = ${rate}")
    formatted_time = f"{hour.split(':')[0].zfill(2)}:{hour.split(':')[1].zfill(2)}:{hour.split(':')[2].zfill(2)}"
    date_label.config(text=f"{date}, {formatted_time}")
    window.after(5000, fetch_data, currency_name)


def on_currency_change(*args):
    if hasattr(window, 'after_id'):
        window.after_cancel(window.after_id)
    window.after_id = window.after(3000, fetch_data, value.get())


window = Tk()
window.title("Crypto Exchange Rates")
window.geometry("450x200")


title_label = Label(window, text="Crypto Exchange Rates", font=("Arial", 30))
title_label.grid(column=1, row=0)

OPTIONS = [
    "BTC",
    "ETH",
    "LTC"
]

value = StringVar()

currencies_list = OptionMenu(window, value, *OPTIONS, command=fetch_data)
currencies_list.grid(column=1, row=1)

exchange_label = Label(window, text="Choose a currency", font=("Arial", 20))
exchange_label.grid(column=1, row=2)

date_label = Label(window, text="", font=("Arial", 20))
date_label.grid(column=1, row=3)

value.trace("w", on_currency_change)

window.mainloop()
