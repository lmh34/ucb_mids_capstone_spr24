import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def make_feature_subset_pearson_corr_heatmap(pandas_df, str_to_select_cols, plot_title):
    """
    generate heatmap of Pearson correlation coefficients for subset of features in df
    - str_to_select_cols: string within column name subtroup that contain this substring. These columns form the feature subset.

    """
    # select cols containing string that identifies feature subset
    heatmap_columns = [col for col in pandas_df.columns if str_to_select_cols in col]
    # subset those columns in df
    df_filtered = pandas_df[heatmap_columns]
    # calculate correlation matrix
    corr_matrix = df_filtered.corr()
    # set repeated values in upper triangle of correlation matrix to NaN (simplify plot)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    corr_matrix[mask] = np.nan
    # plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", mask=mask)
    plt.title(plot_title)
    plt.show()

def make_feature_list_corr_heatmap(pandas_df, features_list, plot_title):
    """
    generate heatmap of Pearson correlation coefficients for subset of features in df
    - str_to_select_cols: string within column name subtroup that contain this substring. These columns form the feature subset.

    """
    # subset those columns in df
    df_filtered = pandas_df[features_list]
    # calculate correlation matrix
    corr_matrix = df_filtered.corr()
    # set repeated values in upper triangle of correlation matrix to NaN (simplify plot)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    corr_matrix[mask] = np.nan
    # plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", mask=mask)
    plt.title(plot_title)
    plt.show()

def make_null_df(df):
    # calculate percentage of nulls for each column
    percent_missing = df.isnull().sum() * 100 / len(df)
    # return df of results
    results_df = pd.DataFrame({'feature_name': percent_missing.index, 'percent_null': percent_missing.values})
    results_df.sort_values(by='percent_null',ascending=False, inplace=True)
    results_df.reset_index(drop=True,inplace=True)
    return results_df

def null_values_percentage_by_county_and_period(df, column_names):
    """
    # function that filters pandas df by individual columns and returns percentages of rows
    # with missing values by 'county_name' and 'PERIOD'
    # - 'column_names' argument: list of column names to inspect
    # returns dict of keys = column name, values = dfs for column name
    """
    result = {}
    for column_name in column_names:
        # filter df to null values in the specified column
        filtered_df = df[df[column_name].isnull()]
        # group by 'county_name' and 'PERIOD' to obtain null row counts
        grouped = filtered_df.groupby(['county_name', 'period']).size().reset_index(name='count_nulls')
        # group df by 'county_name' and 'PERIOD' to get total counts
        total_counts = df.groupby(['county_name', 'period']).size().reset_index(name='total_counts')
        # merge counts to calculate percentages
        merged_df = pd.merge(grouped, total_counts, on=['county_name', 'period'])
        merged_df['null_percentage'] = (merged_df['count_nulls'] / merged_df['total_counts']) * 100
        # select relevant columns
        final_df = merged_df[['county_name', 'period', 'null_percentage']]
        result[column_name] = final_df
    return result

def create_violin_plots_all_features(df):
    # Calculate the number of rows needed for subplots (5 plots per row)
    num_plots = sum(df[column].dtype in ['int64', 'float64'] or (df[column].dtype == 'object' and df[column].nunique() < 10) for column in df.columns)
    num_rows = (num_plots + 4) // 5  # Adds 4 for rounding up the division

    plt.figure(figsize=(20, 6 * num_rows))  # Adjust the size as needed

    plot_count = 1  # To keep track of which subplot we're on
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64'] or (df[column].dtype == 'object' and df[column].nunique() < 10):
            plt.subplot(num_rows, 5, plot_count)
            sns.violinplot(x=df[column])
            plt.title(f'Violin plot of {column}')
            if plot_count % 5 == 0 or plot_count == num_plots:
                plt.show()  # Show the plot when a row is complete or it's the last plot
                if plot_count < num_plots:
                    plt.figure(figsize=(20, 6 * num_rows))  # Start a new figure if there are more plots to show
            plot_count += 1




