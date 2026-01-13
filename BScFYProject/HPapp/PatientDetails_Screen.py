from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import ANN_Model
import Patient
import DataFileManager

class PatientDetails_Screen :
    
    def __init__(self,parent,patient_list,data_manager,index):

      # Back-End Properties/Variables
        self.patient_list = patient_list
        self.data_manager = data_manager
        self.index = index
        self.model = ANN_Model.ANN_Model(data_manager)


      # GUI Properties for Widgets
        backcolour = 'floralwhite' # Setting Background Colour for Labels, etc.
        style = ttk.Style()
        style.configure('TFrame', background=backcolour) # Setting Background Colour for Frames
        style.configure('Treeview', font= ('Calibri',11)) # Setting properties for Treeview
        style.configure('Treeview.Heading',font = ('Calibri',12),padding = (0,8)) # Setting properties for Treeview.Headings


      # Background Canvas (Panel)
        self.canvas = Canvas(parent, width=1366, height=768)
        self.canvas.pack()
        self.canvas.config(background='floralwhite') # Setting Canvas Background Colour

        # Drawing line separating the Header from the Body
        self.canvas.create_line(0,130,1366,130, fill='#2696d8', width=3)

        # Drawing line separating the Body Section
        self.canvas.create_line(970,130,970,768, fill='lightsteelblue', width=1)


#--------------------------Header of the Screen------------------------
        
      #-------------Left Side of the Header------------------
        
        logo = ImageTk.PhotoImage(Image.open('Images\\HeartSeer_Logo.png')) # App Logo

        # Label Properties
        self.label_logo = ttk.Label(self.canvas, image = logo)
        self.label_logo.image = logo

        self.label_logo.config(background=backcolour)

        self.label_logo.place(x=10, y=6)

        
      #-------------Right Side of the Header------------------
        
        profile_icon = ImageTk.PhotoImage(Image.open('Images\\profile_icon.png')) #Profile Icon

        # Label Properties
        self.label_username = ttk.Label(self.canvas, text='Username', image = profile_icon)
        self.label_username.image = profile_icon

        self.label_username.config(font=('Calibri',16))
        self.label_username.config(compound=LEFT)
        self.label_username.config(background=backcolour)

        self.label_username.place(x=1070,y=6)


