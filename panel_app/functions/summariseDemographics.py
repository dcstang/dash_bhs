from tableone import TableOne
import pandas as pd

def runTableOne(df_key):
    # choose table1 reporting columns
    pathDict = {"Original": "complete", "Imputed": "impute"}

    df_path = pathDict[df_key]

    df = pd.read_parquet(f"data/{df_path}_demographics.parquet")
    tableOneCols = [
        "age.0.0",
        "sex",
        "BMI.0.0",
        "qual_factor",
        "smoking_status.0.0",
        "reg_ps",
        "alcohol.0.0"]

    orderingDict = {
            "reg_ps"      : ["Yes", "No", "Unknown"],
            "qual_factor" : ["High school", "Diploma/Vocational", "Tertiary education"],
     "smoking_status.0.0" : [ 'Current', 'Previous', 'Never', 'Prefer not to answer'],
            "alcohol.0.0" : ['Daily or almost daily', 'Once or twice a week',
                             'Three or four times a week', 
                             'Ocassionally to three times a month',
                             'Never', "Unknown"]
    }
    categoricalList = [
            "qual_factor", "sex",
            "smoking_status.0.0", "reg_ps", "alcohol.0.0"]
    
    renameDict = {
        "n":"Population size",
        "age.0.0": "Age",
        "sex":"Sex",
        "BMI.0.0":"BMI",
        "qual_factor":"Education",
        "smoking_status.0.0":"Smoking",
        "reg_ps":"Prescription medications",
        "alcohol.0.0":"Alcohol intake"}

    outputDf = TableOne(df, columns=tableOneCols,
            rename=renameDict,
            categorical=categoricalList, order=orderingDict)
        
    return outputDf.tabulate(tablefmt="html", colalign=["","","center","right"])