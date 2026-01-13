import tkinter as tk
import re
from tkinter import messagebox
from PIL import Image, ImageTk

from ResultsScreen import Results_Screen


class Initial_Screen:

    def __init__(self, parent):

        self.back_colour = "white" # Background Colour

        self.frame = tk.Frame(parent, width = 1280, height = 720)
        self.frame.pack()
        self.frame.config(background = self.back_colour)
 
 
    #\\----------Image Label Configuration-------------------\\

        self.logo = Image.open("Images/SE_Logo.png")
        self.logo_img = ImageTk.PhotoImage(self.logo)

        self.logo_label = tk.Label(self.frame, image = self.logo_img, bg = self.back_colour)
        self.logo_label.image = self.logo_img
        self.logo_label.place(x = 410, y = 15)

        
    #\\----------Text Box Configuration-------------------\\

        self.text_box = tk.Entry(self.frame, font=("Arial", 14), width = 42, bd = 0, relief = "solid", fg ="#333333",
                                 highlightbackground = "#3F5965", highlightcolor = "#3F5965", highlightthickness = 1)
        
        self.text_box.place(x = 405, y = 435)

        self.text_box.bind("<Return>", self.search_button) # Binding "enter" key 

    
    #\\----------Search Button Configuration-------------------\\

        self.srch_icon = Image.open("Images/search_icon.png")
        self.srch_icon = self.srch_icon.resize((26, 26))
        self.srch_img = ImageTk.PhotoImage(self.srch_icon)

        self.srch_button = tk.Button(self.frame, image = self.srch_img, command = self.search_button,
                                     borderwidth = 1, bg = "#289DB9", cursor = "hand2")
        
        self.srch_button.image = self.srch_img
        self.srch_button.place(x = 873, y = 433)


    #\\----------Other Methods-------------------\\

    def check_text(self, text):

        if not text.strip(): # Empty or Blank spaces

            return True
        else:
            return False
    
    
    def search_button(self, event = None):

        query = self.text_box.get()

        if self.check_text(query):
            messagebox.showinfo("System Warning", "Please enter something in the text box.")
        else:

            for widget in self.frame.winfo_children():
              widget.destroy()

            query  = re.sub(r'\s+', ' ', query.lower().strip())
            
            screen2 = Results_Screen(self.frame, query)


def desktop_window_size (window):
    window_width = 1280
    window_height = 650
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(False, False)

def main():

    root = tk.Tk()
    root.title('ShcolarlySeek')
    desktop_window_size(root)
    search_engine = Initial_Screen(root)
    root.mainloop()
   
    
if __name__ == "__main__": main()