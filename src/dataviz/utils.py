import pandas as pd
import numpy as np

def clean_dataset(df):
    """
    Clean the input dataset by performing common cleaning operations:
    - Remove duplicate rows
    - Handle missing values
    - Convert data types
    - Remove outliers
    - Standardize column names
    """
    # Make a copy of the dataframe
    df_clean = df.copy()
    
    # Standardize column names
    df_clean.columns = [col.lower().replace(' ', '_') for col in df_clean.columns]
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    for column in df_clean.columns:
        # Get the data type of the column
        dtype = df_clean[column].dtype
        
        if pd.api.types.is_numeric_dtype(dtype):
            # For numeric columns, fill missing values with median
            df_clean[column] = df_clean[column].fillna(df_clean[column].median())
        else:
            # For non-numeric columns, fill missing values with mode
            df_clean[column] = df_clean[column].fillna(df_clean[column].mode()[0])
    
    # Convert data types
    for column in df_clean.columns:
        # Try to convert to numeric if possible
        try:
            df_clean[column] = pd.to_numeric(df_clean[column])
        except:
            pass
        
        # Convert date-like columns to datetime
        if df_clean[column].dtype == object:
            try:
                df_clean[column] = pd.to_datetime(df_clean[column])
            except:
                pass
    
    # Remove outliers from numeric columns
    for column in df_clean.select_dtypes(include=[np.number]).columns:
        Q1 = df_clean[column].quantile(0.25)
        Q3 = df_clean[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean[column] = df_clean[column].clip(lower=lower_bound, upper=upper_bound)
    
    return df_clean