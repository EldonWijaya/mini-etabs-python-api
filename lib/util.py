import os
import pandas as pd
import tempfile

def open_as_csv(table):
    """
    This function saves a pandas DataFrame to a temporary csv file and opens it
    """
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp_name = tmp.name

    csv_folder_path = os.getcwd() + r'\csv'
    # os.makedirs(csv_folder_path)
    table.to_csv(tmp_name, index = False)
    os.startfile(tmp_name)