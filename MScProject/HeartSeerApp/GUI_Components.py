from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


#--------------Circular Progress Bar------------------\\
class CircularProgressBar(Widget):
    
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.progress = 0
        self.stop_gap = 0

        self.fading_param = 1.0
        
        #---------Setting Background------\\
        with self.canvas:

            # Background Circle
            self.bckgrd_color = Color(0.929, 0.792, 0.004)
            self.bckgrd_circle = Ellipse(size = (200, 200), pos = self.center)
            
            # Circular Outline
            self.outline_color = Color(0.62, 0.62, 0.62, 1)
            self.track_line = Line(circle = (self.center_x, self.center_y, 100, 0, 360), width = 8)
            
            # Progress Bar 
            self.bar_color = Color(0.929, 0.792, 0.004)
            self.progress_bar = Line(circle = (self.center_x, self.center_y, 100, 0, 0), width = 8)
        
        #---------Percentage Label------\\
        self.percent_lb = Label(
            text = "0%",
            size_hint = (None, None),
            font_size = '28sp',
            color = (0, 0, 0, 1),
            size = (200, 50),
            pos = (self.center_x - 100, self.center_y - 25))
        
        self.add_widget(self.percent_lb)

        self.bind(pos = self.adjust_canvas, size = self.adjust_canvas)


    #---------Methods------\\

    def lerp_color(self, c1, c2, t): # linear interpolation

        return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))


    def brighten_color(self, color, factor = 1.5):

        return tuple(min(c * factor, 1.0) for c in color)


    def darker_color(self, color, factor = 1.1):

        return tuple(c * factor for c in color)


    # Controls color change as risk percentage increases
    def update_progress(self, time_secs):

        if self.progress == self.stop_gap:

            Clock.unschedule(self.update_progress) # Stopping the clock

            return

        self.progress += 1
        self.fading_param = max(0, self.fading_param - 0.01) # color smoothly fades away

        green, yellow, red = (0.18, 0.76, 0.42, 1), (0.95, 0.9, 0.03, 1), (0.835, 0.129, 0.078, 1)

        if self.progress <= 30:

            target_color = self.lerp_color(green, yellow, self.progress / 30)

        else:

            target_color = self.lerp_color(yellow, red, (self.progress - 30) / 70)

        blending_factor = 1 - self.fading_param
        current_color = self.lerp_color(green, target_color, blending_factor)

        bright_bar_color = self.brighten_color(current_color)
        self.bar_color.rgba = (*bright_bar_color, 1)

        dark_bckgrd_color = self.darker_color(current_color)
        self.bckgrd_color.rgba = (*dark_bckgrd_color, 1)

        self.progress_bar.circle = (self.center_x, self.center_y, 100, 0, 360 * (self.progress / 100))
        self.percent_lb.text = f'{self.progress}%'


    # Calls the clock as a new stop limit is set
    def run_progress_clock(self, stop_gap):

        self.progress = 0
        self.stop_gap = stop_gap
        self.fading_param = 1
        
        def reset_canvas(dt): # delta time

            try:

                self.percent_lb.text = f'{self.progress}%'
                self.bckgrd_color.rgba = (0.929, 0.792, 0.004, 1)
                self.bar_color.rgba = (0.929, 0.792, 0.004, 1)
                self.progress_bar.circle = (self.center_x, self.center_y, 100, 0, 0)
            
            except Exception as e:

                print(f"[run_progress_clock] Error resetting canvas: {e}")
        
        Clock.schedule_once(reset_canvas, 0) # Schedules reset_canvas to run on the main Kivy thread on the next screen update

        Clock.schedule_interval(self.update_progress, 0.05)


    def adjust_canvas(self, *args):

        pos = (self.center_x - 100, self.center_y - 100)

        self.bckgrd_circle.pos = pos

        self.track_line.circle = (self.center_x, self.center_y, 100, 0, 360)

        self.progress_bar.circle = (self.center_x, self.center_y, 100, 0, 360 * (self.progress / 100))

        self.percent_lb.pos = (self.center_x - self.percent_lb.width / 2 + 5, self.center_y - self.percent_lb.height / 2)