#--------------------------Body of the Screen------------------------

      #-------------Left Side of the Body------------------
        

        #----Patient ID Label----
        self.label_ID = ttk.Label (self.canvas, text = 'ID')
        self.label_patientID = ttk.Label(self.canvas, text = self.index)

         # Label Properties
        self.label_ID.config (font=('Calibri', 16,'italic'))
        self.label_ID.config (background=backcolour)

        self.label_patientID.config(font = ('Calibri', 15) )
        self.label_patientID.config(background=backcolour)

        self.label_ID.place(x=35, y=180)
        self.label_patientID.place(x=35,y=210)


        #----Patient Name Label----
        self.label_name = ttk.Label(self.canvas,text='Name')
        self.label_patientName = ttk.Label(self.canvas,text=f'{self.patient_list[self.index].get_firstname()} {self.patient_list[self.index].get_lastname()}') 

         # Label Properties
        self.label_name.config(font = ('Calibri', 16, 'italic'))
        self.label_name.config(background=backcolour)

        self.label_patientName.config(font = ('Calibri', 15))
        self.label_patientName.config(background=backcolour)

        self.label_name.place(x = 65, y = 180)
        self.label_patientName.place(x=65,y=210)



        #----Frame containing the Tables with Patient Health Parameters----
        self.frame_tables = ttk.Frame(self.canvas)

        self.frame_tables.place(x=20,y=300)


        #----Top Treeview with Patient Health Parameters----
        self.table1 = ttk.Treeview(self.frame_tables, columns=('Age','Gender','Height','Weight','BMI','Active'), show='headings',height=2)

         # Age -> Heading Properties
        self.table1.heading('Age',text ='Age')
        self.table1.column('Age',width=50,anchor='center')

         # Gender -> Heading Properties
        self.table1.heading('Gender',text ='Gender')
        self.table1.column('Gender',width=75,anchor='center')

         # Height -> Heading Properties
        self.table1.heading('Height',text ='Height')
        self.table1.column('Height',width=75,anchor='center')

         # Weight -> Heading Properties
        self.table1.heading('Weight',text ='Weight')
        self.table1.column('Weight',width=75,anchor='center')

         # BMI -> Heading Properties
        self.table1.heading('BMI',text ='BMI')
        self.table1.column('BMI',width=140,anchor='center')

         # Active -> Heading Properties
        self.table1.heading('Active',text ='Active')
        self.table1.column('Active',width=75,anchor='center')


         # Inserting respective values below each of the headings
        self.table1.insert(parent='',index =0,values=(self.patient_list[self.index].get_age(),
                                                      self.patient_list[self.index].get_gender(),
                                                      self.patient_list[self.index].get_height(),
                                                      self.patient_list[self.index].get_weight(),
                                                      self.patient_list[self.index].get_BMI(),
                                                      self.patient_list[self.index].get_active()))
        

        #----Bottom Treeview with Patient Health Parameters----
        self.table2 = ttk.Treeview(self.frame_tables, columns=('Smoking','Alcohol','Chol lvl','Gluc lvl','Systolic BP','Diastolic BP','BP Category'),show='headings',height=2)

         # Smoking -> Heading Properties
        self.table2.heading('Smoking',text ='Smoking')
        self.table2.column('Smoking',width=75,anchor='center')

         # Alcohol -> Heading Properties
        self.table2.heading('Alcohol',text ='Alcohol')
        self.table2.column('Alcohol',width=75,anchor='center')

         # Cholesterol -> Heading Properties
        self.table2.heading('Chol lvl',text ='Chol lvl')
        self.table2.column('Chol lvl',width=75,anchor='center')

         # Glucose -> Heading Properties
        self.table2.heading('Gluc lvl',text ='Gluc lvl')
        self.table2.column('Gluc lvl',width=75,anchor='center')

         # Systolic Blood Pressure -> Heading Properties
        self.table2.heading('Systolic BP',text ='Systolic BP')
        self.table2.column('Systolic BP',width=100,anchor='center')

         # Diastolic Blood Pressure -> Heading Properties
        self.table2.heading('Diastolic BP',text ='Diastolic BP')
        self.table2.column('Diastolic BP',width=100,anchor='center')

         # Blood Pressure Category -> Heading Properties
        self.table2.heading('BP Category',text ='BP Category')
        self.table2.column('BP Category',width=140,anchor='center')


         # Inserting respective values below each of the headings
        self.table2.insert(parent='',index =0,values=(self.patient_list[self.index].get_smoking(),
                                                      self.patient_list[self.index].get_alcohol(),
                                                      self.patient_list[self.index].get_cholvl(),
                                                      self.patient_list[self.index].get_gluclvl(),
                                                      self.patient_list[self.index].get_ap_hi(),
                                                      self.patient_list[self.index].get_ap_lo(),
                                                      self.patient_list[self.index].get_BP_category()))
        
        # Treeviews Positioning on the Frame
        self.table1.grid(row=0,column=0,padx=(0, 10),pady=10)
        self.table2.grid(row=1,column=0, padx=(0, 10), pady=10)

        self.table1.bind('<Double-1>',self.on_double_click_table1)
        self.table2.bind('<Double-1>', self.on_double_click_table2)

        #'Edit' Button to edit the table with patient data
        self.edit = ttk.Button(self.canvas,text='Edit')
        self.edit.config(command = self.edit_button)
        self.edit.place(x=490,y=490)
        self.edit_button_clicked = False

        #'Save' Button to save the changes on the table with patient data
        self.save = ttk.Button(self.canvas,text='Save')
        self.save.config(command = self.save_button)
        self.save.place(x=585,y=490)

        #'Delete' Button to delete a patient
        self.delete = ttk.Button(self.canvas,text='Delete')
        self.delete.config(command = self.delete_button)
        self.delete.place(x=20,y=490)


        #----Frame containing the Buttons to navigate through the List of Patients----
        self.frame_nav = ttk.Frame(self.canvas)

        self.frame_nav.place(x=580,y=550)


        # Label Separating Both 'Previous' & 'Next' Buttons
        self.label_seperator = ttk.Label(self.frame_nav, text='/')

         # Label Properties
        self.label_seperator.config(padding = (10,10))
        self.label_seperator.config(background=backcolour)

        self.label_seperator.grid(row=0,column=1)


        #'Previous' Button to move to the previous Patient
        self.previous = ttk.Button(self.frame_nav,text='Previous')

         #Button Properties
        self.previous.config(command = self.previous_button) # Command upon click
        
        self.previous.grid(row=0, column=0)


        # 'Next' Button to move on to the next Patient
        self.next = ttk.Button(self.frame_nav,text='Next')

         #Button Properties
        self.next.config(command = self.next_button) # Command upon click

        self.next.grid(row=0,column=2)


      #-------------Right Side of the Body------------------
        
        #----Frame containing the Accuracy/Heart Disease Ans/Probability Labels
        self.frame_pred = ttk.Frame(self.canvas)
         
         # Frame Properties
        self.frame_pred.config(style='TFrame')

        self.frame_pred.place(x=1035,y=200)


        #----Heart Disease Probability Label----
        self.label_pro = ttk.Label(self.frame_pred,text=f'Heart Prediction\n(%)\n\n{self.patient_list[self.index].get_heartper()}%')

         #Label Properties
        self.label_pro.config(font=('Calibri',12))
        self.label_pro.config(justify=CENTER)
        self.label_pro.config(background=backcolour)


        #----Heart Disease Prediction Label----
        self.label_hdpred = ttk.Label(self.frame_pred,text=f'Heart Disease\n(Yes/No)\n\n{self.patient_list[self.index].get_heartdis()}')

         # Label Properties
        self.label_hdpred.config(font=('Calibri',12))
        self.label_hdpred.config(justify=CENTER)
        self.label_hdpred.config(background=backcolour)


        #----AI Model Accuracy Label----
        self.label_accuracy = ttk.Label(self.frame_pred,text=f'Accuracy\n(%)\n\n{self.model.get_accuracy()}%')

         # Label Properties
        self.label_accuracy.config(font=('Calibri',12))
        self.label_accuracy.config(justify=CENTER)
        self.label_accuracy.config(background=backcolour)


        #----'Train' Button to train and evaluate the AI Model for 1 epoch----
        self.train = ttk.Button(self.frame_pred,text = 'Train Model')
        
         # Button Properties
        self.train.config(command = self.train_button) # Command upon click


        #----'Predict' Button to predict Heart Disease of a Patient----
        self.predict = ttk.Button(self.frame_pred,text='Predict')

         # Button Properties
        self.predict.config(command = self.predict_button)

        
        # Labels Positioning on the Frame
        self.label_pro.grid(row=0,column=1, padx=(0, 10),pady=10)
        self.label_hdpred.grid(row=1,column=1, padx=(0, 10),pady=10)
        self.label_accuracy.grid(row=1,column=0, padx=(0, 10),pady=10)

        # Buttons Positioning on the Frame
        self.train.grid(row=2,column=0,padx=(0, 10),pady=10)
        self.predict.grid(row=2,column=1,padx=(0, 10),pady=10)



