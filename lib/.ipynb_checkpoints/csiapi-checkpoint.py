import os
import pandas as pd
import comtypes.client
import sys

def get_active_etabs_object():
    helper = comtypes.client.CreateObject("ETABSv1.Helper")
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    print("Succesfully created helper object")

    try:
        # get the active ETABS object
        ETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        SapModel = ETABSObject.SapModel
        print("Succesfully created SapModel")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    return ETABSObject, SapModel

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

def select_unique_names(SapModel, df):
    for i in df['UniqueName']:
        SapModel.FrameObj.SetSelected(str(i), True)
        
    