import tkinter as tk
import pandas as pd
import json
import math
import time
import re

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from tkinter import messagebox
from PIL import Image, ImageTk
from sklearn.feature_extraction.text import CountVectorizer

from ArticleScreen import Article_Screen
from RetrievalModels import BM25_Model, SBERT_Model


class Results_Screen:

    def __init__(self, frame, query):

        self.frame = frame
        self.query = query
        self.DOCS_PER_PAGE = 3
        self.TOP_N = 100 # top n docs retrieved by BM25 
        self.TOP_K = 50 # top k docs retrieved by SBERT

        file_path = "Dataset/arxiv_subset.json"
        self.back_colour  = "white" # Background Colour


  #\\----------Document Retrieval Process-------------------\\
        self.documents = self.load_text_data(file_path, 500)
        self.lemmatizer = WordNetLemmatizer()
        self.text_data, self.vocabulary, self.dataframe = self.process_text()
           
           # Retrieval Models
        self.BM25_model = BM25_Model(self.documents, self.text_data, self.vocabulary, self.dataframe)
        
        self.SBERT_model = SBERT_Model()
 
            # Retrieved Documents
        start_time = time.time()

        self.ranked_docs = self.BM25_model.rank_documents(self.process_query(), self.TOP_N)
        self.ranked_docs = self.SBERT_model.rank_documents(self.ranked_docs, ' '.join(self.process_query()), self.TOP_K)

        end_time = time.time()
        self.duration = round(end_time - start_time, 4)

        self.doc_idx_list  = [doc[0][0] for doc in self.ranked_docs] # True doc ids from data


  #\\----------Image Label Configuration-------------------\\
        self.logo = Image.open("Images/SE_Logo.png")
        self.logo = self.logo.resize((280, 280))
        self.logo_img = ImageTk.PhotoImage(self.logo)

        self.logo_lb = tk.Label(self.frame, image = self.logo_img, bg = self.back_colour)
        self.logo_lb.image = self.logo_img
           
           # Position in Frame
        self.logo_lb.place(x = 8, y = -55)
        

  #\\----------Text Box Configuration-------------------\\
        self.text_box = tk.Entry(self.frame, font = ("Arial", 14), width = 42, bd = 0, relief = "solid", fg = "#333333",
                                 highlightbackground = "#3F5965", highlightcolor = "#3F5965", highlightthickness = 1)
        
        
        self.text_box.insert(0, self.query) # Inserting query at position 0

           # Position in Frame
        self.text_box.place(x = 305, y = 62)

           # Key Bindings
        self.text_box.bind("<Return>", self.on_click_search) # Binding "enter" key


    #\\----------Search Button Configuration-------------------\\
        self.srch_icon = Image.open("Images/search_icon.png")
        self.srch_icon = self.srch_icon.resize((26, 26))
        self.srch_img = ImageTk.PhotoImage(self.srch_icon)

        self.srch_button = tk.Button(self.frame, image = self.srch_img, command = self.on_click_search,
                                     borderwidth = 1, bg = "#289DB9", cursor = "hand2")
        
        self.srch_button.image = self.srch_img
           
           # Position in Frame
        self.srch_button.place(x = 773, y = 60)

    #\\----------Search Time Label Configuration-------------------\\
        self.srch_time_lb = tk.Label(self.frame, font=("Arial", 12), bg = self.back_colour,
                                     text = f'About {len(self.ranked_docs)} document(s) retrieved in {self.duration} secs.')
        
        self.srch_time_lb.place(x = 305, y = 100)


    #\\----------Retrieved Documents Configuration-------------------\\
        self.docs_frame = tk.Frame(self.frame, width = 275, height = 250)
        self.docs_frame.place(x = 305, y = 135)
        self.docs_frame.config(background = self.back_colour)

        self.title_lb_list = []
        self.author_lb_list = []
        self.date_lb_list = []
        self.abstract_lb_list = []

        pos = 0 # Row number in grid-like frame 

        for i in range(self.DOCS_PER_PAGE):

           #\\----------Title-----------\\
            title_lb = tk.Label(self.docs_frame, font=("Arial", 14, "bold"), justify = "left",
                                bg = self.back_colour, cursor = "hand2")
           
                # Position in Frame
            title_lb.grid(row = 0 + pos, column = 0, padx = 2, pady = 3, sticky = "w")

               # Key Bindings
            title_lb.bind("<Enter>", lambda e, lbl = title_lb: lbl.config(fg = "blue", font = ("Arial", 14, "bold", "underline")))
            title_lb.bind("<Leave>", lambda e, lbl = title_lb: lbl.config(fg = "black", font = ("Arial", 14, "bold")))
               
               # On Click Command
            title_lb.bind("<Button-1>", lambda e, idx = i: self.on_click_title(idx))


           #\\----------Authors-----------\\
            authors_lb = tk.Label(self.docs_frame, font = ("Arial", 12), justify = "left", bg = self.back_colour)

                # Position in Frame
            authors_lb.grid(row = 1 + pos, column = 0, padx = 2, pady = 3, sticky = "w")


           #\\----------Publication Date-----------\\
            date_lb = tk.Label(self.docs_frame, font = ("Arial", 12), justify = "left", bg = self.back_colour)

                # Position in Frame
            date_lb.grid(row = 1 + pos, column = 1, padx = 2, pady = 3, sticky = "w")


           #\\----------Abstract-----------\\
            abstract_lb = tk.Label(self.docs_frame, font = ("Arial", 11), justify  = "left", bg = self.back_colour)

                # Position in Frame
            abstract_lb.grid(row = 2 + pos, column = 0, padx = 2, pady =(3,15), sticky = "w")


           #\\----------Widget Lists (Length = 3)-----------\\
            self.title_lb_list.append(title_lb)
            self.author_lb_list.append(authors_lb)
            self.date_lb_list.append(date_lb)
            self.abstract_lb_list.append(abstract_lb)
            pos += 3

        self.max_page_num = max(1, math.ceil(len(self.ranked_docs) / 3)) # either 1 or > 1
        self.page_num = 1
        self.set_label_text()


    #\\----------Page Number Configuration-------------------\\
        self.page_count_fr = tk.Frame(self.frame, width = 50, height = 100)
        self.page_count_fr.config(background = self.back_colour)

           # Position in Frame
        self.page_count_fr.place(x = 495, y = 580)


       #\\----------Previous Button-----------\\
        self.prev_button = tk.Button(self.page_count_fr, text = "< Previous", borderwidth = 2, 
                                     bg = "#289DB9", width = 9, font = ("Arial", 12, "bold"),
                                     command = self.on_click_previous, cursor = "hand2")
        
           # Position in Frame
        self.prev_button.grid(row = 0, column = 0, padx = 12, pady = 3, sticky = "w")


       #\\----------Page Count Label-----------\\
        self.page_count_lb = tk.Label(self.page_count_fr, text = f'{self.page_num} / {self.max_page_num}',
                                      font=("Arial", 14, "bold"), bg = self.back_colour)

           # Position in Frame
        self.page_count_lb.grid(row = 0, column = 1, padx = 12, pady = 3, sticky = "w")


       #\\----------Next Button-----------\\
        self.next_button = tk.Button(self.page_count_fr, text = "Next >", borderwidth = 2,
                                      bg = "#289DB9", width = 9, font = ("Arial", 12, "bold"),
                                      command = self.on_click_next, cursor = "hand2")
        
           # Position in Frame
        self.next_button.grid(row = 0, column = 2, padx = 12, pady = 3, sticky = "w")



