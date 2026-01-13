import tensorflow as tf
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class ANN_Model:
    
    def __init__(self,data_manager):

        self.data_manager = data_manager
        self.cardio_df = self.data_manager.get_CardioData()
        self.patients_df = self.data_manager.process_PatientsData()
        self.accuracy = 0
        self.heartdis_ans = ''
        self.seperate_data()

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape = (self.train_values.shape[1],)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(rate = 0.5),
            tf.keras.layers.Dense(64, activation = 'relu'),
            tf.keras.layers.Dropout(rate = 0.5),
            tf.keras.layers.Dense(32, activation = 'relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        optimizer = tf.keras.optimizers.Adam(learning_rate=0.002)
        loss_function = tf.keras.losses.BinaryCrossentropy()
        
        self.model.compile(
            optimizer = optimizer,
            loss = loss_function,
            metrics=['accuracy'])
        
#Dividing dataset into Training and Testing sets
    def seperate_data (self):

        df_onlyvalues = self.cardio_df.drop(columns = 'cardio')

        ds_values = df_onlyvalues.values
        ds_labels = self.cardio_df['cardio'].values

        self.train_values, self.test_values, self.train_labels, self.test_labels = train_test_split(ds_values, ds_labels, test_size=0.2, random_state=50)
        self.train_values, self.val_values, self.train_labels, self.val_labels = train_test_split(self.train_values, self.train_labels, test_size = 0.125, random_state=50)


 #Training the ANN model
    def train_model (self,cycles):

        self.model.fit(self.train_values, self.train_labels,
                        epochs=cycles, batch_size=64,
                        validation_data=(self.val_values, self.val_labels))
        
        print("Model accuracy on the test set is:", self.model.evaluate(self.test_values, self.test_labels))

 #Testing accuracy of the ANN model
    def test_accuracy(self):

        predictions = self.model.predict(self.test_values)

        binary_predictions = np.round(predictions)

        self.accuracy = accuracy_score(self.test_labels, binary_predictions)

        print(f'Model Accuracy: {self.accuracy*100:.0f}%')

        self.accuracy = round(self.accuracy * 100)



 #Getter method for accuracy variable 
    def get_accuracy(self):

        return self.accuracy

 #Predicting if a patient has HeartDisease 
    def predict_HD (self, id):

        patient_details = self.patients_df.iloc[id].values
        #print(patient_details)

        prediction = self.model.predict(np.array(patient_details).reshape((1, -1)))[0]

        binary_prediction = (prediction > 0.5).astype(int)

        predicted_value = binary_prediction[0]
        print(predicted_value)

        if(predicted_value==1):

            self.heartdis_ans = 'Yes'

        else:

            self.heartdis_ans = 'No'

 #Getter method for predicted value variable
    def get_heartdis_ans (self):

        return self.heartdis_ans
    
 #Calculating the percentage of a patient getting heart disease if it is not present
    def calculate_percentage (self,patient):

        age = patient.get_age()
        bmi = patient.get_BMI()
        active = patient.get_active()
        smoking = patient.get_smoking()
        alcohol = patient.get_alcohol()
        chol = patient.get_cholvl()
        gluc = patient.get_gluclvl()
        bp_cat = patient.get_BP_category()
        percentage = 0

        if(self.heartdis_ans == 'No'):

            if(age >= 65):

                age = 12.5

            elif(age>=20 and age<65): # below 20 years old is 0, 65 and above is 12.5

                age = (12.5/46) * (age - 19) # Same process as to BMI

            else:

                age = 0

            if(bmi >= 30 or bmi<18.5): # Above 30 or below 18.5, a person is classified as Obese or Skinny

                bmi = 12.5

            elif(bmi>=25 and bmi<30): # A person is classified as Overweight

                bmi = (12.5/5.1) * (bmi-24.9) # slope (m) = (12.5-0)/(30-24.9), m = (12.5/5.1)
                                              # y - 0 = m * (x - 24.9)
            else: # Between 18.5 and 25, a person is classified as Normal

                bmi = 0
            
            if(active == 'Yes'):

                active = 0

            else:

                active = 12.5
            
            if(smoking == 'Yes'):

                smoking = 12.5

            else:

                smoking = 0

            if(alcohol == 'Yes'):

                alcohol = 12.5

            else:

                alcohol = 0
            
            if(chol == 1):

                chol = 0

            elif(chol == 2):

                chol = 6.25

            else:

                chol = 12.5

            if(gluc == 1):

                gluc = 0

            elif(gluc == 2):

                gluc = 6.25

            else:

                gluc = 12.5

            if(bp_cat == 'Normal'):

                bp_cat = 0

            elif(bp_cat == 'Elevated'):

                bp_cat = 12.5/3

            elif(bp_cat == 'Hypertension Stage 1'):

                bp_cat = (12.5*2)/3

            else:

                bp_cat = 12.5

            percentage = round(age + bmi + active + smoking + alcohol + chol + gluc + bp_cat)

            patient.set_heartper(percentage)

        else:
            
            patient.set_heartper(percentage)










