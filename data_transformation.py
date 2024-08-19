# -*- coding: utf-8 -*-
import pandas as pd
from scipy import stats
from data_info import DataFrameInfo
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class DataTransformation:
    """
    Handling the task of data conversion in the loans dataset
    """
    def __init__(self, df):
        self.df = df.copy  # Create a copy to avoid modifying the original dataframe

    def remove_whitespace(self): # First lets strip the whitespace
     return self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def datetime_date_column(self, date_column):
        """
        Convert pandas object dtype into a pandas datetime dtype.
        
        Args:
            date_column (str): Name of the pandas dataframe column to be converted.
        
        Returns:
            pandas.DataFrame: Updated dataframe with converted date column.
        """
        self.df[date_column] = pd.to_datetime(self.df[date_column], dayfirst=True) # dayfirst=True is not strict, but will prefer to parse with day first
        return self.df

    def float_term(self, term_column):
        """
        Convert the 'term' column to float format. 
        
        Args:
            term_column (str): Name of the pandas dataframe column to be converted to float.
        
        Returns:
            pandas.DataFrame: Updated dataframe with converted term column.
        """
        self.df[term_column] = self.df[term_column].str.extract(r'(\d+)', expand=False).astype(float)
        return self.df

    def categorical_cat_column(self, cat_column):
        """
        Converting column to categorical dtype.
        
        Args:
            cat_column (str): Name of the pandas dataframe column to be converted to category dtype.
        
        Returns:
            pandas.DataFrame: Updated dataframe with converted categorical column.
        """
        self.df[cat_column] = self.df[cat_column].astype('category')
        return self.df

    def categorical_numerical(self, category_column):
        """
        Converting categorical columns to numerical columns.
        
        Args:
            category_column (str): Name of the pandas df column being converted to numerical.
        
        Returns:
            pandas.DataFrame: Updated dataframe with converted numerical column.
        """
        self.df[category_column] = pd.factorize(self.df[category_column])[0] + 1
        return self.df

    def convert_to_float(self, column):
        """
        Converts column to float dtype.
        
        Args:
            column (str): Name of the pandas df column being converted.
        
        Returns:
            pandas.DataFrame: Updated dataframe with converted float column.
        """
        self.df[column] = self.df[column].astype(float)
        return self.df


class DataFrameTransform:
    """
    A class for handling missing values in a DataFrame, including identification,
    percentage calculation, imputation, and removal of columns or rows.
    """
    
    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()
    
    def identify_missing_values(self):
        """
        Identifies variables with missing values and calculates the percentage of missing values.
        
        Returns:
            pandas.DataFrame: A DataFrame with columns for null count and percentage.
        """
        null_count = self.df.isnull().sum()
        null_percentage = 100 * null_count / len(self.df)
        missing_value_df = pd.DataFrame({'null_count': null_count,
                                         'null_percentage': null_percentage})
        missing_value_df = missing_value_df[missing_value_df['null_count'] > 0].sort_values('null_percentage', ascending=False)
        return missing_value_df
    
    def handle_missing_values(self, threshold_percentage=10, method='impute'):
        """
        Handles missing values based on the percentage of missing data and specified method.
        
        Args:
            threshold_percentage (float): The threshold percentage for deciding whether to impute or remove. Defaults to 5.
            method (str): The method to handle missing values, either 'impute' or 'remove'. Defaults to 'impute'.
        
        Returns:
            pandas.DataFrame: The updated DataFrame after handling missing values.
        """
        missing_value_df = self.identify_missing_values()
        
        for column in missing_value_df.index:
            percentage = missing_value_df.loc[column, 'null_percentage']
            
            if percentage <= threshold_percentage:
                if method == 'impute':
                    self.impute_column(column)
                elif method == 'remove':
                    self.df = self.df.dropna(subset=[column])
            else:
                print(f"Column '{column}' has {percentage:.2f}% missing values. Removing this column.")
                self.df = self.df.drop(columns=[column])
        
        return self.df
    
    def impute_column(self, column, impute_type='median'):
        """
        Imputes a DataFrame column.
        
        Args:
            column (str): Name of the pandas df column being imputed.
            impute_type (str): Whether to impute median or mean. Defaults to 'median'.
        """
        if impute_type not in ['median', 'mean']:
            raise ValueError("Please enter a valid imputation method: either 'median' or 'mean'.")
        
        if np.issubdtype(self.df[column].dtype, np.number):
            impute_value = getattr(self.df[column], impute_type)()
            self.df[column].fillna(impute_value, inplace=True)
        else:
            # For non-numeric columns, use mode
            impute_value = self.df[column].mode()[0]
            self.df[column].fillna(impute_value, inplace=True)
        
        print(f"Imputed column '{column}' with {impute_type}")

    def visualize_null_removal(self):
        """
        Generates a plot to visualize the removal of NULL values.
        Compares the original DataFrame with the current DataFrame.
        """
        original_nulls = self.original_df.isnull().sum()
        current_nulls = self.df.isnull().sum()
        
        comparison_df = pd.DataFrame({
            'Original': original_nulls,
            'Current': current_nulls
        }).sort_values('Original', ascending=False)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=comparison_df)
        plt.title('Comparison of NULL Values: Original vs Current')
        plt.xlabel('Columns')
        plt.ylabel('Number of NULL Values')
        plt.xticks(rotation=10)
        plt.tight_layout()
        plt.show()

    def remove_highly_correlated_columns(self, threshold=0.9):
        """
        Identifies and removes highly correlated columns from the DataFrame.

        Args:
            threshold (float): The correlation threshold above which columns will be considered highly correlated.
                            Default is 0.9.
        
        Returns:
            pandas.DataFrame: The updated DataFrame with highly correlated columns removed.
        """
        # Convert non-numeric columns to numeric, coercing errors to NaN
        df_numeric = self.df.apply(pd.to_numeric, errors='coerce')
        
        # Drop columns that were not converted to numeric (all NaNs)
        df_numeric = df_numeric.dropna(axis=1, how='all')
        
        # Step 0: Compute the correlation matrix
        corr_matrix = df_numeric.corr()

        # Step 2: Visualize the correlation matrix
        plt.figure(figsize=(15, 15))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        plt.show()

        # Step 3: Identify highly correlated columns
        # Find pairs of columns with correlation above the threshold
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper_tri.columns if any(upper_tri[column].abs() > threshold)]

        print(f"Columns to drop due to high correlation (>{threshold}): {to_drop}")

        # Step 4: Remove the highly correlated columns from the original DataFrame
        self.df = self.df.drop(columns=to_drop)
        
        return self.df

    def save_dataframe(self, filename):
        """
        Saves the current DataFrame to a CSV file.
        
        Args:
            filename (str): The name of the file to save the DataFrame to.
        """
        self.df.to_csv(filename, index=False)
        print(f"DataFrame saved to {filename}") 



if __name__ == "__main__":
    df_transform = DataFrameTransform(pd.read_csv('loan_payments.csv'))

        # To see the missing value statistics
        # print(df_transform.identify_missing_values())

        # To handle missing values with default settings (5% threshold, imputation)
        # updated_df = df_transform.handle_missing_values()

        # To handle missing values with custom settings
    # updated_df = df_transform.handle_missing_values(threshold_percentage=10, method='remove')

    df_transform.identify_missing_values()
    df_transform.handle_missing_values()
    df_transform.impute_column
    df_transform.save_dataframe("Clean_data.csv")
    df_transform.remove_highly_correlated_columns(threshold=0.9)