#\\--------------------Other Methods-------------------\\

    def clean_text(self, text):
        
        if not isinstance(text, str):
           return ""

        text = re.sub(r'[^a-zA-Z\s.,;!?]', '', text) # Removes anything, but letters and some punc
        
        text = re.sub(r'\s+', ' ', text.lower().strip())

        tokens = word_tokenize(text)

        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if len(token) > 1] #heavy on memory

        return ' '.join(tokens)


#\\----------Checking if a doc has all the necessary content-----------\\
    def check_doc_content(self, doc):

        content = ["id", "title", "abstract", "authors", "update_date"]

        for key in content:

            if not doc.get(key, "").strip(): # Empty or Blank spaces

                return True
            
        return False


#\\----------Loading a specified number of docs from dataset-----------\\
    def load_text_data(self, file_path, num_papers = None):

        docs = []

        with open(file_path, "r", encoding = "utf-8") as file:

            for i, line in enumerate(file):

                paper = json.loads(line)  # Convert JSON string to dictionary

                if self.check_doc_content(paper):
                    continue

                doc = dict(
                    id  =  paper["id"],
                    title =  paper["title"],
                    abstract = paper["abstract"],
                    authors = paper["authors"],
                    publication_date =  paper["update_date"]
                )

                docs.append(doc)

                if num_papers is not None and i == num_papers - 1:
                    break

        return docs
    

#\\----------Retrieving Title and Abstract from each doc-----------\\
    def process_text(self):

        text_data = []

        for doc in self.documents:

            text = doc["title"] + " " + doc["abstract"]

            text = self.clean_text(text)

            text_data.append(text)

        vectorizer = CountVectorizer(stop_words = 'english')

        documents_vectorized = vectorizer.fit_transform(text_data) # Term count across docs
        vocabulary = vectorizer.get_feature_names_out() # Creating the term vocabulary
        
        # Matrix with doc ids as rows and vocabulary terms as cols
        dataframe = pd.DataFrame(documents_vectorized.toarray(), columns = vocabulary)

        return  text_data, vocabulary, dataframe
    

