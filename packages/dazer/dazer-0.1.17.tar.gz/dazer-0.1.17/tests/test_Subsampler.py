import unittest
from dazer import Subsampler 
import pandas as pd
import seaborn as sns
import numpy as np
import tempfile
import shutil

class Testing(unittest.TestCase):
    
    def setUp(self) -> None:
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        return super().setUp()
    
    
    def tearDown(self) -> None:
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        return super().tearDown()
    
    
    def test_column_normalize(self):
        col = pd.Series([-0.25, 3])
        col_norm = Subsampler.column_normalize(col)
        self.assertTrue(col_norm.min() == 0)
        self.assertTrue(col_norm.max() == 1)
    
    
    def test_Subsampler(self):
        
        df = sns.load_dataset('penguins', data_home=self.test_dir)
        subsampler = Subsampler(df, ['body_mass_g'], .07, True)
        
        df_test = subsampler.extract_test(.2, random_state=2)
        df_train = subsampler.subsample(.4, random_state=3)
        
        deviation_test = np.abs(subsampler.column_normalize(df['body_mass_g']).mean() - subsampler.column_normalize(df_test['body_mass_g']).mean())
        self.assertTrue(round(deviation_test, 5) == round(0.028691008567169607, 5))
            
        deviation_train = np.abs(subsampler.column_normalize(df['body_mass_g']).mean() - subsampler.column_normalize(df_train['body_mass_g']).mean())
        self.assertTrue(round(deviation_train, 5) == round(0.010262500500191507, 5))
        
        
    def test_subsampling_deviation(self):
        df = sns.load_dataset('penguins', data_home=self.test_dir)
        subsampler = Subsampler(df, ['body_mass_g'], .02, True)
        
        df_test = subsampler.extract_test(.2, random_state=2)
        self.assertTrue(df_test is None)
    
        
    def test_subsampling_get_deviation_list(self):
        df = sns.load_dataset('penguins', data_home=self.test_dir)
        subsampler = Subsampler(df, ['body_mass_g'], .06, True)
        
        _ = subsampler.extract_test(.4, random_state=4)
        _ = subsampler.subsample(.4, random_state=4)
        
        devialtion_list = subsampler.get_deviation_list()
        
        self.assertTrue(round(devialtion_list[0]['deviation'], 5) == round(0.01643383149231098, 5))
        
        
    def test_subsampling_allow_zero_occurrences(self):
        df = sns.load_dataset('penguins', data_home=self.test_dir)
        subsampler = Subsampler(df, ['body_mass_g', 'island', 'species'], 1, True)
        
        df_train = subsampler.subsample(.01, random_state=4)
        
        self.assertTrue(df_train is None)
        
            
        
            
        
