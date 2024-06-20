import os
import pandas as pd

def get_table_display(SapModel, TableKey, Group = ''):
    """
    This function returns a DatabaseTable from ETABS
    """
    csv_folder_path = os.getcwd() + r'\csv'
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)
    csv_file_path = os.path.join(csv_folder_path,TableKey+r'.csv')
    SapModel.DatabaseTables.GetTableForDisplayCSVFile(TableKey, '', Group, -1, csv_file_path)
    table = pd.read_csv(csv_file_path)
    os.remove(csv_file_path)
    return table

class database_tables:
    """
    This class allows interactive editing with DatabaseTables
    """
    def __init__(self, SapModel, TableKey, Group = ''):
        csv_folder_path = os.getcwd() + r'\csv'
        self.SapModel = SapModel
        self.TableKey = TableKey
        self.Group = Group
        self.csv_folder_path = os.getcwd() + r'\csv'
        self.csv_file_path = os.path.join(csv_folder_path, TableKey + r'.csv')
    def get_table_edit(self):
        ret = self.SapModel.DatabaseTables.GetTableForEditingCSVFile(self.TableKey,self.Group,-1,self.csv_file_path)
        table = pd.read_csv(self.csv_file_path)
        self.table = table
        os.remove(self.csv_file_path)
        return ret
        # return table
    def set_table_edit(self):
        self.table.to_csv(self.csv_file_path)
        ret = self.SapModel.DatabaseTables.SetTableForEditingCSVFile(self.TableKey, -1, self.csv_file_path)
        return ret