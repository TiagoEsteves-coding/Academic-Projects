class UserAccount:

    def __init__(self, first_name = None, surname = None, password = None, email = None):

        self.firstname = first_name
        self.surname = surname
        self.password = password
        self.email = email
        
        self.cvd_risk = 0
        self.cvd_out = "No"

        self.med_params = {
            "Chol(mg/dL)": "Nan",
            "Gluc(mg/dL)": "Nan",
            "Height(m)": "Nan",
            "Weight(kg)": "Nan",
            "Gender": "Nan",
            "BP(high)": "Nan",
            "BP(low)": "Nan",
            "Smoke": "Nan",
            "Alcohol": "Nan",
            "Active": "Nan",
            "Age": "Nan",
            "BMI": 0,
            "BP_elevated": 0,
            "BP_st1": 0,
            "BP_st2": 0,
            "BP_normal": 0,
            "Chol_bv_normal": 0,
            "Chol_normal": 0,
            "Chol_well_bv_normal": 0,
            "Gluc_bv_normal": 0,
            "Gluc_normal": 0,
            "Gluc_well_bv_normal": 0,
            }
    
    #---------Methods------\\

    # Getting the category that Systolic BP(hi) falls under
    def get_bplvl_hi (self):

        try:

            ap_hi = int(self.med_params["BP(high)"])

        except ValueError:

            return None

        level = 0

        if ap_hi < 120:

            level = 1

        elif ap_hi >= 120 and ap_hi < 129:

            level = 2

        elif ap_hi >= 130 and ap_hi < 139:

            level = 3

        elif ap_hi >= 140 and ap_hi < 180:

            level = 4

        else:

            level = 5

        return level
    

    # Getting the category that Diastolic BP(lo) falls under
    def get_bplvl_lo (self):

        try:

            ap_lo = int(self.med_params["BP(low)"])

        except ValueError:

            return None

        level = 0

        if ap_lo < 80:

            level = 1

        elif ap_lo >= 80 and ap_lo < 90:

            level = 3

        elif ap_lo >= 90 and ap_lo < 120:

            level = 4

        else:

            level = 5

        return level


    # Setting BP_category based on ap_li and ap_lo categories
    def set_BP_category (self):

        level_hi = self.get_bplvl_hi()
        level_lo = self.get_bplvl_lo()
        final_level = 0

        if level_hi == None or level_lo == None:

            return


        if level_hi > level_lo:

            final_level = level_hi

        else:

            final_level = level_lo


        if final_level == 1:

            self.med_params["BP_elevated"] = 0
            self.med_params["BP_st1"] = 0
            self.med_params["BP_st2"] = 0
            self.med_params["BP_normal"] = 1

        elif final_level == 2:

            self.med_params["BP_elevated"] = 1
            self.med_params["BP_st1"] = 0
            self.med_params["BP_st2"] = 0
            self.med_params["BP_normal"] = 0

        elif final_level == 3:

            self.med_params["BP_elevated"] = 0
            self.med_params["BP_st1"] = 1
            self.med_params["BP_st2"] = 0
            self.med_params["BP_normal"] = 0

        else:

            self.med_params["BP_elevated"] = 0
            self.med_params["BP_st1"] = 0
            self.med_params["BP_st2"] = 1
            self.med_params["BP_normal"] = 0


    # Setting Cholesterol Category based on its value
    def set_chol_category(self):

        try:
            chol = int(self.med_params["Chol(mg/dL)"])

        except ValueError:

            return
        
        if chol < 200:

            self.med_params["Chol_bv_normal"] = 0
            self.med_params["Chol_normal"] = 1
            self.med_params["Chol_well_bv_normal"] = 0

        elif chol >= 200 and chol < 240:

            self.med_params["Chol_bv_normal"] = 1
            self.med_params["Chol_normal"] = 0
            self.med_params["Chol_well_bv_normal"] = 0

        else:

            self.med_params["Chol_bv_normal"] = 0
            self.med_params["Chol_normal"] = 0
            self.med_params["Chol_well_bv_normal"] = 1


    # Setting Glucose Category based on its value
    def set_gluc_category(self):

        try:
            gluc = int(self.med_params["Gluc(mg/dL)"])

        except ValueError:

            return
        
        if gluc < 100:

            self.med_params["Gluc_bv_normal"] = 0
            self.med_params["Gluc_normal"] = 1
            self.med_params["Gluc_well_bv_normal"] = 0

        elif gluc >= 100 and gluc < 126:

            self.med_params["Gluc_bv_normal"] = 1
            self.med_params["Gluc_normal"] = 0
            self.med_params["Gluc_well_bv_normal"] = 0

        else:

            self.med_params["Gluc_bv_normal"] = 0
            self.med_params["Gluc_normal"] = 0
            self.med_params["Gluc_well_bv_normal"] = 1


    # BMI Setter and Getter Methods
    def set_bmi(self):

        try:
            weight = float(self.med_params["Weight(kg)"])
            height = float(self.med_params["Height(m)"])

            self.med_params["BMI"] = round(weight / ((height))**2, 6)
        
        except ValueError:

            self.med_params["BMI"] = 0
    

    def get_bmi(self):

        return self.med_params["BMI"]


    # Medical Paramaters Setter and Getter Methods
    def set_med_params(self, med_params):

        for key in med_params:

            if key in self.med_params:

                self.med_params[key] = med_params[key]

        self.set_BP_category()
        self.set_bmi()
        self.set_chol_category()
        self.set_gluc_category()


    def get_med_params(self):

        return self.med_params


    # First Name Setter and Getter Methods
    def set_firstname(self, firstname):

        self.firstname = firstname
    

    def get_firstname(self):

        return self.firstname
    

    # Surname Setter and Getter Methods
    def set_surname(self, surname):

        self.surname = surname


    def get_surname(self):

        return self.surname

    
    # Password Setter and Getter Methods
    def set_password(self, password):

        self.password = password


    def get_password(self):

        return self.password

    
    # Email Setter and Getter Methods
    def set_email(self, email):

        self.email = email


    def get_email(self):

        return self.email
    
    
    # Disease Probability Setter and Getter Methods
    def set_cvd_risk(self, cvd_risk):

        self.cvd_risk = cvd_risk


    def get_cvd_risk(self):

        return self.cvd_risk


    # Disease Outcome Setter and Getter Methods
    def set_cvd_out (self, cvd_out):

        self.cvd_out = cvd_out
    

    def get_cvd_out(self):

        return self.cvd_out
    

    # Returns Demographic Parameters
    def get_demographic_params(self):

        keys = ["Age", "Gender", "Height(m)", "Weight(kg)"]

        demographics = {key: value for key, value in self.med_params.items() if key in keys}

        return demographics


    # Returns Lifestyle Parameters
    def get_lifestyle_params(self):

        keys = ["Smoke", "Active", "Alcohol"]

        lifestyle = {key: value for key, value in self.med_params.items() if key in keys}

        return lifestyle


    # Returns Cardiovascular Parameters
    def get_cardiovascular_params(self):

        keys = ["Chol(mg/dL)", "Gluc(mg/dL)", "BP(high)", "BP(low)"]

        cardiovascular = {key: value for key, value in self.med_params.items() if key in keys}

        return cardiovascular