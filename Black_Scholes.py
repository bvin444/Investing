# Code to model Black-Sholes


import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class Black_Scholes:

    def __init__(self):
        self.main()
    def main(self):
        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("COP", "STRIKE", "RFI", "TtM", "VOL", "SP", values=values): continue
                self.calc_Black_Scholes()
    def create_main_window(self):
        Black_Scholes_Frame = sg.Frame("Black Scholes",
            [
                [sg.Text("Please enter your Call-Option price"), sg.Input('', key = "COP")],
                [sg.Text("Please enter your Strike Price"), sg.Input('', key = "STRIKE")],
                [sg.Text("Please enter your risk-free interest rate"), sg.Input('', key = "RFI")],
                [sg.Text("Please enter your time to maturity"), sg.Input('', key = "TtM")],
                [sg.Text("Please enter your Asset's Volatility"), sg.Input('', key = "VOL")],
                [sg.Text("Please enter your Spot-price"), sg.Input('', key = "SP")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
        layout = [[Black_Scholes_Frame]]
        return sg.Window("Black-Scholes", layout, resizable = True)
    def calc_Black_Scholes(self):
        pass
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