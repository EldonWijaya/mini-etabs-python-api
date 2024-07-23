import os
import pandas as pd
import tempfile
import openpyxl
import xlsxwriter

def open_as_csv(table):
    """
    This function saves a pandas DataFrame to a temporary csv file and opens it
    """
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tmp:
        tmp_name = tmp.name

    csv_folder_path = os.getcwd() + r'\csv'
    # os.makedirs(csv_folder_path)
    table.to_csv(tmp_name, index = False)
    os.startfile(tmp_name)

def open_as_excel(*args):
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as tmp:
        tmp_name = tmp.name
    with pd.ExcelWriter(tmp_name, engine='xlsxwriter') as writer:
        for i, df in enumerate(args, start=1):
            sheet_name_i = f'Sheet{i}'
            df.to_excel(writer, sheet_name=sheet_name_i, index=False)
    os.startfile(tmp_name)
                        
            