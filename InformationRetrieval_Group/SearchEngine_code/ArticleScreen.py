import tkinter as tk
import webbrowser
from PIL import Image, ImageTk


class Article_Screen:

    def __init__(self, ranked_docs, docs, title_idx, page_num, frame):

        self.ranked_docs = ranked_docs
        self.doc_idx_list  = [doc[0][0] for doc in self.ranked_docs] # True doc ids from data
        self.docs = docs

        self.page_num = page_num
        self.doc_id = ((self.page_num - 1) * 3) + title_idx # Doc id in the ranked list of docs

        self.back_frame = frame # Frame on the background with all the widgets from Results_Screen
        self.back_colour = "white" # Background Colour


  #\\----------Superimposed Frame Configuration-------------------\\
        self.frame = tk.Frame(self.back_frame, width = 1280, height = 720)
        self.frame.pack()
        self.frame.config(background = self.back_colour)


  #\\----------Image Label Configuration-------------------\\
        self.logo = Image.open("Images/SE_Logo.png")
        self.logo = self.logo.resize((280, 280))
        self.logo_img = ImageTk.PhotoImage(self.logo)

        self.logo_lb = tk.Label(self.frame, image = self.logo_img, bg = self.back_colour)
        self.logo_lb.image = self.logo_img
        self.logo_lb.place(x = 125, y = -55)


    #\\----------Back to Search Configuration-------------------\\
        self.back_lb = tk.Label(self.frame, font = ("Arial", 14), bg = self.back_colour, cursor = "hand2",text = "< Back")

        self.back_lb.bind("<Enter>", lambda e, lbl = self.back_lb: lbl.config(fg = "blue", font = ("Arial", 14)))
        self.back_lb.bind("<Leave>", lambda e, lbl = self.back_lb: lbl.config(fg = "black", font = ("Arial", 14)))
        self.back_lb.bind("<Button-1>", lambda e: self.on_click_back())

        self.back_lb.place(x = 30, y = 50)


    #\\----------Retrieved Document Configuration-------------------\\
        self.doc_frame = tk.Frame(self.frame, width = 275, height = 250)
        self.doc_frame.place(x = 400, y = 145)
        self.doc_frame.config(background = self.back_colour)

       #\\----------Title-----------\\
        self.title_lb = tk.Label(self.doc_frame, font=("Arial", 14, "bold"), justify = "left", bg = self.back_colour,
                                    text = self.docs[self.doc_idx_list[self.doc_id]]["title"])
        
        self.title_lb.grid(row = 0, column = 0, padx = 2, pady = (3, 12), sticky = "w")


       #\\----------Authors-----------\\
        self.authors_lb_ref = tk.Label(self.doc_frame, font=("Arial", 12, "bold"), justify = "left", bg = self.back_colour,
                                    text = "Authors: ")

        self.authors_lb = tk.Label(self.doc_frame, font=("Arial", 12), justify = "left", bg = self.back_colour,
                                    text = self.set_display_limit(self.docs[self.doc_id]["authors"], 25))
           
           # Position in Frame
        self.authors_lb_ref.grid(row = 1, column = 0, padx = (12, 0), pady = 3, sticky = "w")
        self.authors_lb.grid(row = 1, column = 0, columnspan = 2, padx = (87, 2), pady = 3, sticky = "w")


       #\\----------Publication Date-----------\\
        self.date_lb_ref = tk.Label(self.doc_frame, font=("Arial", 12, "bold"), justify = "left", bg = self.back_colour,
                                    text = "Published in:")

        self.date_lb = tk.Label(self.doc_frame, font=("Arial", 12), justify = "left", bg = self.back_colour,
                                    text = self.docs[self.doc_idx_list[self.doc_id]]["publication_date"])
        
           # Position in Frame
        self.date_lb_ref.grid(row = 2, column = 0, padx = (15, 0), pady = 3, sticky = "w")
        self.date_lb.grid(row = 2, column = 0, columnspan = 2, padx = (124, 2), pady = 3, sticky = "w")


       #\\----------Abstract-----------\\
        self.abstract_lb_ref = tk.Label(self.doc_frame, font=("Arial", 11, "bold"), justify = "left", bg = self.back_colour,
                                    text = "Abstract")

        self.abstract_lb = tk.Label(self.doc_frame, font=("Arial", 11), justify = "left", bg = self.back_colour,
                                    text = self.set_display_limit(self.docs[self.doc_idx_list[self.doc_id]]["abstract"]))

           # Position in Frame
        self.abstract_lb_ref.grid(row = 3, column = 0, padx = (8, 0), pady = (15, 2), sticky = "w")
        self.abstract_lb.grid(row = 4, column = 0, columnspan = 2, padx = (8, 0), pady = (3, 8), sticky = "w")


       #\\----------Link to Document-----------\\
        self.arxiv_url = f'https://arxiv.org/abs/{self.docs[self.doc_idx_list[self.doc_id]]["id"]}'

        self.link_lb_ref = tk.Label(self.doc_frame, font=("Arial", 11, "bold"), justify = "left", bg = self.back_colour,
                                    text = "Link:")
        
        self.link_lb = tk.Label(self.doc_frame, font=("Arial", 11, "underline"), justify = "left", bg = self.back_colour, fg = "blue",
                                    cursor = "hand2", text = self.arxiv_url)
           
           # Position in Frame
        self.link_lb_ref.grid(row = 5, column = 0, padx = (16, 0), pady = 3, sticky = "w")
        self.link_lb.grid(row = 5, column = 0, columnspan = 2, padx = (58, 2), pady = 3, sticky = "w")

           # Key Bindings
        self.link_lb.bind("<Button-1>", self.on_click_link)
        

    #\\----------Document Number Configuration-------------------\\
        self.doc_count_fr = tk.Frame(self.frame, width = 50, height = 100)
        self.doc_count_fr.config(background = self.back_colour)

           # Position in Frame
        self.doc_count_fr.place(x = 495, y = 580)


       #\\----------Previous Button-----------\\
        self.prev_button = tk.Button(self.doc_count_fr, text = "< Previous", borderwidth = 2,
                                     bg = "#289DB9", width = 9, font=("Arial", 12, "bold"),
                                     cursor = "hand2", command = self.on_click_previous)
           # Position in Frame
        self.prev_button.grid(row = 0, column = 0, padx = 12, pady = 3, sticky = "w")


       #\\----------Document Number Page-----------\\
        self.doc_count_lb = tk.Label(self.doc_count_fr, text = f'{self.doc_id + 1} / {len(self.ranked_docs)}',
                                     font = ("Arial", 14, "bold"), bg = self.back_colour)
           
           # Position in Frame
        self.doc_count_lb.grid(row = 0, column = 1, padx = 12, pady = 3, sticky = "w")


       #\\----------Next Button-----------\\
        self.next_button = tk.Button(self.doc_count_fr, text = "Next >", borderwidth = 2,
                                      bg = "#289DB9", width = 9, font = ("Arial", 12, "bold"),
                                      cursor = "hand2", command = self.on_click_next)
 
           # Position in Frame
        self.next_button.grid(row = 0, column = 2, padx = 12, pady = 3, sticky = "w")