#--------------------------Methods of the Class------------------------
    def edit_button (self):

        if (self.edit_button_clicked == True):
            return
        
        self.edit_button_clicked = True

        self.entry_list = []

        selected_iid = 'I001'

        selected_values = self.table1.item(selected_iid)

        for column_index in range(0,6):

            if(column_index != 4):

             column = '#' + str(column_index+1)

             selected_text = selected_values.get('values') [column_index]

             column_box = self.table1.bbox(selected_iid, column)
             print(column_box)

             entry_edit = ttk.Entry(self.table1)
             entry_edit.editing_column_index = column_index
             entry_edit.editing_item_iid = selected_iid

             entry_edit.insert(0,selected_text)
             entry_edit.select_range(0, END)

             entry_edit.focus()

             #entry_edit.bind('<FocusOut>',self.on_focus_out)

             entry_edit.place(x=column_box[0],y=column_box[1],w=column_box[2],h=column_box[3])
             self.entry_list.append(entry_edit)

        print(column_index)

        selected_values = self.table2.item(selected_iid)

        for column_index in range(0,7):

            if(column_index != 6):

             column = '#' + str(column_index+1)

             selected_text = selected_values.get('values') [column_index]

             column_box = self.table2.bbox(selected_iid, column)
             print(column_box)

             entry_edit = ttk.Entry(self.table2)
             entry_edit.editing_column_index = column_index
             entry_edit.editing_item_iid = selected_iid

             entry_edit.insert(0,selected_text)
             entry_edit.select_range(0, END)

             entry_edit.focus()

             #entry_edit.bind('<FocusOut>',self.on_focus_out)

             entry_edit.place(x=column_box[0],y=column_box[1],w=column_box[2],h=column_box[3])
             self.entry_list.append(entry_edit)
             #print(self.entry_list)


    def save_button (self):

        if(self.edit_button_clicked == False):
            return
    
        selected_iid = self.entry_list[0].editing_item_iid

        for i in range(0,len(self.entry_list)):

            new_text = self.entry_list[i].get()
            print('newtext=',new_text)

            column_index = self.entry_list[i].editing_column_index

            if(i < 5):

                if(self.check_table1Data(column_index,new_text)==True):
                   
                   new_text = self.upper_firstletter(new_text)

                   current_values_table1 = self.table1.item(selected_iid).get('values')
                   current_values_table1[column_index] = new_text
                   self.table1.item(selected_iid,values=current_values_table1)

            else:
                if(self.check_table2Data(column_index,new_text) == True):

                    new_text = self.upper_firstletter(new_text)

                    current_values_table2 = self.table2.item(selected_iid).get('values')
                    current_values_table2[column_index] = new_text
                    self.table2.item(selected_iid,values=current_values_table2)

            self.entry_list[i].destroy()

        current_values_table1 = self.table1.item(selected_iid, 'values')
        current_values_table2 = self.table2.item(selected_iid, 'values')

        self.patient_list[self.index].set_age(int(current_values_table1[0]))
        self.patient_list[self.index].set_gender(current_values_table1[1])
        self.patient_list[self.index].set_height(float(current_values_table1[2]))
        self.patient_list[self.index].set_weight(current_values_table1[3])
        self.patient_list[self.index].set_BMI()
        self.table1.item(selected_iid, values=current_values_table1[:4] + (self.patient_list[self.index].get_BMI(),) + current_values_table1[5:])
        self.patient_list[self.index].set_active(current_values_table1[5])

        self.patient_list[self.index].set_smoking(current_values_table2[0])
        self.patient_list[self.index].set_alcohol(current_values_table2[1])
        self.patient_list[self.index].set_cholvl(int(current_values_table2[2]))
        self.patient_list[self.index].set_gluclvl(int(current_values_table2[3]))
        self.patient_list[self.index].set_ap_hi(int(current_values_table2[4]))
        self.patient_list[self.index].set_ap_lo(int(current_values_table2[5]))
        self.patient_list[self.index].set_BP_category()
        self.table2.item(selected_iid, values=current_values_table2[:6] + (self.patient_list[self.index].get_BP_category(),))

        # Updating the data of a Patient in the Patients File
        self.data_manager.update_PatientData(self.patient_list[self.index])
        self.edit_button_clicked = False
        self.table1.selection_remove(self.table1.selection())
        self.table2.selection_remove(self.table2.selection())
    

    def delete_button(self):
        answer = messagebox.askquestion('System Warning', 'Do you want to proceed?')

        if(answer == 'yes'):
            del self.patient_list [self.index]
            self.data_manager.remove_Patient(self.index)

            for i in range (0, len(self.patient_list)):

                self.patient_list[i].set_id(i)

            self.previous_button()

        else:
            print('Message Box closed.')
        
        
    def on_double_click_table1(self,event):
       
       # Identify the region that was Double-clicked
       region_clicked = self.table1.identify_region(event.x, event.y)

       # Here we're only interested in tree and cell
       if region_clicked not in ('tree','cell'):
           return
       
       # Which item was double-clicked
       column =  self.table1.identify_column(event.x)

       # For example, '#0' will become -1, '#1' will become 0 etc.
       column_index = int(column[1:]) - 1

       if(column_index == 4):
           return

       # For example: 001
       selected_iid = self.table1.focus()

       # This will contain both text and values from the given item iid
       selected_values = self.table1.item(selected_iid)

       if column == '#0':
           selected_text = selected_values.get('text')
       else:
           selected_text = selected_values.get('values') [column_index]

       column_box = self.table1.bbox(selected_iid, column)
       print(column_box)

       entry_edit = ttk.Entry(self.table1)

       # Record column index and item iid
       entry_edit.editing_column_index = column_index
       entry_edit.editing_item_iid = selected_iid

       entry_edit.insert(0,selected_text)
       entry_edit.select_range(0, END)

       entry_edit.focus()

       entry_edit.bind('<FocusOut>',self.on_focus_out)
       entry_edit.bind('<Return>',self.on_enter_pressed_table1)

       entry_edit.place(x=column_box[0],y=column_box[1],w=column_box[2],h=column_box[3])


    def on_double_click_table2(self,event):
       
       # Identify the region that was Double-clicked
       region_clicked = self.table2.identify_region(event.x, event.y)

       # Here we're only interested in tree and cell
       if region_clicked not in ('tree','cell'):
           return
       
       # Which item was double-clicked
       column =  self.table2.identify_column(event.x)

       # For example, '#0' will become -1, '#1' will become 0 etc.
       column_index = int(column[1:]) - 1

       if(column_index == 6):
           return

       # For example: 001
       selected_iid = self.table2.focus()

       # This will contain both text and values from the given item iid
       selected_values = self.table2.item(selected_iid)

       if column == '#0':
           selected_text = selected_values.get('text')
       else:
           selected_text = selected_values.get('values') [column_index]

       column_box = self.table2.bbox(selected_iid, column)
       print(column_box)

       entry_edit = ttk.Entry(self.table2)

       # Record column index and item iid
       entry_edit.editing_column_index = column_index
       entry_edit.editing_item_iid = selected_iid

       entry_edit.insert(0,selected_text)
       entry_edit.select_range(0, END)

       entry_edit.focus()

       entry_edit.bind('<FocusOut>',self.on_focus_out)
       entry_edit.bind('<Return>',self.on_enter_pressed_table2)

       entry_edit.place(x=column_box[0],y=column_box[1],w=column_box[2],h=column_box[3])
       

    def on_enter_pressed_table1(self,event):
        new_text = event.widget.get()

        # such as I001
        selected_iid = event.widget.editing_item_iid

        # such as -1 (tree column), 0 (first self-defined column), etc.
        column_index = event.widget.editing_column_index


        if(self.check_table1Data(column_index,new_text) == True):

            new_text = self.upper_firstletter(new_text)

            current_values = self.table1.item(selected_iid).get('values')
            current_values[column_index] = new_text
            self.table1.item(selected_iid,values=current_values)

            current_values = self.table1.item(selected_iid, 'values')

            if(column_index == 0):
               
               self.patient_list[self.index].set_age(int(current_values[column_index]))

            elif(column_index == 1):

               self.patient_list[self.index].set_gender(current_values[column_index])

            elif(column_index == 2):

               self.patient_list[self.index].set_height(float(current_values[column_index]))
               self.patient_list[self.index].set_BMI()
               self.table1.item(selected_iid, values=current_values[:4] + (self.patient_list[self.index].get_BMI(),) + current_values[5:])

            elif(column_index == 3):

               self.patient_list[self.index].set_weight(int(current_values[column_index]))
               self.patient_list[self.index].set_BMI()
               self.table1.item(selected_iid, values=current_values[:4] + (self.patient_list[self.index].get_BMI(),) + current_values[5:])

            else:
               self.patient_list[self.index].set_active(current_values[column_index])

        # Updating the data of a Patient in the Patients File
            self.data_manager.update_PatientData(self.patient_list[self.index])

        else:
            messagebox.showinfo('System Warning', 'Inserted data not accepted!')

        event.widget.destroy()
        self.table1.selection_remove(self.table1.selection())


    def on_enter_pressed_table2(self,event):
        new_text = event.widget.get()

        # such as I002
        selected_iid = event.widget.editing_item_iid

        # such as -1 (tree column), 0 (first self-defined column), etc.
        column_index = event.widget.editing_column_index

        if(self.check_table2Data(column_index ,new_text) == True):

            new_text = self.upper_firstletter(new_text)

            current_values = self.table2.item(selected_iid).get('values')
            current_values[column_index] = new_text
            self.table2.item(selected_iid,values=current_values)

            current_values = self.table2.item(selected_iid, 'values')

            if(column_index == 0):
                
                self.patient_list[self.index].set_smoking(current_values[column_index])

            elif(column_index == 1):

                self.patient_list[self.index].set_alcohol(current_values[column_index])

            elif(column_index == 2):

                self.patient_list[self.index].set_cholvl(int(current_values[column_index]))

            elif(column_index == 3):

                self.patient_list[self.index].set_gluclvl(int(current_values[column_index]))

            elif(column_index == 4):

                self.patient_list[self.index].set_ap_hi(int(current_values[column_index]))
                self.patient_list[self.index].set_BP_category()
                self.table2.item(selected_iid, values=current_values[:6] + (self.patient_list[self.index].get_BP_category(),))
        
            else:

                self.patient_list[self.index].set_ap_lo(int(current_values[column_index]))
                self.patient_list[self.index].set_BP_category()
                self.table2.item(selected_iid, values=current_values[:6] + (self.patient_list[self.index].get_BP_category(),))

            # Updating the data of a Patient in the Patients File
            self.data_manager.update_PatientData(self.patient_list[self.index])

        else:
            messagebox.showinfo('System Warning', 'Inserted data not accepted!')

        event.widget.destroy()
        self.table2.selection_remove(self.table2.selection())


    def on_focus_out(self, event):
        event.widget.destroy()
        self.table1.selection_remove(self.table1.selection())
        self.table2.selection_remove(self.table2.selection())


    def upper_firstletter (self, text):

        if(len(text)!=0 and len(text)!=1):

           text = text[0].upper() + text[1:]

        return text
    
    
    def check_table1Data(self, index, text):
        text = text.lower()

        if(index == 0):
            try:
                number = int(text)
                if(number > 0 and number <101):
                    return True
                else:
                    return False
                
            except ValueError:
                return False
                    
        elif(index == 1):

            if(text == 'female' or text == 'male'):
                return True
            else:
                return False
            
        elif(index == 2):

            try:
                number = float(text)
                if(number > 0.50 and number <3.00):
                    return True
                else:
                    return False
                
            except ValueError:
                return False

        elif (index == 3):

            try:
                number = int(text)
                if(number > 0 and number <300):
                    return True
                else:
                    return False
                
            except ValueError:
                return False

        else:

            if(text == 'yes' or text == 'no'):
                return True
            else:
                return False

            
    def check_table2Data (self, index, text):
        text = text.lower()

        if(index == 0 or index == 1):

            if(text == 'no' or text == 'yes'):
                return True
            else:
                return False

        elif(index == 2 or index == 3):

            if(text == '1' or text == '2' or text == '3'):
                return True
            else:
                return False
        else:
            try:
                number = int(text)
                if(number > 60 and number < 200):
                    return True
                else:
                    return False
                
            except ValueError:
                return False


    # Defining Command for 'Previous' Button
    def previous_button(self):

        if(self.index==-(len(self.patient_list)-1)): # When index = -4, resets back to 1
            self.index = 1

        self.index = self.index - 1 # Decreases index upon clicking
        
        # Updating Patient ID Label when switching to another Patient
        self.label_patientID.config(text = self.patient_list[self.index].get_id())

        # Updating Patient Name Label when switching to another Patient
        self.label_patientName.config(text=f'{self.patient_list[self.index].get_firstname()} {self.patient_list[self.index].get_lastname()}')

        # Updating Heart Disease Ans Label when switching to another Patient
        self.label_hdpred.config(text=f'Heart Disease\n(Yes/No)\n\n{self.patient_list[self.index].get_heartdis()}')

        # Updating Heart Disease Probability Label when switching to another Patient
        self.label_pro.config(text=f'Heart Prediction\n(%)\n\n{self.patient_list[self.index].get_heartper()}%')

        self.update_tables() # Updating health parameters upon switching to another Patient


    # Defining Command for 'Previous' Button
    def next_button(self):

        if(self.index==len(self.patient_list)-1): # When index = 4, resets back to -1
          self.index = -1

        self.index = self.index + 1 # Increases id upon clicking

        # Updating Patient ID Label when switching to another Patient
        self.label_patientID.config(text = self.patient_list[self.index].get_id())

        # Updating Patient Name Label when switching to another Patient
        self.label_patientName.config(text=f'{self.patient_list[self.index].get_firstname()} {self.patient_list[self.index].get_lastname()}')

        # Updating Heart Disease Ans Label when switching to another Patient
        self.label_hdpred.config(text=f'Heart Disease\n(Yes/No)\n\n{self.patient_list[self.index].get_heartdis()}')

        # Updating Heart Disease Probability Label when switching to another Patient
        self.label_pro.config(text=f'Heart Prediction\n(%)\n\n{self.patient_list[self.index].get_heartper()}%')

        self.update_tables() # Updating health parameters upon switching to another Patient
 

    # Updating Health Parameters Tables upon switching to another Patient
    def update_tables(self):

        i = self.table1.get_children()

        for item in i: # Changing all children from root item
            self.table1.item(item, text='Line1', values=(self.patient_list[self.index].get_age(),
                                                        self.patient_list[self.index].get_gender(),
                                                        self.patient_list[self.index].get_height(),
                                                        self.patient_list[self.index].get_weight(),
                                                        self.patient_list[self.index].get_BMI(),
                                                        self.patient_list[self.index].get_active()))
            
            self.table2.item(item, text='Line1', values=(self.patient_list[self.index].get_smoking(),
                                                         self.patient_list[self.index].get_alcohol(),
                                                         self.patient_list[self.index].get_cholvl(),
                                                         self.patient_list[self.index].get_gluclvl(),
                                                         self.patient_list[self.index].get_ap_hi(),
                                                         self.patient_list[self.index].get_ap_lo(),
                                                         self.patient_list[self.index].get_BP_category()))


    # Training and Evaluating AI Model
    def train_button(self):

        self.model.train_model(1) # Training AI ANN

        self.model.test_accuracy() # Testing its accuracy

        # Displaying AI Model Accuracy on the Accuracy Label
        self.label_accuracy.config(text=f'Accuracy\n(%)\n\n{self.model.get_accuracy()}%')


    # Predicting if a Patient has Heart Disease 
    def predict_button(self):

        if(self.model.get_accuracy()==0):
            messagebox.showinfo('System Warning', 'AI Model has not been trained yet!')
            return

        self.model.predict_HD(self.index)

        # Setting Patient Class Variable to the predicted value
        self.patient_list[self.index].set_heartdis(self.model.get_heartdis_ans())
        
        # Calculating Heart Disease Probability if ans is 'No'
        self.model.calculate_percentage(self.patient_list[self.index])
        
        # Updating Heart Disease Ans Label according to the predicted value
        self.label_hdpred.config(text=f'Heart Disease\n(Yes/No)\n\n{self.patient_list[self.index].get_heartdis()}')

        # Updating Heart Disease Probability Label according to the calculated percentage
        self.label_pro.config(text=f'Heart Prediction\n(%)\n\n{self.patient_list[self.index].get_heartper()}%')

        # Updating the data of a Patient in the Patients File
        self.data_manager.update_PatientData(self.patient_list[self.index])



def desktop_window_size (window):
    window_width = 1366
    window_height = 768
    window.geometry(f"{window_width}x{window_height}")

def main():
    data_manager = DataFileManager.DataFileManager()
    patient_dataframe = data_manager.get_PatientsData()
    patient_list = []

    for i in range(0,patient_dataframe.shape[0]):
        array_info = patient_dataframe.iloc[i].values
        patient = Patient.Patient(array_info)
        patient_list.append(patient)

    root = Tk()
    root.title('Heart Seer')
    desktop_window_size(root)
    app = PatientDetails_Screen(root,patient_list,data_manager,0)
    root.mainloop()
   
    
if __name__ == "__main__": main()


'''def adapt_window_size(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set the window size based on a percentage of the screen size
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    # Set the window position to be centered on the screen
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")'''