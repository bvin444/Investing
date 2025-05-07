# Code to model Black-Sholes

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
import math as math
import yfinance as yf

from scipy.stats import norm

class Black_Scholes:

    def __init__(self):
        self.main()
    def main(self):
        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                # if self.input_Validation("STOCK_PRICE", "STRIKE", "RFI", "TtM", "VOL", values=values): continue
                if self.identify_Stock(values): continue
    def create_main_window(self):
        Black_Scholes_Frame = sg.Frame("Black Scholes",
            [
                [sg.Text("Please enter the stock's ticker"), sg.Input("", key = "TICKER")],
                [sg.Text("Stock's-Price"), sg.Input('', key = "STOCK_PRICE")],
                [sg.Text("Strike Price"), sg.Input('', key = "STRIKE")],
                [sg.Text("Risk-free interest rate"), sg.Input('', key = "RFI")],
                [sg.Text("Time to maturity"), sg.Input('', key = "TtM")],
                [sg.Text("Volatility"), sg.Input('', key = "VOL")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
        layout = [[Black_Scholes_Frame]]
        return sg.Window("Black-Scholes", layout, resizable = True)
    
    def identify_Stock(self, values):
        try:
            ticker = yf.Ticker(str(values["TICKER"]))
        except:
            sg.popup("Sorry, ticker not found")
            return True
        self.window["STOCK_PRICE"].update(ticker.info['regularMarketPrice'])


    def calc_Black_Scholes(self):
        N = 1 
        S_0 = self.numerical_Dictionary["STOCK_PRICE"]
        K = self.numerical_Dictionary["STRIKE"]
        r =self.numerical_Dictionary["RFI"]
        sigma = self.numerical_Dictionary["VOL"]
        T = self.numerical_Dictionary["TtM"]

        d_1 = (math.log(S_0/K) + (r + 0.5*(sigma**2))*T) / (sigma*(T)**(1/2))
        d_2 = d_1 - sigma*(T)**(1/2)
        Call = S_0 * norm.cdf(d_1) - K*(math.e**(-r*T))*norm.cdf(d_2)
        print(round(Call,2))
    def input_Validation(self, *args, values):
        for test_Input in args:
            if values[test_Input] == '':
                sg.popup("Input cannot be blank!")
                return True
            try:
                float(values[test_Input])
            except:
                sg.popup("Input must be a numerical value")
                return True
        self.numerical_Dictionary = {key : float(values[key]) for key in args}
        return False
if __name__ == "__main__":
    Executable = Black_Scholes()