# encoding=UTF-8
from functools import wraps, lru_cache
import importlib
import subprocess
import sys
import csv
import pandas as pd
import numpy as np

# List of required libraries
required_libraries = ['numpy', 'pandas', 'pyarrow']

# Check if required libraries are installed and install them if missing
missing_libraries = []
for lib in required_libraries:
    try:
        importlib.import_module(lib)
    except ModuleNotFoundError:
        missing_libraries.append(lib)

if missing_libraries:
    print(f"The following required libraries are missing and will be installed: ")
    for lib in missing_libraries:
        print(lib)
    try:
        for lib in missing_libraries:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', lib])
        print(f"Installation complete.")
    except Exception as e:
        print(f"An error occurred while installing the required libraries: {str(e)}")
        sys.exit(1)

# Memoization cache
memoization_cache = {}


@lru_cache(maxsize=None)
def memoize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (func, args, frozenset(kwargs.items()))
        if key in memoization_cache:
            return memoization_cache[key]
        result = func(*args, **kwargs)
        memoization_cache[key] = result
        return result

    return wrapper


@memoize
def read_csv(file_path: str, delimiter=',', quotechar='"', encoding='utf-8', skiprows=None, filters=None,
             group_by=None, columns_to_print=None, group_entire_print=False, **kwargs):
    try:
        """ Advanced feather csv debugging"""
        try:
            feather_path = file_path.replace('.csv', '.feather')
            df = pd.read_feather(feather_path, **kwargs)
        except Exception as e:
            Warning(f'{e} Switching to the csv format. Conversion on write_csv')
            with open(file_path, 'r', encoding=encoding) as file:
                csv_reader = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
                if skiprows is not None:
                    for _ in range(skiprows):
                        next(csv_reader)

                # Read the first row to get column names
                all_columns = next(csv_reader)

                # Read data into a list of dictionaries
                data = [dict(zip(all_columns, row)) for row in csv_reader]
            df = pd.DataFrame(data)

        if skiprows is not None:
            df = df.iloc[skiprows:]
        if filters is not None:
            for column, value in filters.items():
                df = df[df[column] == value]
        if group_by is not None:
            grouped_df = df.groupby(group_by)
            for name, group in grouped_df:
                if group_entire_print:
                    print(f"Group {name}:")
                    print(group[columns_to_print if columns_to_print is not None else slice(None)])
        return df
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return None


def write_csv(data_frame: pd.DataFrame, csv_file_path: str, feather_file_path: str, index: bool = False,
              info: bool = False,
              **kwargs) -> None:
    try:
        # Write DataFrame to CSV
        data_frame.to_csv(csv_file_path, index=index, **kwargs)

        # Convert CSV to Feather
        df_from_csv = pd.read_csv(csv_file_path, **kwargs)  # Read CSV to create DataFrame
        df_from_csv.to_feather(feather_file_path)  # Convert DataFrame to Feather

        if info is True:
            print(f"DataFrame successfully written to {csv_file_path} and converted to Feather: {feather_file_path}.")
    except Exception as e:
        FileNotFoundError(f"An error occurred while writing the DataFrame to CSV and converting to Feather: {e}")


if __name__ == '__main__':
    file_path = 'map/chicken.csv'
    csv_file_path = 'map/chicken.csv'
    feather_file_path = 'map/chicken.feather'
    group_by_column = 'token_id'
    columns_to_print = np.array(
        ['chicken_name', 'breed', 'type', 'hatch_date', 'token_id', 'achievements', 'collections',
         'flying_eligibility', 'drumstick_value'])
    data_frame = read_csv(file_path, delimiter=',', quotechar='"', encoding='utf-8', skiprows=0,
                          group_by=group_by_column, columns_to_print=None, group_entire_print=False)
    if data_frame is not None:
        # Convert 'type' column to a list and print
        type_column_as_list = data_frame['breed'].tolist()
        print(type_column_as_list)
        print("1. type: " + type_column_as_list[1])
        print("2. type: " + type_column_as_list[2])
        write_csv(data_frame, csv_file_path, feather_file_path, index=False)
