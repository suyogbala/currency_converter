import tkinter as tk
from requests import get

BASE_URL = 'http://data.fixer.io/api/'
API_KEY = '2459c67155f69ff6059b77059a7ba434'

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.currency1_label = tk.Label(root, text = "Enter the currency you want to convert:")
        self.currency1_label.pack()

        self.currency1_var = tk.StringVar()
        self.currency1_entry = tk.Entry(root, textvariable = self.currency1_var)
        self.currency1_entry.pack()

        self.currency2_label = tk.Label(root, text = "Enter the currency you want to get converted:") 
        self.currency2_label.pack()

        self.currency2_var = tk.StringVar()
        self.currency2_entry = tk.Entry(root, textvariable = self.currency2_var)
        self.currency2_entry.pack()

        self.amount_label = tk.Label(root, text = "Enter the amount:")
        self.amount_label.pack()

        self.amount_var = tk.IntVar(value = '')
        self.amount_entry = tk.Entry(root, textvariable = self.amount_var)
        self.amount_entry.pack()

        self.convert_button = tk.Button(root, text = "Convert", command = self.convert_currency)
        self.convert_button.pack()

        self.result_label = tk.Label(root, text = "")
        self.result_label.pack()

    def get_currencies(self):
        endpoint = f'latest?access_key={API_KEY}'
        url = BASE_URL + endpoint
        data = get(url).json()
        date = data['date']
        return data, date

    def euro1(self, data, date, currency2, amount):
        rate_in_euro_of_currency2 = data['rates'][currency2]
        result = f'As of {date}, {amount} {self.currency1_var.get().upper()} is equal to {round(amount * rate_in_euro_of_currency2, 2)} {currency2}.'
        return result

    def euro2(self, data, date, currency1, currency2, amount):
        rate_in_euro_of_currency1 = data['rates'][currency1]
        result = f'As of {date}, {amount} {currency1} is equal to {round(amount * rate_in_euro_of_currency1, 2)} {currency2}.'
        return result

    def exchange_rate(self, data, date, currency1, currency2, amount):
        if currency1 == 'eur':
            result = self.euro1(data, date, currency2, amount)
        elif currency2 == 'eur':
            result = self.euro2(data, date, currency1, currency2, amount)
        else:
            rate_in_euro_of_currency1 = data['rates'][currency1]
            rate_in_euro_of_currency2 = data['rates'][currency2]
            result = f'As of {date}, {amount} {currency1} is equal to {round((amount * rate_in_euro_of_currency2) / rate_in_euro_of_currency1, 2)} {currency2}.'
        return result

    def convert_currency(self):
        currency1 = self.currency1_var.get().upper()
        currency2 = self.currency2_var.get().upper()
        amount = self.amount_var.get()
        data, date = self.get_currencies()

        if currency1 not in data['rates']:
            result = f'Please enter the correct currency for {currency1}'
        elif currency2 not in data['rates']:
            result = f'Please enter the correct currency for {currency2}'
        else:
            result = self.exchange_rate(data, date, currency1, currency2, amount)
        self.result_label.config(text=result)


root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()