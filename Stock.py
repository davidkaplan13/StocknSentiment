from tkinter import *
import quandl

Quandl_API = "9AK1N1LNy7PzHefyRR9w"

class Stock(object):

    def __init(self):
        quandl.ApiConfig.api_key = Quandl_API
        self.PullStockData()


    def PullStockData(self):
        print(x)
        stock = quandl.get("WIKI/"+str(x),rows=25)
        print(stock)


class Window(Frame):

    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.master = master
        self.Main_window()
        self.stock = Stock()


    def Main_window(self):
        """Creating The Main Window Widgets"""
        self.master.title("Main")
        self.master.configure(background='light steel blue',highlightbackground='light steel blue')

        self.LabelT = Label(self.master, text="Select Company:", font=("Calibri", 12))
        self.var = StringVar(self.master)

        self.Choice = [
            "AAPL",
            "AMZN",
            "MSFT"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master, self.var, *self.Choice)  # Drop Down Menu
        self.ButtonT = Button(self.master, text="Enter", command=self.CompanyEntry)

        self.LabelT.place(x=0, y=50)
        self.w.place(x=0, y=75)
        self.ButtonT.place(x=0, y=100)

    def CompanyEntry(self):
        """Retrives Entry of USER and calls on Pull Stock Data from Class Stock"""
        try:
            global x
            x = self.var.get()
            self.stock.PullStockData()

        except:
            print("Help me")

root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()