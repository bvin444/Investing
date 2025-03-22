# Code to analyze HYSAs
import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
class HYSAs:
    contribution_Dictionary : ClassVar[Dict] = {'daily': 365, 'monthly': 12, 'annually': 1}
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
                self.window["OUTPUT_TOTAL"].update(f"{round((self.Total_OUTPUT - self.Hold), 2)}")
                self.window["FIRST_MONTH"].update(f"{(self.month_Array[0])}")
                self.window["LAST_MONTH"].update(f"{(self.month_Array[len(self.month_Array) - 1])}")
                self.window["DIFFERENCE"].update(f"{round(self.month_Array[len(self.month_Array) - 1] - self.month_Array[0], 2)}")
        self.window.close()

    def create_main_window(self):

        HYSA_Frame = sg.Frame("HYSA Analyis", 
            [
                [sg.Text("Please enter your principal: "), sg.Input("", key = 'PRINCIPAL')],
                [sg.Text("Please specify you Annual Percentage Yield: "), sg.Input("", key = "APY")],
                [sg.Text("How many months would you like to evaluate this over?"), sg.Input("", key = "MONTHS")],
                [sg.Text("Please specify you how regularly you contribute): "), sg.Combo(list(HYSAs.contribution_Dictionary), enable_events = True, key = "CONTRIBUTION")],
                [sg.Text("Please enter how much you are contributingl: "), sg.Input("", key = 'CONTRIBUTION_AMOUNT')],
                [sg.Text("You should expect to make this much over the year: "), sg.Input("", size = (10, 10), key = "OUTPUT_TOTAL")],
                [sg.Text("Your first month you made: "), sg.Input("", size = (10, 10), key = "FIRST_MONTH"), sg.Text("Your last month you made: "), 
                sg.Input("", size = (10, 10), key = "LAST_MONTH"), sg.Text("Difference: "), sg.Input("", size = (10, 10), key = "DIFFERENCE")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ], size = (HYSAs.x_Frame, HYSAs.y_Frame))
        layout = [[HYSA_Frame]]
        window = sg.Window("HYSA Analysis", layout, resizable = True)
        return window
    
    def Calculation(self, values):
        Prin = self.Numerical_Dictionary["PRINCIPAL"]
        self.Hold = Prin
        APY = self.Numerical_Dictionary["APY"] / 100
        # for 
        self.month_Array = []
        Contribution = self.Numerical_Dictionary["CONTRIBUTION_AMOUNT"]
        for i in range(1, int(values["MONTHS"]) + 1): # should be fine, as value is already an int HYSAs.contribution_Dictionary[values["CONTRIBUTION"]+1]
            month_New_Value = ((Prin*APY))/ 12 # how much money I got from the month
            Prin = Prin + month_New_Value
            self.month_Array.append(round(month_New_Value, 2))

        self.Total_OUTPUT = Prin

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
            
if __name__ == "__main__":
    Executable = HYSAs()