import pandas as pd
import panel as pn
from tableone import TableOne
from components.variable_store import cardHeaderStylesheet

def runTableOne(dfKeyList):
    # choose table1 reporting columns
    outputList = []

    for key in dfKeyList:
        df = pd.read_parquet(f"data/{key}_demographics.parquet")
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
            
        outputList.append(
            outputDf.tabulate(tablefmt="html", colalign=["","","center","right"])
        )

    return outputList

def highlightImputedDataset(dfKey=None):
    """
        function to check which card and apply specific 
    """
    if dfKey == "complete":
        return ["#bebebe", "#0", "#d3d3d340"]
    else:
        return ["#0000CD", "#ffffff", "#5c9ac830"]

def generateDemographicsComponent(dfKeyList):

    populationTableList = runTableOne(dfKeyList)

    tableStyles = {
        'background-color': '#F6F6F6', 'border': '2px solid black',
        'border-radius': '10px', 'padding': '10px',
        'padding-left': '10%', 'padding-right': '10%',
        'width': '650px'
    }

    # create logic for cards display to enable dataset comparisons
    # instantiate row component that takes list of tables

    demographicsComponentCards = pn.Column()

    for (dataset, name) in zip(populationTableList, dfKeyList):
        cardColorList = highlightImputedDataset(name)
        demographicsComponentCards.append(
            pn.Card(pn.pane.HTML(dataset, margin=25, styles=tableStyles),
                title=f"{name.capitalize()} dataset",
                header_background=cardColorList[0],
                header_color=cardColorList[1],
                styles={'background':cardColorList[2], 
                        'border-radius': '10px'},
                stylesheets=[cardHeaderStylesheet]))

    return pn.Row(
        pn.layout.HSpacer(),
        demographicsComponentCards,
        pn.layout.HSpacer())