import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

class SkewTransform:
    def __init__(self, df):
        self.df = df
    
    def identify_skewed_columns(self, threshold=2):
        '''
        Identifies skewed columns in the dataframe.

        Args:
            threshold (float): The skewness threshold above which columns are considered skewed. Default is 2.

        Returns:
            List[str]: A list of column names with skewness above the given threshold.
        '''
        numerical_columns = self.df.select_dtypes(include=[np.number]).columns
        skewness = self.df[numerical_columns].apply(lambda n: n.skew())
        skewed_columns = skewness[abs(skewness) > threshold].index.tolist()
        return skewed_columns
    
    def transform_log(self, threshold=2):
        '''
        Applies a log transformation to columns identified as skewed.

        Args:
            threshold (float): The skewness threshold above which columns will be transformed. Default is 2.
        
        Returns:
            None: The dataframe is transformed in place.
        '''
        skewed_columns = self.identify_skewed_columns(threshold)
        for column in skewed_columns:
            self.df[column] = np.log1p(self.df[column].clip(lower=0))  # clip to avoid negative values or zero

    # def transform_yeo_johnson(self, threshold=2):
        '''
        Applies Yeo-Johnson transformation to columns identified as skewed.

        Args:
            threshold (float): The skewness threshold above which columns will be transformed. Default is 2.
        
        Returns:
            None: The dataframe is transformed in place.
        '''
        # skewed_columns = self.identify_skewed_columns(threshold)
        # for column in skewed_columns:
           # self.df[column], _ = stats.yeojohnson(self.df[column])

    def transform_box_cox(self, threshold=2):
        '''
        Applies Box-Cox transformation to columns identified as skewed.
        Note: Box-Cox requires the data to be positive.

        Args:
            threshold (float): The skewness threshold above which columns will be transformed. Default is 2.
        
        Returns:
            None: The dataframe is transformed in place.
        '''
        skewed_columns = self.identify_skewed_columns(threshold)
        for column in skewed_columns:
            if (self.df[column] > 0).all():  # Check if all values are positive
                self.df[column], _ = stats.boxcox(self.df[column])
            else:
                print(f"Column {column} contains non-positive values and cannot be Box-Cox transformed.")
                
    def plot_histograms(self):
        '''
        Plots histograms of all numerical columns to visualize the skewness before and after transformation.
        
        Returns:
            None: Displays plots of histograms.
        '''
        numerical_columns = self.df.select_dtypes(include=[np.number]).columns
        fig, axes = plt.subplots(nrows=2, ncols=len(numerical_columns), figsize=(15, 8))
        fig.suptitle('Histograms of Numerical Columns Before and After Transformation', fontsize=16)
        
        for i, column in enumerate(numerical_columns):
            # Plot before transformation
            sns.histplot(self.df[column], ax=axes[0, i], kde=True, color='blue')
            axes[0, i].set_title(f'Original: {column}')
            
            # Plot after transformation
            transformed_df = self.df.copy()  # Make a copy to apply transformations
            skew_transformer = SkewTransform(transformed_df)
            skew_transformer.transform_log()  # Apply one transformation, or call others as needed
            sns.histplot(transformed_df[column], ax=axes[1, i], kde=True, color='red')
            axes[1, i].set_title(f'Transformed: {column}')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def plot_skewness(self):
        '''
        Plots the skewness of each column before and after transformation.

        Returns:
            None: Displays a bar plot comparing skewness values.
        '''
        original_skewness = self.df.copy().apply(lambda n: n.skew())
        transformed_df = self.df.copy()
        skew_transformer = SkewTransform(transformed_df)
        skew_transformer.transform_log()  # Apply one transformation, or call others as needed
        transformed_skewness = transformed_df.apply(lambda n: n.skew())
        
        skew_df = pd.DataFrame({
            'Column': original_skewness.index,
            'Original Skewness': original_skewness.values,
            'Transformed Skewness': transformed_skewness.values
        })

        skew_df.set_index('Column', inplace=True)
        skew_df.plot(kind='bar', figsize=(12, 6))
        plt.title('Skewness Comparison Before and After Transformation')
        plt.ylabel('Skewness')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # Create a sample DataFrame
    data = pd.read_csv('loan_payments.csv')
    df = pd.DataFrame(data)
    
    # Initialize SkewTransform with the DataFrame
    skew_data = SkewTransform(df)
    
    # Identify skewed columns
    print("Skewed columns:", skew_data.identify_skewed_columns())

    # Apply log transformation
    skew_data.transform_log()
    print("Data after log transformation:")
    print(df)
    
    # Apply Yeo-Johnson transformation
    # skew_data.transform_yeo_johnson()
    # print("Data after Yeo-Johnson transformation:")
    # print(df)
    
    # Apply Box-Cox transformation
    skew_data.transform_box_cox()
    print("Data after Box-Cox transformation:")
    print(df)

        # Visualize histograms
    skew_data.plot_histograms()
    
    # Plot skewness comparison
    skew_data.plot_skewness()
