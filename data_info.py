import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Union

class DataFrameInfo:
    """Generate useful information about your DataFrame."""
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy() # Create a copy to avoid modifying the original dataframe

    def describe(self) -> pd.DataFrame:
        """
        Returns the statistical information about the dataframe.
        
        Returns:
            pd.DataFrame: Statistical summary of the dataframe.
        """
        return self.df.describe()
    
    def get_statistic(self, stat_func: str, column: Optional[str] = None) -> Union[float, pd.Series]:
        """
        Calculate a statistic (median, std, or mean) for a column or the entire dataframe.
        
        Args:
            stat_func (str): The statistic to calculate ('median', 'std', or 'mean').
            column (str, optional): The column name. If None, calculates for all numeric columns.
        
        Returns:
            Union[float, pd.Series]: The calculated statistic.
        """
        if stat_func not in ['median', 'std', 'mean']:
            raise ValueError("Invalid statistic. Choose 'median', 'std', or 'mean'.")
        
        if column:
            return getattr(self.df[column], stat_func)(numeric_only=True)
        return getattr(self.df, stat_func)(numeric_only=True)

    def shape(self) -> tuple:
        """
        Returns the shape of the dataframe.
        
        Returns:
            tuple: The shape of the dataframe (rows, columns).
        """
        return self.df.shape
    
    def count_distinct_categories(self, column: str) -> pd.Series:
        """
        Count distinct categories in a categorical column.
        
        Args:
            column (str): The name of the column to analyze.
        
        Returns:
            pd.Series: Value counts of the categories.
        
        Raises:
            ValueError: If the column is not of category dtype.
        """
        if not pd.api.types.is_categorical_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' is not of category dtype. Convert it first.")
        return self.df[column].value_counts()

    def get_missing_values(self) -> pd.DataFrame:
        """
        Calculate the percentage of missing values in each column.
        
        Returns:
            pd.DataFrame: A dataframe with columns and their missing value percentages.
        """
        percent_missing = (self.df.isnull().sum() * 100 / len(self.df)).round(2)
        missing_value_df = pd.DataFrame({
            'column_name': self.df.columns,
            'percent_missing': percent_missing
        })
        return missing_value_df[missing_value_df["percent_missing"] > 0]

class Plotter:
    """Class for plotting dataframe information."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def histogram(self, column: str, bins: int = 10, title: Optional[str] = None, 
                  xlabel: Optional[str] = None, ylabel: Optional[str] = None):
        """
        Plot a histogram for a specified column.
        
        Args:
            column (str): The name of the column to plot.
            bins (int, optional): Number of bins in the histogram. Defaults to 10.
            title (str, optional): The title of the plot.
            xlabel (str, optional): The label for the x-axis.
            ylabel (str, optional): The label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[column].dropna(), bins=bins, edgecolor='black')
        plt.title(title or f'Histogram of {column}')
        plt.xlabel(xlabel or column)
        plt.ylabel(ylabel or 'Frequency')
        plt.show()