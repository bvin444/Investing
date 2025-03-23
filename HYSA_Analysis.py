# Code to analyze HYSAs
# assuming daily compounding

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class HYSAs:

    # Class Variables
    contribution_Dictionary : ClassVar[Dict] = {'daily': 365, 'monthly': 12, 'annually': 1}
    month_days : ClassVar[int] = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]



    x_Frame : ClassVar[int] = 750
    y_Frame : ClassVar[int] = 200

    def __init__(self):
        self.main()

    def main(self):

        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("PRINCIPAL", "APY", "CONTRIBUTION_AMOUNT", "YEARS", values = values): continue # break out of current iteration, and begin anew
                self.Calculation(values)
                self.window["OUTPUT_TOTAL"].update(f"{round((self.Total_OUTPUT), 2)}")
                self.window["FIRST_MONTH"].update(f"{round((self.day_Array[0])*31, 2)}")
                self.window["LAST_MONTH"].update(f"{round((self.day_Array[len(self.day_Array) - 1]*31), 2)}")
                self.window["DIFFERENCE"].update(f"{round((self.day_Array[len(self.day_Array) - 1]*31) - (self.day_Array[0]*31), 2)}")
                self.window["BALANCE_TOTAL"].update(f"{round(self.Total_Balance, 2)}")
                self.window["PERSONAL_CONTRIBUTIONS_TOTAL"].update(f"{round(self.Index * self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"], 2)}")

            elif event == "RESET":
                self.Reset()
        self.window.close()

    def create_main_window(self):

        HYSA_Frame = sg.Frame("HYSA Analyis", 
            [
                [sg.Text("Please enter your principal: "), sg.Input("", key = 'PRINCIPAL')],
                [sg.Text("Please specify you Annual Percentage Yield: "), sg.Input("", key = "APY")],
                [sg.Text("How many years would you like to evaluate this over?"), sg.Input("", key = "YEARS")],
                [sg.Text("Please specify you how regularly you contribute): "), sg.Combo(list(HYSAs.contribution_Dictionary), enable_events = True, key = "CONTRIBUTION")],
                [sg.Text("Please enter how much you are contributingl: "), sg.Input("", key = 'CONTRIBUTION_AMOUNT')],
                [sg.Text("You should expect to make this much over the year (interest): "), sg.Input("", size = (10, 10), key = "OUTPUT_TOTAL"), sg.Text("Your Balance Total: "), sg.Input("", size = (10, 10), 
                key = "BALANCE_TOTAL"), sg.Text("Total Contribution"), sg.Input("", key = "PERSONAL_CONTRIBUTIONS_TOTAL")],
                [sg.Text("Your first month you made: "), sg.Input("", size = (10, 10), key = "FIRST_MONTH"), sg.Text("Your last month you made: "), 
                sg.Input("", size = (10, 10), key = "LAST_MONTH"), sg.Text("Difference: "), sg.Input("", size = (10, 10), key = "DIFFERENCE")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Reset", key = "RESET"), sg.Button("Exit", key = "EXIT")]
            ], size = (HYSAs.x_Frame, HYSAs.y_Frame))
        layout = [[HYSA_Frame]]
        window = sg.Window("HYSA Analysis", layout, resizable = True)
        return window
    
    def Calculation(self, values): # add contribution start from there.
        Prin = self.Numerical_Dictionary["PRINCIPAL"]
        self.Hold = Prin
        APY = self.Numerical_Dictionary["APY"] / 100
        self.day_Array = []
        day = 0
        self.Index = 0
        daily_Rate = ((1+APY)**(1/365) - 1)
        print(daily_Rate)

        for i in range(1, (int(values["YEARS"]) * 365) + 1): # 1 - 365
            print(i)
            day = day + 1

            if values["CONTRIBUTION"] == 'daily': 
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]

            elif values["CONTRIBUTION"] == 'monthly' and day in (HYSAs.month_days):
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
                self.Index = self.Index + 1

            elif values["CONTRIBUTION"] == 'annually' and day % 365 == 1:
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]

            else:
                Prin = Prin

            if day == 365:
                day = 0
 
            day_New_Value = Prin * daily_Rate # how much is being added daily
            Prin = Prin + day_New_Value
            self.day_Array.append(day_New_Value)
        self.Total_Balance = Prin
        self.Total_OUTPUT = round(sum(self.day_Array), 2)

    def input_Validation(self, *args, values):

        for Test_Input in args:
            if values[Test_Input] == '':
                sg.popup("Input cannot be blank", title = "Blank Input")
                return True
            try:
                float(values[Test_Input])
            except:
                sg.popup("Input must be a integer", title = "Integer Input Error")
                return True
        self.Numerical_Dictionary = {key: (float(values[key])) for key in args} # accessing individual keys?
        return False
    
    def Reset(self):
        
        self.window["OUTPUT_TOTAL"].update("")
        self.window["FIRST_MONTH"].update("")
        self.window["LAST_MONTH"].update("")
        self.window["DIFFERENCE"].update("")
        self.window["PRINCIPAL"].update("")
        self.window["APY"].update("")
        self.window["YEARS"].update("")
        self.window["CONTRIBUTION"].update("")
        self.window["CONTRIBUTION_AMOUNT"].update("")
        self.window["FIRST_MONTH"].update("")
        self.window["LAST_MONTH"].update("")
        self.window["DIFFERENCE"].update("")
            
if __name__ == "__main__":
    Executable = HYSAs()