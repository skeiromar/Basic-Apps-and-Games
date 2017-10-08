from tkinter import *
from tkinter import ttk   # for styling
import math  # only used this for square root


WID = 4  # width of the buttons
p = 7  # Top and bottom padding for the buttons

class Calculator:

    calc_value = 0.0

    div_trigger = False
    mul_trigger = False
    sub_trigger = False
    add_trigger = False
    pow_trigger = False
    sqrt_trigger = False

    def button_press(self, value):

        entryVal = self.number_entry.get()
        if entryVal != "number too large":
            entryVal += value

        for l in entryVal:
            if entryVal.count(".") > 1 :
                entryVal = entryVal[:-1]
            elif entryVal.count("Divide by zero: Error") > 0:
                entryVal = entryVal[-1:]


        self.number_entry.delete(0, "end")

        self.number_entry.insert(0, entryVal)

        if value == "AC":
            self.number_entry.delete(0, "end")
            self.div_trigger = False
            self.mul_trigger = False
            self.sub_trigger = False
            self.add_trigger = False
            self.pow_trigger = False


    def isFloat(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def math_button_press(self, value):

        if self.isFloat(str(self.number_entry.get())):
            self.div_trigger = False
            self.mul_trigger = False
            self.sub_trigger = False
            self.add_trigger = False
            self.pow_trigger = False


            self.calc_value = float(self.entry_value.get())

            if value == "/":
                self.div_trigger = True
            elif value == "*":
                self.mul_trigger = True
            elif value == "+":
                self.add_trigger = True
            elif value == "**":
                self.pow_trigger = True
            else:
                self.sub_trigger = True

            self.number_entry.delete(0, "end")


    def equal_button_press(self):
        if self.isFloat(str(self.number_entry.get())):
            if self.add_trigger or self.mul_trigger or self.div_trigger or \
                    self.sub_trigger or self.pow_trigger or self.sqrt_trigger:

                if self.add_trigger:

                    solution = self.calc_value + float(self.entry_value.get())

                elif self.mul_trigger:

                    solution = self.calc_value * float(self.entry_value.get())

                elif self.div_trigger:
                    if float(self.entry_value.get()) != 0.0:
                        solution = self.calc_value / float(self.entry_value.get())
                    else:
                        solution = "Divide by zero: Error"

                elif self.sub_trigger:

                    solution = self.calc_value - float(self.entry_value.get())

                elif self.pow_trigger:

                    solution = self.calc_value ** float(self.entry_value.get())

                elif self.sqrt_trigger:
                    if float(self.entry_value.get()):
                        solution = math.sqrt(float(self.entry_value.get()))
                    else:
                        print('h')

                self.number_entry.delete(0, "end")

            try:    # checks to see if we are dividing by zero
                self.number_entry.insert(0, solution)
            except Exception:
                print('')


            self.div_trigger = False
            self.mul_trigger = False
            self.sub_trigger = False
            self.add_trigger = False
            self.pow_trigger = False
            self.sqrt_trigger = False


    def sq_press(self):
        if self.isFloat(str(self.number_entry.get())):   # checks if string is convertible
            entryVal = self.number_entry.get()
            self.number_entry.delete(0, "end")
            if entryVal != "" and entryVal != ".":
                solution = float(entryVal) ** 2
                self.number_entry.insert(0, solution)
            elif OverflowError:
                self.number_entry.insert(0, "number too large")

    def sqrt_press(self, value):

        self.sqrt_trigger = False
        if value == "sqrt":
            self.sqrt_trigger = True


    def __init__(self, root):

        self.entry_value = StringVar(root, value="") #the default value of entry
        root.title("Calculator")
        root.geometry("405x470")
        root.resizable(width=False, height=False)
        style = ttk.Style() # We use ttk for styling
        style.configure("TButton",
                        foreground='black',background='white',font="Monaco 18 bold",padding=18)
        style.configure("TEntry",
                        font="Monaco 19",padding=10)
        self.number_entry = ttk.Entry(root,
                        textvariable=self.entry_value,width=60)
        self.number_entry.grid(row=0, columnspan=4,sticky=W,padx=10)


        # First Row


        self.button7 = ttk.Button(root, text='7',
            width=WID,command =lambda: self.button_press('7')).grid(row=1, column=0,pady=p,sticky=E)

        self.button8 = ttk.Button(root, text='8',
            width=WID,command=lambda: self.button_press('8')).grid(row=1, column=1,pady=p)

        self.button9 = ttk.Button(root, text='9',
            width=WID,command=lambda: self.button_press('9')).grid(row=1, column=2,pady=p)
        self.button_div = ttk.Button(root, text='/',
        width=WID,command=lambda: self.math_button_press('/')).grid(row=1, column=3,pady=p,sticky=W)


        # Second Row

        self.button4 = ttk.Button(root, text='4',
            width=WID,command =lambda: self.button_press('4')).grid(row=2, column=0,pady=p,sticky=E)

        self.button5 = ttk.Button(root, text='5',
            width=WID,command=lambda: self.button_press('5')).grid(row=2, column=1,pady=p)

        self.button6 = ttk.Button(root, text='6',
            width=WID,command=lambda: self.button_press('6')).grid(row=2, column=2,pady=p)
        self.button_mul = ttk.Button(root, text='x',
        width=WID,command=lambda: self.math_button_press('*')).grid(row=2, column=3,pady=p,sticky=W)

        # Third Row

        self.button1 = ttk.Button(root, text='1',
            width=WID,command =lambda: self.button_press('1')).grid(row=3, column=0,pady=p,sticky=E)

        self.button2 = ttk.Button(root, text='2',
            width=WID,command=lambda: self.button_press('2')).grid(row=3, column=1,pady=p)

        self.button3 = ttk.Button(root, text='3',
            width=WID,command=lambda: self.button_press('3')).grid(row=3, column=2,pady=p)
        self.button_add = ttk.Button(root, text='+',
        width=WID,command=lambda: self.math_button_press('+')).grid(row=3, column=3,pady=p,sticky=W)

        # Fourth Row

        self.button_clear = ttk.Button(root, text='AC',
            width=WID,command =lambda: self.button_press('AC')).grid(row=4, column=0,pady=p,sticky=E)

        self.button0 = ttk.Button(root, text='0',
            width=WID,command=lambda: self.button_press('0')).grid(row=4, column=1,pady=p)
        self.button0 = ttk.Button(root, text='.',
            width=WID, command=lambda: self.button_press('.')).grid(row=5, column=1, pady=p)

        self.button_eq = ttk.Button(root, text='=',
            width=WID,command=lambda: self.equal_button_press()).grid(row=4, column=2,pady=p)
        self.button_sub = ttk.Button(root, text='-',
        width=WID,command=lambda: self.math_button_press('-')).grid(row=4, column=3,pady=p,sticky=W)
        self.button_pow = ttk.Button(root, text='X^Y',
        width=WID, command=lambda: self.math_button_press('**')).grid(row=5, column=3, pady=p,sticky=W)
        self.button_sq = ttk.Button(root, text='X^2',
        width=WID, command=lambda: self.sq_press()).grid(row=5, column=2, pady=p, sticky=W)
        self.button_sqrt = ttk.Button(root, text='sqrt',
        width=WID, command=lambda: self.sqrt_press('sqrt')).grid(row=5, column=0, pady=p, sticky=E)


root = Tk()


calc = Calculator(root)


root.mainloop()