#\\--------------------Other Methods-------------------\\


#\\------Setting a limit on the number of chars displayed--------\\
    def set_display_limit(self, text, limit = 700):

        # Removing spaces at the beginning of the string
        text = "\n".join(paragraph.lstrip() for paragraph in text.split("\n"))
    
        if len(text) <= limit:

            return text

        text = text[:limit].rsplit(" ", 1)[0] # Making sure no word is cut-off
        
        return text + "..."


#\\----------Clearing & Setting Text on Labels-----------\\
    def set_label_text(self):
       
       # Clear Labels
        self.title_lb.config(text = "")
        self.authors_lb.config(text = "")
        self.date_lb.config(text = "")
        self.abstract_lb.config(text = "")
        self.link_lb.config(text = "")
       
       # Update Labels
        self.title_lb.config(text = self.docs[self.doc_idx_list[self.doc_id]]["title"])
        self.authors_lb.config(text = self.set_display_limit(self.docs[self.doc_id]["authors"], 25))
        self.date_lb.config(text = self.docs[self.doc_idx_list[self.doc_id]]["publication_date"])
        self.abstract_lb.config(text = self.set_display_limit(self.docs[self.doc_idx_list[self.doc_id]]["abstract"]))
        self.arxiv_url = f'https://arxiv.org/abs/{self.docs[self.doc_idx_list[self.doc_id]]["id"]}'
        self.link_lb.config(text = self.arxiv_url)


#\\--------------------Button/Label Commands-------------------\\


#\\----------On Click Link-----------\\
    def on_click_link(self, event = None):

        webbrowser.open(self.arxiv_url)


#\\----------On Click "Back" Label-----------\\
    def on_click_back(self):

        for widget in self.frame.winfo_children():

            widget.destroy()

        self.frame.destroy()


#\\----------On Click Previous Button-----------\\
    def on_click_previous(self):

        if self.doc_id > 0:

            self.doc_id -= 1
            self.doc_count_lb.config(text = f'{self.doc_id + 1} / {len(self.ranked_docs)}')
            self.set_label_text()
 
        else:
            self.doc_id = len(self.ranked_docs) - 1
            self.doc_count_lb.config(text = f'{self.doc_id + 1} / {len(self.ranked_docs)}')
            self.set_label_text()


#\\----------On Click Next Button-----------\\
    def on_click_next(self):

        if self.doc_id < len(self.ranked_docs) - 1:

            self.doc_id += 1
            self.doc_count_lb.config(text = f'{self.doc_id + 1} / {len(self.ranked_docs)}')
            self.set_label_text()

        else:
            self.doc_id = 0
            self.doc_count_lb.config(text = f'{self.doc_id + 1} / {len(self.ranked_docs)}')
            self.set_label_text()
