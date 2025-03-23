# Code to analyze HYSAs
# assuming daily compounding

# TODO: add in functionality to allow user to choose between firist of the month and last of the month.
# TODO: add in plotting functionality.

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")  # Ensures compatibility with PySimpleGUI

class HYSAs:

    # Class Variables
    contribution_Dictionary : ClassVar[Dict] = {'daily': 365, 'monthly': 12, 'annually': 1}
    contribution_Time : ClassVar[Dict] = {'Beginning': [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335], 'End': [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]}
    plot_Dictionary : ClassVar[Dict] = ['daily interest', 'daily balance']
    x_Frame : ClassVar[int] = 750
    y_Frame : ClassVar[int] = 240

    def __init__(self):

        self.main()

    def main(self):

        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT", "EXIT_1"): break
            elif event == "SUBMIT":
                if self.input_Validation("PRINCIPAL", "APY", "CONTRIBUTION_AMOUNT", "YEARS", values = values): continue # break out of current iteration, and begin anew
                self.Calculation(values)
                self.window["OUTPUT_TOTAL"].update(f"{round((self.Total_OUTPUT), 2)}")
                self.window["FIRST_MONTH"].update(f"{round((sum(self.day_Array[:31])), 2)}")
                self.window["LAST_MONTH"].update(f"{round((sum(self.day_Array[-31:])), 2)}")
                self.window["DIFFERENCE_MONTH"].update(f"{round((sum(self.day_Array[-31:]) - sum(self.day_Array[:31])), 2)}")
                self.window["FIRST_DAY"].update(f"{round((self.day_Array[0]), 2)}")
                self.window["LAST_DAY"].update(f"{round((self.day_Array[len(self.day_Array) - 1]), 2)}")
                self.window["DIFFERENCE_DAY"].update(f"{round((self.day_Array[len(self.day_Array) - 1]) - (self.day_Array[0]), 2)}")
                self.window["BALANCE_TOTAL"].update(f"{round(self.Total_Balance, 2)}")
                self.window["PERSONAL_CONTRIBUTIONS_TOTAL"].update(f"{round(self.Index * self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"], 2)}")
            elif event == "PLOT":
                if self.input_Validation("PRINCIPAL", "APY", "CONTRIBUTION_AMOUNT", "YEARS", values = values): continue # break out of current iteration, and begin anew
                self.plot(values)
            elif event == "RESET":
                self.Reset()
            elif event == "RESET_1":
                self.Reset_1()
        self.window.close()

    def create_main_window(self):

        HYSA_Frame = sg.Frame("HYSA Analyis", 
            [
                [sg.Text("Please enter your principal: "), sg.Input("", key = 'PRINCIPAL')],
                [sg.Text("Please specify you Annual Percentage Yield: "), sg.Input("", key = "APY")],
                [sg.Text("How many years would you like to evaluate this over?"), sg.Input("", key = "YEARS")],
                [sg.Text("Please specify you how regularly you contribute): "), sg.Combo(list(HYSAs.contribution_Dictionary), enable_events = True, key = "CONTRIBUTION"), 
                sg.Text("Contribution at the end or beginning of the month"), sg.Combo(list(HYSAs.contribution_Time), default_value = 'Beginning', key = "CONTRIBUTION_TIME")],
                [sg.Text("Please enter how much you are contributingl: "), sg.Input("", key = 'CONTRIBUTION_AMOUNT')],
                [sg.Text("You should expect to make this much over the year (interest): "), sg.Input("", size = (10, 10), key = "OUTPUT_TOTAL"), sg.Text("Your Balance Total: "), sg.Input("", size = (10, 10), 
                key = "BALANCE_TOTAL"), sg.Text("Total Contribution"), sg.Input("", key = "PERSONAL_CONTRIBUTIONS_TOTAL")],
                [sg.Text("Your first month you made: "), sg.Input("", size = (10, 10), key = "FIRST_MONTH"), sg.Text("Your last month you made: "), 
                sg.Input("", size = (10, 10), key = "LAST_MONTH"), sg.Text("Difference: "), sg.Input("", size = (10, 10), key = "DIFFERENCE_MONTH")],
                [sg.Text("Your first day you made: "), sg.Input("", size = (10, 10), key = "FIRST_DAY"), sg.Text("Your last day you made: "), 
                sg.Input("", size = (10, 10), key = "LAST_DAY"), sg.Text("Difference: "), sg.Input("", size = (10, 10), key = "DIFFERENCE_DAY")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Reset", key = "RESET")],
                [sg.Button("Exit", key = "EXIT")]
            ], size = (HYSAs.x_Frame, HYSAs.y_Frame))
        
        Plot_Frame = sg.Frame("Plot",
            [
                [sg.Text("What data would you like to plot?"), sg.Combo(list(HYSAs.plot_Dictionary), key = "Y-AXIS_DATA")],
                [sg.Text("Please enter your x-axis label"), sg.Input("", key = "X-AXIS")],
                [sg.Text("Please enter your y-axis label"), sg.Input("", key = "Y-AXIS")],
                [sg.Text("Please enter your title"), sg.Input("", key = "TITLE")],
                [sg.Text("Would you like to plot this data?"), sg.Button("Plot", key = "PLOT")],
                [sg.Button("Reset", key = "RESET_1"), sg.Button("Exit", key = "EXIT_1")]

            ], size = (HYSAs.x_Frame, HYSAs.y_Frame))
        layout = [[HYSA_Frame], [Plot_Frame]]
        window = sg.Window("HYSA Analysis", layout, resizable = True)
        return window
    
    def Calculation(self, values): # add contribution start from there.

        Prin = self.Numerical_Dictionary["PRINCIPAL"]
        self.Hold = Prin
        APY = self.Numerical_Dictionary["APY"] / 100
        self.day_Array = []
        self.Prin_Array = []
        day = 0
        self.Index = 0
        daily_Rate = ((1+APY)**(1/365) - 1) # DIR

        for i in range(1, (int(values["YEARS"]) * 365) + 1): # 1 - 365 
            day = day + 1

            if values["CONTRIBUTION"] == 'daily': 
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]

            elif values["CONTRIBUTION"] == 'monthly' and day in HYSAs.contribution_Time[values["CONTRIBUTION_TIME"]]:
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
                self.Index = self.Index + 1

            elif values["CONTRIBUTION"] == 'annually' and day % 365 == 1:
                Prin = Prin + self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]

            else:
                Prin = Prin

            if day == 365:
                day = 0
 
            day_New_Value = Prin * daily_Rate # how much is being added daily
            self.day_Array.append(day_New_Value) # array that holds each day's earned-interest
            Prin = Prin + day_New_Value
            self.Prin_Array.append(Prin)
        self.Total_Balance = Prin
        self.Total_OUTPUT = round(sum(self.day_Array), 2)

    def plot(self, values):

        x = np.linspace(1, (int(values["YEARS"]) * 365), (int(values["YEARS"]) * 365))
        fig, ax = plt.subplots() 
        if values["Y-AXIS_DATA"] == 'daily interest':
            ax.plot(x, self.day_Array)
        elif values["Y-AXIS_DATA"] == 'daily balance':
            ax.plot(x, self.Prin_Array)
        else:
            sg.popup("Please select data to plot")
            return
        ax.set_ylabel(f"{values["Y-AXIS"]}")
        ax.set_xlabel(f"{values["X-AXIS"]}")
        ax.set_title(f"{values["TITLE"]}")
        ax.grid()
        fig.canvas.manager.show()

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
        self.window["DIFFERENCE_MONTH"].update("")
        self.window["PRINCIPAL"].update("")
        self.window["APY"].update("")
        self.window["YEARS"].update("")
        self.window["CONTRIBUTION"].update("")
        self.window["CONTRIBUTION_AMOUNT"].update("")
        self.window["FIRST_DAY"].update("")
        self.window["LAST_DAY"].update("")
        self.window["DIFFERENCE_DAY"].update("")
        self.window["BALANCE_TOTAL"].update("")
        self.window["PERSONAL_CONTRIBUTIONS_TOTAL"].update("")
    
    def Reset_1(self):
        self.window["X-AXIS"].update("")
        self.window["Y-AXIS"].update("")
        self.window["TITLE"].update("")

if __name__ == "__main__":
    Executable = HYSAs()