import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class DataFileManager:

    def __init__(self):
        
        self.df_cardio = pd.read_excel('Datasets\\CardioData.xlsx')

        self.df_patients = pd.read_excel('Datasets\\PatientsData.xlsx')

        self.private_process_CardioData()

#Processing Cardio Data Dataframe
    def private_process_CardioData(self):

        columns_to_drop = ['age', 'bp_category_encoded','id']

        self.df_cardio.drop(columns=columns_to_drop, inplace=True)

        self.df_cardio = pd.get_dummies(self.df_cardio, columns=['bp_category'], prefix='bp_category')

        numerical_columns = self.df_cardio.select_dtypes(include=['float64', 'int64', 'bool']).columns

        scaler = MinMaxScaler()

        self.df_cardio[numerical_columns] = scaler.fit_transform(self.df_cardio[numerical_columns])
        #self.df_cardio.info()

#Getter method for Cardio Data Dataframe
    def get_CardioData(self):

        return self.df_cardio

#Processing Patients Data Dataframe
    def process_PatientsData (self):

        df_patients = self.df_patients.copy(True)

        columns_to_drop = ['ID','First Name','Last Name','Heart Disease','HP (%)']

        df_patients.drop(columns=columns_to_drop, inplace=True)

        columns_to_convert = ['Smoking','Alcohol','Active']

        df_patients['Gender'] = df_patients['Gender'].apply(lambda x: 1 if x == 'Female' else 0)

        df_patients[columns_to_convert] = df_patients[columns_to_convert].applymap(lambda x: 1 if x == 'Yes' else 0)

        df_patients = pd.get_dummies(df_patients, columns=['BP Category'], prefix='BP Category')

        numerical_columns = df_patients.select_dtypes(include=['float64', 'int64', 'bool']).columns

        scaler = MinMaxScaler()

        df_patients[numerical_columns] = scaler.fit_transform(df_patients[numerical_columns])

        return df_patients
    
#Updating the Patients Data File
    def update_PatientData (self,patient):

        patient_info = patient.get_patientInfo()

        self.df_patients.loc[self.df_patients['ID'] == patient.get_id()] = patient_info

        self.df_patients.to_excel('Datasets\\PatientsData.xlsx', index = False)

#Removing a patient from the dataset by their ID
    def remove_Patient (self, patient_id):

        self.df_patients = self.df_patients.drop(index = patient_id)

        self.df_patients ['ID'] = range (0,len(self.df_patients))

        self.df_patients.to_excel('Datasets\\PatientsData.xlsx', index=False)

#Getter method for Patients Data dataframe
    def get_PatientsData (self):

        return self.df_patients
