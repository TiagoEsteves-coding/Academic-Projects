
#BMI needs to be updated everytime Height and/or Weight changes
#Blood Pressure Category needs to be updated everytime ap_hi and/or ap_lo changes

class Patient:

#When inserting a new Patient and fetching data from a File
    def __init__(self,details = None):

        if(details is not None and len(details)!=0):
          
          self.id = details[0]
          self.firstname = details[1]
          self.lastname = details[2]
          self.age = details[3]
          self.gender = details[4]
          self.height = details[5]
          self.weight = details [6]

          self.active = details[8]
          self.smoking = details [9]
          self.alcohol = details [10]
          
          self.cholvl = details[11]
          self.gluclvl = details[12]
          self.ap_hi = details[13]
          self.ap_lo = details[14]

          if(len(details)>15): #Fetching from the File
             
             self.bmi = details[7]
             self.bp_cat = details[15]
             self.heartdis = details[16]
             self.heartper = details[17]

          else:          #Inserting new patient
             
             self.bp_cat = ''
             self.bmi = 0
             self.heartdis = '-'
             self.heartper = '-'
             self.set_BMI()
             self.set_BP_category()

#Getter and Setter methods for ID variable
    def set_id (self, id):

        self.id = id

    def get_id (self):

        return self.id

#Getter and Setter methods for First Name variable
    def set_firstname (self, firstname):

        self.firstname = firstname

    def get_firstname (self):

        return self.firstname
    
#Getter and Setter methods for Last Name variable
    def set_lastname (self, lastname):

        self.firstname = lastname

    def get_lastname (self):

        return self.lastname
    
#Getter and Setter methods for Age variable
    def set_age (self, age):

        self.age = age

    def get_age (self):

        return self.age
    
#Getter and Setter methods for Gender variable
    def set_gender (self, gender):

        self.gender = gender

    def get_gender (self):

        return self.gender
    
#Getter and Setter methods for Height variable
    def set_height (self, height):

        self.height = height

    def get_height (self):

        return self.height
    
#Getter and Setter methods for Weight variable
    def set_weight (self, weight):

        self.weight= weight

    def get_weight (self):

        return self.weight
    
#Getter and Setter methods for Smoking variable
    def set_smoking (self, smoking):

        self.smoking = smoking

    def get_smoking (self):

        return self.smoking
    
#Getter and Setter methods for Alcohol variable
    def set_alcohol (self, alcohol):

        self.alcohol = alcohol

    def get_alcohol (self):

        return self.alcohol

#Getter and Setter methods for Active variable
    def set_active (self, active):

        self.active = active

    def get_active (self):

        return self.active    

#Getter and Setter methods for Chlosterol Level variable
    def set_cholvl (self, cholvl):

        self.cholvl = cholvl

    def get_cholvl (self):

        return self.cholvl

#Getter and Setter methods for Glucose Level variable
    def set_gluclvl (self, gluclvl):

        self.gluclvl = gluclvl

    def get_gluclvl (self):

        return self.gluclvl

#Getter and Setter methods for Systolic Blood Pressure variable
    def set_ap_hi (self, ap_hi):

        self.ap_hi = ap_hi

    def get_ap_hi (self):

        return self.ap_hi
    
#Getter and Setter methods for Diastolic Blood Pressure variable
    def set_ap_lo (self, ap_lo):

        self.ap_lo = ap_lo

    def get_ap_lo (self):

        return self.ap_lo
    
#Getter and Setter methods for Heart Disease variable
    def set_heartdis (self, heartdis):

        self.heartdis = heartdis

    def get_heartdis (self):

        return self.heartdis
    
#Getter and Setter methods for Heart Disease Prediction variable
    def set_heartper (self, heartper):

        self.heartper = heartper

    def get_heartper (self):

        return self.heartper

#Setting BMI based on height and weight
    def set_BMI (self):
         
         weight = float(self.weight)
         height = self.height

         while(round(height/10)!=0):

           height = height/10
            
         self.bmi = round(weight/(height**2),8)

#Getter method for BMI variable
    def get_BMI (self):

        return self.bmi
    
#Checking the category that Systolic BP falls under
    def private_check_ap_hi (self):

        level = 0

        if(self.ap_hi<120):

            level = 1

        elif((self.ap_hi>=120 and self.ap_hi<129)):

            level = 2

        elif((self.ap_hi>=130 and self.ap_hi<139)):

            level = 3

        elif((self.ap_hi>=140 and self.ap_hi<180)):

            level = 4

        else:

            level = 5

        return level
    
#Checking the category that Diastolic BP falls under
    def private_check_ap_lo (self):

        level = 0

        if(self.ap_lo<80):

            level = 1

        elif(self.ap_lo>=80 and self.ap_lo<90):

            level = 3

        elif(self.ap_lo>=90 and self.ap_lo<120):

            level = 4

        else:

            level = 5

        return level

#Setting BP_category based on ap_li and ap_lo
    def set_BP_category (self):

        level_hi = self.private_check_ap_hi()
        level_lo = self.private_check_ap_lo()
        level_val = 0

        if(level_hi>level_lo):

            level_val = level_hi

        else:

            level_val = level_lo

        if(level_val == 1):

            self.bp_cat = 'Normal'

        elif(level_val == 2):

            self.bp_cat = 'Elevated'

        elif(level_val== 3):

            self.bp_cat = 'Hypertension Stage 1'

        elif(level_val == 4):

            self.bp_cat = 'Hypertension Stage 2'

        else:

            self.bp_cat = 'Hypertensive Crisis'

#Getter method for Blood Pressure Category
    def get_BP_category (self):
        
        return self.bp_cat

#Getter method for all the details of a patient
    def get_patientInfo (self):

        patient_info = []
        patient_info.append(self.id)
        patient_info.append(self.firstname)
        patient_info.append(self.lastname)
        patient_info.append(self.age)
        patient_info.append(self.gender)
        patient_info.append(self.height)
        patient_info.append(self.weight)
        patient_info.append(self.bmi)
        patient_info.append(self.active)
        patient_info.append(self.smoking)
        patient_info.append(self.alcohol)
        patient_info.append(self.cholvl)
        patient_info.append(self.gluclvl)
        patient_info.append(self.ap_hi)
        patient_info.append(self.ap_lo)
        patient_info.append(self.bp_cat)
        patient_info.append(self.heartdis)
        patient_info.append(self.heartper)

        return patient_info



    



