#--------------Window Size------------------\\
from kivy.config import Config
Config.set("graphics", "width", "393")
Config.set("graphics", "height", "635")
Config.set("graphics", "resizable", False)

#--------------Code Libraries------------------\\
import os
import threading
import numpy as np
import pandas as pd
from plyer import filechooser

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

#--------------Python Files------------------\\
from User_Account import UserAccount
from Classification_Model import AI_Model
from GUI_Components import CircularProgressBar
from GUI_Components import Legend
from GUI_Components import InputFrame
from GUI_Components import NavBar
from GUI_Components import NavButton


#--------------Summary Screen------------------\\
class SummaryScreen(Screen):

    def __init__(self, user_acc, **kwargs):

        super().__init__(**kwargs)
        
        self.model = AI_Model("Trained_Model/random_forest_model.joblib")

        self.user_acc = user_acc

        #---------Setting Background------\\
        self.layout = FloatLayout(size_hint = (1, 1))

        with self.layout.canvas:

            self.bckgrd_color = Color(0.2, 0.6, 0.8, 1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        
        self.bind(size = self.adjust_canvas, pos = self.adjust_canvas)

        #---------Scroll Bar------\\
        self.scroll_bar = ScrollView(size_hint = (1, 1))
        self.content_panel = FloatLayout(size_hint_y = None, height = 1350)

       #---------Title Label------\\
        self.title_lb = Label(
            text = "Summary",
            size_hint = (None, None),
            font_size = "35sp",
            pos = (100, 1245), # (x, y)
            bold = True,
            color = (1, 1, 1, 1)
        )

        #---------Progress Bar/Circle------\\
        self.progress_bar = CircularProgressBar()
        self.progress_bar.pos = (-135, 440)
        
        #---------Legend------\\
        self.color_legend = Legend()
        self.color_legend.pos = (350, 1055)
        
        #---------Heart Disease Label------\\
        self.heartdis_lb = Label(
            text = "Heart Disease?",
            size_hint = (None, None),
            font_size = "18sp",
            pos = (115, 895), # (x, y)
            bold = True,
            color = (0, 0, 0, 1),
        )

        #---------Prediction Label------\\
        self.prediction_lb = Label(
            text = "",
            size_hint = (None, None),
            font_size = "18sp",
            pos = (325, 895), # (x, y)
            bold = True,
            color = (0, 0, 0, 1),
        )

        #---------Details Label------\\
        self.details_lb = Label(
            text = "Details",
            size_hint = (None, None),
            font_size = "20sp",
            pos = (55, 785), # (x, y)
            bold = True,
            color = (0, 0, 0, 1),
        )

        #---------Import File Label------\\
        self.import_lb = Label(
            text = "Import File",
            size_hint = (None, None),
            font_size = "14sp",
            pos = (385, 785), # (x, y)
            color = (0, 0, 0, 1),
        )

        #---------Import File Button------\\
        self.import_btn = Button(
            size_hint = (None, None),
            size = (33, 33),
            background_normal = "Images/add_file.png",
            background_disabled_normal = "Images/active_add_file.png",
            border = (0, 0, 0, 0),
            pos = (495, 820), # (x, y)
        )

        self.import_btn.bind(on_release = self.on_click_import)

        #---------Params Tables------\\
        self.demographics_tb = InputFrame("Demographics", self.user_acc.get_demographic_params(), on_done_callback = self.update_user_details)
        self.demographics_tb.pos = (60, 600)

        self.lifestyle_tb = InputFrame("Lifestyle", self.user_acc.get_lifestyle_params(), on_done_callback = self.update_user_details)
        self.lifestyle_tb.pos = (60, 365)

        self.cardiovascular_tb = InputFrame("Cardiovascular", self.user_acc.get_cardiovascular_params(), on_done_callback = self.update_user_details)
        self.cardiovascular_tb.pos = (60, 130)

        #---------Adding Widgets to Panel------\\
        self.content_panel.add_widget(self.title_lb) # Title
        self.content_panel.add_widget(self.progress_bar) # Progress Bar
        self.content_panel.add_widget(self.color_legend) # Color Legend
        
        self.content_panel.add_widget(self.heartdis_lb) # Heart Disease Label
        self.content_panel.add_widget(self.prediction_lb) # Prediction Label
        
        self.content_panel.add_widget(self.details_lb) # Details Label
        self.content_panel.add_widget(self.import_lb) # Import File Label
        self.content_panel.add_widget(self.import_btn) # Import File Button
        self.content_panel.add_widget(self.demographics_tb) # Demographics Table
        self.content_panel.add_widget(self.lifestyle_tb) # Lifestyle Table
        self.content_panel.add_widget(self.cardiovascular_tb) # Cardiovascular Table
 
        self.scroll_bar.add_widget(self.content_panel)
        self.layout.add_widget(self.scroll_bar)

        self.add_widget(self.layout)
        
        # Loading UserAccount Details
        self.load_user_details()

        
    #---------Methods------\\

    # Processing data and converting it to a numpy array of size (n x k)
    def process_data(self, med_params):

        input_data = list(med_params.items())

        input_data = [item[1] for item in input_data[4:]]
    
        for i in range(len(input_data)):

            if input_data[i] in ("Nan", "No", "Male"):

                input_data[i] = 0

            elif input_data[i] in ("Yes", "Female"):

                input_data[i] = 1

            else:

                continue
        
        input_data = np.array(input_data, dtype = float).reshape(1, -1)

        return input_data


    # Gets and displays cvd prediction and risk 
    def load_user_details(self):

        cvd_out = self.user_acc.get_cvd_out()
        cvd_risk = self.user_acc.get_cvd_risk()
        
        self.prediction_lb.text = cvd_out
        self.color_legend.set_lb_text(cvd_out)

        self.progress_bar.run_progress_clock(cvd_risk)

    
    # Continuously captures data as it changes/updates 
    def update_user_details(self, med_params):
        
        self.user_acc.set_med_params(med_params) # Updating medical params in UserAccount

        med_dict = self.user_acc.get_med_params()

        print(med_dict)

        cvd_risk = self.model.compute_cvd_risk(med_dict)

        processed_data = self.process_data(med_dict)

        print(processed_data)

        cvd_out = self.model.predict_cvd(processed_data)
        
        self.user_acc.set_cvd_risk(cvd_risk)
        self.user_acc.set_cvd_out(cvd_out)

        self.load_user_details()


    # Reads and clean medical files
    def read_file(self, filepath = None):

        allowed_keys = ["Gender", "Age", "Smoke", "Alcohol", "Active",
                         "Gluc(mg/dL)", "Chol(mg/dL)", "BP(high)", "BP(low)",
                         "Height(m)", "Weight(kg)"]

        try:

            data_frame = pd.read_excel(filepath)

            if not data_frame.empty:
            
               med_params = data_frame.iloc[0].to_dict()

               med_params = {key: str(value) for key, value in med_params.items() if key in allowed_keys}

               return med_params
            
            else:

                return dict()
        
        except  Exception as e:

            print(f'\nError reading file: {e}')

            return dict()


    # Retrieves chosen file and updates labels accordingly
    def retrieve_file(self, selection):

        if selection: # list of file paths (can be more than 1)
       
            selected_file = selection[0]

            print(f"Selected file: {selected_file}")

            med_params = self.read_file(selected_file)

            self.demographics_tb.set_tb_input(med_params)
            self.lifestyle_tb.set_tb_input(med_params)
            self.cardiovascular_tb.set_tb_input(med_params)

            self.update_user_details(med_params)
        
        self.import_btn.disabled = False

    
    # Opens current directory where to chose a file from
    def open_filechooser(self, time_secs):

        current_dir = os.getcwd()

        def open_dialog():

            filechooser.open_file(on_selection = self.retrieve_file, path = current_dir)
        
        threading.Thread(target = open_dialog).start()
    
    
    # Import File Button method
    def on_click_import(self, instance):

        self.import_btn.disabled = True

        Clock.schedule_once(self.open_filechooser, 0.1)


    def adjust_canvas(self, *args):

        self.rect.size = self.size
        self.rect.pos = self.pos


#--------------Other Screens------------------\\
class LLAMAScreen(Screen):

    pass

class ProfileScreen(Screen):

    pass


#--------------App Window------------------\\
class HeartSeer(App):

    def build(self):
        
        root = FloatLayout()

        user_account = UserAccount()
        
        #---------Screen Manager------\\
        self.screen_manager = ScreenManager()

        #---------Adding Screens to the Screen Manager------\\
        self.screen_manager.add_widget(SummaryScreen(user_account, name = "Summary"))
        self.screen_manager.add_widget(LLAMAScreen(name = "LLAMA"))
        self.screen_manager.add_widget(ProfileScreen(name = "Profile"))

        self.screen_manager.size_hint = (1, 1)
        self.screen_manager.pos = (0, 0)

        #---------Navigation Bar------\\
        self.nav_bar = NavBar()

        self.nav_bar.size_hint_x = 1
        self.nav_bar.pos_hint = {"y": 0}
        
        #---------Navigation Buttons------\\
        self.summary_btn = NavButton("Summary", "Images/summary.png", "Images/active_summary.png", self.change_screen)
        self.llama_btn = NavButton("LLAMA", "Images/chatbot.png", "Images/active_chatbot.png", self.change_screen)
        self.profile_btn = NavButton("Profile", "Images/profile.png", "Images/active_profile.png", self.change_screen)
        
        #---------Adding Buttons to the Navigation Bar------\\
        self.nav_bar.add_widget(self.summary_btn)
        self.nav_bar.add_widget(self.llama_btn)
        self.nav_bar.add_widget(self.profile_btn)

        self.summary_btn.set_active(True)
        
        #---------Adding Screen Manager and Navigation Bar to Root------\\
        root.add_widget(self.screen_manager)
        root.add_widget(self.nav_bar)

        return root

    
    def change_screen(self, screen_name):

        self.screen_manager.current = screen_name

        self.summary_btn.set_active(screen_name == "Summary")
        self.llama_btn.set_active(screen_name == "LLAMA")
        self.profile_btn.set_active(screen_name == "Profile")


HeartSeer().run()