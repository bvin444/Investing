# Code to analyze HYSAs
# assuming daily compounding
import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class HYSAs:

    # Class Variables
    contribution_Dictionary : ClassVar[Dict] = {'daily': 365, 'monthly': 12, 'annually': 1}
    month_days : ClassVar[Dict] = {
        1 : 31,
        2 : 28,
        3 : 31,
        4 : 30,
        5: 31,
        6 : 30,
        7 : 31,
        8 : 31,
        9 : 30,
        10 : 31,
        11 : 30,
        12 : 31
    }

    x_Frame : ClassVar[int] = 600
    y_Frame : ClassVar[int] = 200

    def __init__(self):
        self.main()

    def main(self):

        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("PRINCIPAL", "APY", "CONTRIBUTION_AMOUNT", "MONTHS", values = values): continue # break out of current iteration, and begin anew
                self.Calculation(values)
                self.window["OUTPUT_TOTAL"].update(f"{round((self.Total_OUTPUT), 2)}")
                self.window["FIRST_MONTH"].update(f"{(self.month_Array[0])}")
                self.window["LAST_MONTH"].update(f"{(self.month_Array[len(self.month_Array) - 1])}")
                self.window["DIFFERENCE"].update(f"{round(self.month_Array[len(self.month_Array) - 1] - self.month_Array[0], 2)}")
            elif event == "RESET":
                self.Reset()
        self.window.close()

    def create_main_window(self):

        HYSA_Frame = sg.Frame("HYSA Analyis", 
            [
                [sg.Text("Please enter your principal: "), sg.Input("", key = 'PRINCIPAL')],
                [sg.Text("Please specify you Annual Percentage Yield: "), sg.Input("", key = "APY")],
                [sg.Text("How many years would you like to evaluate this over?"), sg.Input("", key = "MONTHS")],
                [sg.Text("Please specify you how regularly you contribute): "), sg.Combo(list(HYSAs.contribution_Dictionary), enable_events = True, key = "CONTRIBUTION")],
                [sg.Text("Please enter how much you are contributingl: "), sg.Input("", key = 'CONTRIBUTION_AMOUNT')],
                [sg.Text("You should expect to make this much over the year (interest): "), sg.Input("", size = (10, 10), key = "OUTPUT_TOTAL")],
                [sg.Text("Your first month you made: "), sg.Input("", size = (10, 10), key = "FIRST_MONTH"), sg.Text("Your last month you made: "), 
                sg.Input("", size = (10, 10), key = "LAST_MONTH"), sg.Text("Difference: "), sg.Input("", size = (10, 10), key = "DIFFERENCE")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Reset", key = "RESET"), sg.Button("Exit", key = "EXIT")]
            ], size = (HYSAs.x_Frame, HYSAs.y_Frame))
        layout = [[HYSA_Frame]]
        window = sg.Window("HYSA Analysis", layout, resizable = True)
        return window
    
    def Calculation(self, values):
        Prin = self.Numerical_Dictionary["PRINCIPAL"]
        contribution = self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
        self.Hold = Prin
        APY = self.Numerical_Dictionary["APY"] / 100
        self.month_Index = 1
        self.month_Array = []
        for i in range(1, int(values["MONTHS"]) + 1): 

            if values["CONTRIBUTION"] == 'daily': 
                Prin = self.daily(Prin, contribution, self.month_Index)
                self.month_Index = self.month_Index + 1
                if self.month_Index == 13:
                    self.month_Index = 1

            elif values["CONTRIBUTION"] == 'monthly':
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
                print(f"{i} {Prin}")
            elif values["CONTRIBUTION"] == 'annually' and i == 13:
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
            else:
                Prin = Prin

            month_New_Value = ((Prin*APY))/ 12 
            Prin = Prin + month_New_Value
            print(f"{i} {Prin}")
            self.month_Array.append(round(month_New_Value, 2))
        self.Total_OUTPUT = sum(self.month_Array)

    def daily(self, Prin, contribution, month_Index):
        for j in range(1, HYSAs.month_days[month_Index] + 1):
            Prin = Prin + contribution
            day = day + 1
            if day % HYSAs.month_days[month_Index] == 0:
                return Prin

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
        print(self.Numerical_Dictionary)
        return False
    
    def Reset(self):
        
        self.window["OUTPUT_TOTAL"].update("")
        self.window["FIRST_MONTH"].update("")
        self.window["LAST_MONTH"].update("")
        self.window["DIFFERENCE"].update("")
        self.window["PRINCIPAL"].update("")
        self.window["APY"].update("")
        self.window["MONTHS"].update("")
        self.window["CONTRIBUTION"].update("")
        self.window["CONTRIBUTION_AMOUNT"].update("")
        self.window["FIRST_MONTH"].update("")
        self.window["LAST_MONTH"].update("")
        self.window["DIFFERENCE"].update("")
            
if __name__ == "__main__":
    Executable = HYSAs()