#--------------Legend Frame------------------\\
class Legend(GridLayout):
    def __init__(self, **kwargs):

        super().__init__(cols = 2, rows = 3, spacing = 20, size_hint = (None, None), size = (180, 120), **kwargs)
        
        self.labels  = dict()

        self.set_circle_lb((0.18, 0.76, 0.42), "green")
        self.set_circle_lb((1.0, 0.89, 0.09), "yellow") 
        self.set_circle_lb((0.835, 0.129, 0.078), "red")


    #---------Methods------\\

    def set_circle_lb(self, color_rgb, key):
        
        circle = Widget(size_hint = (None, None), size = (25, 25))

        with circle.canvas:

            ellipse_color  = Color(*color_rgb, 1)
            ellipse = Ellipse(pos = circle.pos, size = circle.size)

        circle.bind(pos = lambda instance, value: setattr(ellipse, "pos", value))
        circle.bind(size = lambda instance, value: setattr(ellipse, "size", value))

        # Text Label
        label = Label(text = " ", halign = "left", valign = "middle", bold = True, color = (0, 0, 0, 1))
        label.bind(size = label.setter("text_size")) # as label size changes, text size changes too

        self.labels[key] = label

        self.add_widget(circle)
        self.add_widget(label)
    

    def set_lb_text(self, prediction):

        self.labels["red"].text = "Critical"

        if prediction == "Yes":

            self.labels["green"].text = "Stable"
            self.labels["yellow"].text = "Severe"
        
        else:

            self.labels["green"].text = "Healthy"
            self.labels["yellow"].text = "At Risk"


