from bank_system import BankSystem
import page_controller as pc


def start_gui(**kwargs):
    
    root = pc.tk.Tk()

    root.title(kwargs["window_title"])

    # get screen width and height
    screen_width = root.winfo_screenwidth()  # width of the screen
    screen_height = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window    
    kwargs["middle_coords"] = {'X': (screen_width / 2) - (kwargs["window_width"] / 2), 'Y': (screen_height / 2) - (kwargs["window_height"] / 2)}

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (kwargs["window_width"], kwargs["window_height"], kwargs["middle_coords"]['X'], kwargs["middle_coords"]['Y']))

    pc.PageController(root, kwargs["data"], kwargs["middle_coords"])
    
    root.lift()
    
    root.mainloop()


if __name__ == "__main__":
    
    #Instantiate bank class
    bank = BankSystem()
    
    #Start gui and pass instance of bank class to be used by GUI
    start_gui(window_title = "Bank System", window_width = 700, window_height = 400, data = bank) 

