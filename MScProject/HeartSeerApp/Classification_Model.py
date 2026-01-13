import joblib

class AI_Model:

    def __init__(self, filepath):

        self.model = joblib.load(filepath)
    
    
    # Predicts whether the user has or has not heart disease
    def predict_cvd(self, processed_data):

        pred = self.model.predict(processed_data)

        outcome = "No" if pred == 0 else "Yes"

        return outcome
    

    # Calculates the percentage of getting heart diease or how serious it is currently
    def compute_cvd_risk (self, med_params):

        try:

            age = int(med_params["Age"])

        except ValueError:

            age = 0
            
        bmi = med_params["BMI"]
        active = 0
        smoking = 0
        alcohol = 0
        chol = 0
        gluc = 0
        bp = 0

        cvd_risk = 0

        if age >= 65:

            age = 12.0

        elif age > 20 and age < 65: # below 20 years old is 0, 65 and above is 12.0

            age = (12.0/45) * (age - 20) # Same process as to BMI

        else:

            age = 0


        if bmi >= 30 or bmi < 18.5: # Above 30 or below 18.5, a person is classified as Obese or Skinny

            bmi = 7.0

        elif bmi >= 25 and bmi < 30: # A person is classified as Overweight

            bmi = (7.0/(30 - 24.9)) * (bmi - 24.9) # slope (m) = (7.0-0)/(30-24.9)
                                              # y - 0 = m * (x - 24.9)
        else: # Between 18.5 and 25, a person is classified as Normal

            bmi = 0


        if med_params["Active"] == "Yes":

            active = 0

        elif med_params["Active"] == "No":

            active = 5.0

        else:

            active = 0


        if med_params["Smoke"] == "Yes":

            smoking = 15.0

        elif med_params["Smoke"] == "No":

            smoking = 0

        else:

            smoking = 0


        if med_params["Alcohol"] == "Yes":

            alcohol = 3.0

        elif med_params["Alcohol"] == "No":

            alcohol = 0

        else:

            alcohol = 0


        if med_params["Chol_normal"] == 1:

            chol = 0

        elif med_params["Chol_bv_normal"] == 1:

            chol = 9.0

        elif med_params["Chol_well_bv_normal"] == 1:

            chol = 18.0

        else:

            chol = 0


        if med_params["Gluc_normal"] == 1:

            gluc = 0

        elif med_params["Gluc_bv_normal"] == 1:

            gluc = 7.5

        elif med_params["Gluc_well_bv_normal"] == 1:

            gluc = 15.0

        else:

            gluc = 0


        if med_params["BP_normal"] == 1:

            bp = 0

        elif med_params["BP_elevated"] == 1:

            bp = 25.0/3

        elif med_params["BP_st1"] == 1:

            bp = (25.0*2)/3

        elif med_params["BP_st2"] == 1:

            bp = 25.0
        
        else:

            bp = 0

        cvd_risk = int(age + bmi + active + smoking + alcohol + chol + gluc + bp)

        return cvd_risk