import numpy as np
import numpy.random as npr
import pandas as pd
import logging


class Subsampler:
    
    def __init__(self, df_data, columns_keep_ratio=[], allowed_deviation=.2, allow_zero_occurrence=False):

        # df_ratio = df_ratio.dropna(subset=[column_target])  # remove entries in target column with NaN
        
        self.df_data = df_data.copy()  # complete input data
        self.df_ratio = self.df_data[columns_keep_ratio]  # the dataframe with the columns in which to keep the ratio
        self.allowed_deviation = allowed_deviation  # the allowed deviation from the ratio in the subsampled dataframe in the columns 'columns_keep_ratio' from 0 to 1
        
        # get the categorical columns to create dummy columns for ratio comparison. bool columns will not be in the categorical columns and will be converted to integer columns in the preprocessing
        self.categorical_columns = self.df_ratio.columns[~self.df_ratio.columns.isin(self.df_ratio._get_numeric_data().columns)]
        
        # df to compare mean deviation against when subsampling
        self.df_mean_orig = None  # will be set in preprocessing in "_make_mean_reference"

        # attributes to be filled by methods
        self._test_df = None  # contains test data, created by 'extract_test' if test_size > 0
        
        self._deviation_list = []
        
        # whether to allow 0 occurrences of a value in subsampled data, e.g. complete removal of this value due to subsampling
        self.allow_zero_occurrence = allow_zero_occurrence
        
        self._column_separator = '$$$$$$&&&&&&'
        
        # init steps
        self._preprocess()
        
        
    def _bool_to_int_columns(self):
        # normalize columns
        for col in self.df_ratio:
            if self.df_ratio[col].dtype in ['bool']:
                self.df_ratio.loc[:, col] = self.df_ratio[col].map(int)
                
        
    def _normalize_numerical_columns(self):
        # normalize columns
        for col in self.df_ratio:
            if self.df_ratio[col].dtype in ['float64', 'int64']:
                self.df_ratio.loc[:, col] = self.column_normalize(self.df_ratio[col])
                
                
    def _make_mean_reference(self):
        df = self.df_ratio
        
        if len(self.categorical_columns):
            df = df.drop(self.categorical_columns, axis=1).join(pd.get_dummies(df[self.categorical_columns],  prefix_sep=self._column_separator))
            
        self.df_mean_orig = df.mean()
        
        
    def _preprocess(self):
        # convert bool columns to numerical
        self._bool_to_int_columns()
        # normalize numerical columns
        self._normalize_numerical_columns()
        # important to make mean reference after normalization
        self._make_mean_reference()
            
    
    def extract_test(self, test_size=.2, random_state=101):
        """_summary_

        Args:
            test_size (float, optional): percentage of datapoints in test dataset which will be excluded from subsampling. Defaults to .2.
            random_state (int, optional): the random seed. Defaults to 101.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        
        if type(test_size) not in [int, float] or not 1 >= test_size >= 0:
            raise ValueError('Parameter "test_size" has to be a value in the range from 0 to 1.')
        
        # return empty dataframe with columns 
        if test_size == 0:
            return pd.DataFrame(columns=self.df_data.columns)
        # subsample with equal data distributions
        self._test_df = self.subsample(test_size, random_state=random_state)
        if self._test_df is None:
            return None
        
        # remove test data points from df_data to exclude it in the subsampling process
        self.df_ratio = self.df_ratio[~self.df_ratio.index.isin(self._test_df.index)]
        
        return self._test_df
        
    
    def subsample(self, subsample_factor, random_state=101, raise_exception=False):
        npr.seed(random_state)
        # subsample each label category inidividually to keep intrinsic ratios
        
        # use one hot encoding to calculate the distribution of the categorical features
        if len(self.categorical_columns):
            df_ratio_one_hot_encoded = self.df_ratio.drop(self.categorical_columns, axis=1).join(pd.get_dummies(self.df_ratio[self.categorical_columns], prefix_sep=self._column_separator))
        else:
            df_ratio_one_hot_encoded = self.df_ratio
        df_subsampled = df_ratio_one_hot_encoded.sample(frac=subsample_factor, replace=False, random_state=random_state)
        
        if self.allow_zero_occurrence and len(self.categorical_columns):
            # relevant only for categorical columns
            for col in df_subsampled:
                if col not in self.df_ratio:
                    # categorical columns have appendix based on value and are thus not in the columns_keep_ratio list
                    if not df_subsampled[col].any():
                        column, value = col.split(self._column_separator)
                        message = f'Could not find subsample with seed {random_state} due to zero occcurrences of {value} in column {column}.'
                        if raise_exception:
                            raise Exception(message)
                        else:
                            logging.warning(message)
                            return None

        # check for allowed divergence
        deviation_list = self.calculate_deviations(df_subsampled)
        for deviation_dict in deviation_list:
            col, deviation = deviation_dict['col'], deviation_dict['deviation']
            if deviation > self.allowed_deviation:
                message = f'Could not find subsample with seed {random_state} due to mean deviation {deviation} in column {col}. Allowed deviation is set to {self.allowed_deviation}.'
                if raise_exception:
                    raise Exception(message)
                else:
                    logging.warning(message)
                    return None
            
        indices = set(df_subsampled.index)
        df_subsampled = self.df_data[self.df_data.index.isin(indices)]
        return df_subsampled
    
    
    def calculate_deviations(self, df_subsampled):
        deviation_list = []
        for col, col_mean in df_subsampled.mean().items():
            deviation = np.abs(self.df_mean_orig[col] - col_mean)
            deviation_list.append({'col': col, 'deviation': deviation})
        self._deviation_list = deviation_list
        return deviation_list
    
    
    def get_deviation_list(self):
        return self._deviation_list

    
    @staticmethod
    def column_normalize(col):
        col_min = col.min()
        col_max = col.max()
        if col_min == col_max == 0:
            # all 0s
            return col
        return (col - col_min) / (col_max - col_min)