#--------------Input Tables------------------\\
class InputFrame (BoxLayout):

    def __init__(self, title, med_dict, on_done_callback = None, **kwargs):

        super().__init__(orientation = "vertical", padding = 12, size_hint = (None, None), size = (475, 200),  **kwargs)

        with self.canvas:

            self.bckgrd_color = Color(1, 0.980, 0.941, 1)
            self.rect = Rectangle(pos = self.pos, size = self.size)

            self.border_color = Color(0, 0, 0, 1)
            self.border = Line(rectangle = (*self.pos, *self.size), width = 1.5)
        
        self.bind(pos = self.adjust_canvas, size = self.adjust_canvas)

        self.edit_mode = False
        self.widget_types = dict()

        self.title = title
        self.med_dict = med_dict
        self.on_done_callback = on_done_callback 

        self.set_components()


    #---------Methods------\\

    def set_components(self):

        self.clear_widgets()

        header = BoxLayout(orientation = "horizontal", size_hint_y = None, height = 40, padding = (5,0,5,0))
        title_lb = Label(text = self.title, halign = "left", valign = "middle", bold = True, size_hint_x = 0.8, color = (0,0,0,1))
        title_lb.bind(size = title_lb.setter("text_size"))
        header.add_widget(title_lb)

        if self.edit_mode:

            btn_text = "Done"
        
        else:

            btn_text = "Edit"

        edit_button = Button(text = btn_text, size_hint_x = 0.2, background_color = (0,0,0,0), color = (0.2, 0, 0.8, 1))
        edit_button.bind(on_press = self.edit_mode_on)
        header.add_widget(edit_button)

        self.add_widget(header)

        self.table = GridLayout(cols = 4, spacing = 8)

        dict_items = list(self.med_dict.items())

        for i in range(0, len(dict_items), 2):

            for j in range(2):

                if i + j < len(dict_items):

                    lb_name, lb_text = dict_items[i + j]

                    label = Label(text = lb_name + ":", halign = "right", valign = "middle", color = (0,0,0,1), font_size = 22, size_hint_x = None, width = 130)
                    label.bind(size = label.setter("text_size"))
                    self.table.add_widget(label)

                    if self.edit_mode:

                        if lb_name == "Gender":

                            widget = Spinner(text = lb_text, values = ("Male", "Female"), size_hint_y = None, height = 50, font_size = 22, size_hint_x = None, width = 75)

                        elif lb_name in ("Smoke", "Active", "Alcohol"):

                            widget = Spinner(text = lb_text, values = ("Yes", "No"), size_hint_y = None, height = 50, font_size = 22, size_hint_x = None, width = 60)

                        else:

                            widget = TextInput(text = lb_text, multiline = False, size_hint_y = None, height = 50, padding = (3, 5), font_size = 22, size_hint_x = None, width = 73)
                    
                    else:

                        widget = Label(text = lb_text, halign = "left", valign = "middle", color = (0,0,0,1), padding = (3, 5), font_size = 22, size_hint_x = None, width = 78)
                        widget.bind(size = widget.setter("text_size"))

                    self.table.add_widget(widget)
                    self.widget_types[lb_name] = widget
                
                else:

                    self.table.add_widget(Label())
                    self.table.add_widget(Label())

        self.add_widget(self.table)


    def check_input(self, key, input):
            
            input = input.lower().strip()

            if key == "Age":

                try:
                    input = int(input)

                    if input > 0 and input < 101:

                        return True
                    
                    else:

                        return False
                    
                except ValueError:

                    return False

            elif key == "Height(m)":

                try:

                    input = float(input)

                    if input > 0.49 and input < 3.01:

                        return True
                    
                    else:

                        return False
                
                except ValueError:

                    return False

            elif key == "Weight(kg)":

                try:

                    input = int(input)

                    if input > 19 and input < 301:

                        return True
                    
                    else:

                        return False
                
                except ValueError:

                    return False
            
            elif key == "BP(high)" or key == "BP(low)":

                try:

                    input = int(input)

                    if input > 59 and input < 201:

                        return True
                    
                    else:

                        return False
                
                except ValueError:

                    return False
            
            elif key == "Gluc(mg/dL)" or key == "Chol(mg/dL)": # Glucose and Cholesterol

                try:
                    input = int(input)

                    if input > 39 and input < 601:

                        return True
                    
                    else:

                        return False
                    
                except ValueError:

                    return False
            
            else:

                return True
    
    
    def clean_text(self, text):

        text = text.strip()

        text = text[0].upper() + text[1:]
        
        return text


    def edit_mode_on(self, instance):

        if self.edit_mode:

            for key, widget in self.widget_types.items():

                if isinstance(widget, (TextInput, Spinner)) and self.check_input(key, widget.text):

                    self.med_dict[key] = self.clean_text(widget.text)
        
            if self.on_done_callback:

                self.on_done_callback(self.med_dict)

        self.edit_mode = not self.edit_mode

        self.set_components()


    def set_med_dict(self, med_dict):

        for key in med_dict:

            if key in self.med_dict:

                self.med_dict[key] = med_dict[key]

    
    def set_tb_input(self, med_dict):

        self.set_med_dict(med_dict)

        for key, value in self.med_dict.items():

            widget = self.widget_types.get(key)

            if self.check_input(key, value):

                widget.text = value


    def adjust_canvas(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.rectangle = (*self.pos, *self.size)


#--------------Navigation Bar------------------\\
class NavBar(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(orientation = "horizontal", size_hint = (1, None), height = 90, **kwargs)

        with self.canvas:

            self.rect_color = Color(1, 0.980, 0.941, 1)
            self.nav_rect = Rectangle(size = self.size, pos = self.pos)

            self.border_color = Color(0, 0, 0, 1)
            self.nav_top_border = Line(points = [self.x, self.top, self.right, self.top], width = 1.5)

        self.bind(size = self.adjust_canvas, pos = self.adjust_canvas)


    def adjust_canvas(self, instance, value):

        self.nav_rect.size = instance.size
        self.nav_rect.pos = instance.pos

        x = instance.x
        y = instance.top
        width = instance.width
        self.nav_top_border.points = [x, y, x + width, y]


#--------------Navigation Button------------------\\
class NavButton(ButtonBehavior, BoxLayout):

    def __init__(self, screen_title, img_src, active_img_src, change_screen_callback = None, **kwargs):

        super().__init__(orientation = "vertical", padding = 10, size_hint_y = None, height = 90, **kwargs)

        self.screen_title = screen_title
        self.img_src = img_src
        self.active_img_src = active_img_src
        self.change_screen_callback = change_screen_callback

        self.image_widget = Image(source = self.img_src, size_hint_y = 0.6)
        self.btn_lb = Label(text = self.screen_title, font_size = 20, bold = True, size_hint_y = 0.4, color = (0, 0, 0, 1))

        self.add_widget(self.image_widget)
        self.add_widget(self.btn_lb)


    #---------Methods------\\

    def set_active(self, active):

        if active:

            self.image_widget.source = self.active_img_src
            self.btn_lb.color = (0.004, 0.624, 0.902, 1)
        
        else:

            self.image_widget.source = self.img_src
            self.btn_lb.color = (0, 0, 0, 1)


    def on_press(self):

        if self.change_screen_callback:

            self.change_screen_callback(self.screen_title)   