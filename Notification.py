import tkinter as tk

class Notification:

    window = None
    label = None

    def __init__(self,windowName) -> None:
        self.windowName = windowName

    def setGUI(self):
        self.window = tk.Tk(className=self.windowName)
        self.window.geometry("400x200")
        return self

    def setMessage(self,message):     
        self.label = tk.Label(
            text= message,
            foreground="white",  # Set the text color to white
            background="black",  # Set the background color to black
            width=200,
            height=200,
            font=("Arial", 10)             
        )
        return self

    def setVersion(self,text):
        label = tk.Label(self.window,text = text,
            foreground="white",  # Set the text color to white
            background="black", )
        label.place(
            relx = 1.0,
            rely = 1.0,
            anchor ='se')
        return self
    
    def displayGUI(self):
        self.label.pack()
        self.window.mainloop() 