# Checked!
    def process_query(self):

        query = self.clean_text(self.query)

        vectorizer = CountVectorizer(stop_words = 'english', vocabulary = self.vocabulary)

        q_terms = vectorizer.build_analyzer()(query)

        filtered_tokens = [term for term in q_terms if term in self.vocabulary]

        return filtered_tokens


#\\------Setting a limit on the number of chars displayed--------\\
    def set_display_limit(self, text, limit = 125):

        # Removing spaces at the beginning of the string
        text = "\n".join(paragraph.lstrip() for paragraph in text.split("\n"))
    
        if len(text) <= limit:

            return text

        text = text[:limit].rsplit(" ", 1)[0] # Making sure no word is cut-off
        
        return text + "..."


#\\----------Setting Text on Labels-----------\\
    def set_label_text(self):

        start  = (self.page_num - 1) * self.DOCS_PER_PAGE
        
        for i in range(self.DOCS_PER_PAGE):

            if start == len(self.ranked_docs):
                return

            doc_idx = self.doc_idx_list[start]

            self.title_lb_list[i].config(text = self.documents[doc_idx]["title"])
            self.author_lb_list[i].config(text = self.set_display_limit(self.documents[doc_idx]["authors"], 25))
            self.date_lb_list[i].config(text = self.documents[doc_idx]["publication_date"])
            self.abstract_lb_list[i].config(text = self.set_display_limit(self.documents[doc_idx]["abstract"]))

            start  += 1


#\\----------Clearing Text on Labels-----------\\
    def clear_label_text(self):

        for i in range(self.DOCS_PER_PAGE):

            self.title_lb_list[i].config(text = "")
            self.author_lb_list[i].config(text = "")
            self.date_lb_list[i].config(text = "")
            self.abstract_lb_list[i].config(text = "")


#\\----------Checking Query for Empty or Blank Spaces-----------\\
    def check_text(self, text):

        if not text.strip():

            return True
        else:
            return False


#\\--------------------Button/Label Commands-------------------\\


#\\----------On Click Title Label-----------\\
    def on_click_title(self, index):
        
        screen3 = Article_Screen(self.ranked_docs, self.documents, index, self.page_num, self.frame)


#\\----------On Click Search Button-----------\\
    def on_click_search (self, event = None):

        new_query = self.text_box.get()
        new_query = re.sub(r'\s+', ' ', new_query.lower().strip())

        if self.query == new_query:
            return
        
        else:
            self.query = new_query


        self.text_box.delete(0, "end")
        self.text_box.insert(0, self.query)


        if self.check_text(self.query):
            messagebox.showinfo("System Warning", "Please type something in the text box.")
        
        else:
            start_time = time.time()
            self.ranked_docs = self.BM25_model.rank_documents(self.process_query(), self.TOP_N)
            self.ranked_docs = self.SBERT_model.rank_documents(self.ranked_docs, ' '.join(self.process_query()), self.TOP_K)
            end_time = time.time()
            self.duration = round(end_time - start_time, 4)

            self.doc_idx_list  = [doc[0][0] for doc in self.ranked_docs]
            self.max_page_num = max(1, math.ceil(len(self.ranked_docs) / 3))
            self.page_num = 1
            self.page_count_lb.config(text = f'{self.page_num} / {self.max_page_num}')
            self.srch_time_lb.config(text = f'About {len(self.ranked_docs)} document(s) retrieved in {self.duration} secs.')
            self.clear_label_text()
            self.set_label_text()


#\\----------On Click Previous Button-----------\\
    def on_click_previous(self):

        if self.page_num > 1:

            self.page_num -= 1
            self.page_count_lb.config(text = f'{self.page_num} / {self.max_page_num}')
            self.clear_label_text()
            self.set_label_text()   
        
        else:
            self.page_num = self.max_page_num
            self.page_count_lb.config(text = f'{self.page_num} / {self.max_page_num}')
            self.clear_label_text()
            self.set_label_text()
           

#\\----------On Click Next Button-----------\\
    def on_click_next(self):

        if self.page_num < self.max_page_num:

            self.page_num += 1
            self.page_count_lb.config(text = f'{self.page_num} / {self.max_page_num}')
            self.clear_label_text()
            self.set_label_text()
        
        else:
            self.page_num = 1
            self.page_count_lb.config(text = f'{self.page_num} / {self.max_page_num}')
            self.clear_label_text()
            self.set_label_text()