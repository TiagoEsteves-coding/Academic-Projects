import unittest
import Patient
import ANN_Model
import DataFileManager


class TestANN_Model(unittest.TestCase):
    
    def setUp (self):
        self.patient = Patient.Patient([0,'Nicole','Ayton', 48, 'Female', 1.68, 58,0,'Yes', 'Yes', 'Yes', 1,2, 120,78])
        self.data_manager = DataFileManager.DataFileManager()
        self.model = ANN_Model.ANN_Model(self.data_manager)
        self.model.train_model(1)

    def test_predict_HD (self):
        self.model.predict_HD(0)
        self.assertEqual(self.model.get_heartdis_ans(),'No')

    def test_calculate_percentage_no_heart_disease(self):
        self.model.heartdis_ans = 'No'
        self.model.calculate_percentage(self.patient)
        self.assertEqual(self.patient.get_heartper(),43)

    def test_calculate_percentage_yes_heart_disease(self):
        self.model.heartdis_ans = 'Yes'
        self.model.calculate_percentage(self.patient)
        self.assertEqual(self.patient.get_heartper(),0)

if __name__ == '__main__':
    unittest.main()

