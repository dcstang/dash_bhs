import panel as pn
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from components.variable_store import cardHeaderStylesheet

custom_params = {"axes.spines.right": False,
                "axes.spines.top": False,
                "figure.dpi": 300}
sns.set_theme(style="white", rc=custom_params, font_scale=0.5)

introSection = pn.pane.Markdown(
"""
## Background on biomarkers
The Biological Health Score (BHS) is made up of 14 biomarkers. These are derived from both blood and clinical measurements.  

The scoring depends on somewhat arbitary thresholds / cutoff points in these measurements.   
We want to make sure that these levels are not skewed when imputing the population size.

So, the area in the `highest quartile (Q3-Q4)` are highlighted for quick visual comparison.
""")

def distributionBiomarkers(dfKeyList):

    outputList = []
    # define column names
    metabol    = ["glycated_haemoglobin","HDL_cholesterol","LDL_direct","triglycerides"]
    cardio     = ["systolic_bp","diastolic_bp","pulse_rate"]
    inflam     = ["c.reactive_protein","IGF1"]
    renal      = ["creatinine", "cystatin_C"]
    hepato     = ["alanine_aminotransferase","aspartate_aminotransferase","gamma_glutamyltransferase"]
    biomarkersList = metabol + cardio + inflam + renal + hepato
    biomarkersList = [x+".0.0" for x in biomarkersList]

    shortenNameDict = dict(zip(
        biomarkersList,
        ["A1c", "HDLc", "LDL", "TG"] + 
        ["Systolic BP", "Diastolic BP", "Pulse rate"] +
        ["CRP", "IFG-1"] +
        ["Creatinine", "Cystatin C"] +
        ["ALT", "AST", "GGT"]))

    for key in dfKeyList:
        df = pd.read_parquet(f"data/{key}_biomarkers.parquet")
            
        fig, axes = plt.subplots(
            ncols=3, nrows=5, sharey="row",
            figsize=(2.5*3,1.5*5),
            gridspec_kw={"wspace":0})
        axes = axes.flatten()

        for idx, biomarker in enumerate(biomarkersList):
            points = sns.kdeplot(df[biomarker], ax=axes[idx]).get_lines()[0].get_data()
            axes[idx].set_xlabel(None)
            axes[idx].patch.set_facecolor('none')
            axes[idx].text(0.95, 0.9, shortenNameDict[biomarker], 
                           transform=axes[idx].transAxes, 
                            weight='bold', ha="right")

            x = points[0]
            y = points[1]

            axes[idx].fill_between(x, y, 
                where = (x > df[biomarker].quantile(0.75)),
                color='#0000CD')

        axes[-1].set_visible(False)
        fig.patch.set_facecolor('none')    
        fig.tight_layout()
        outputList.append(fig)

    return outputList

def highlightImputedDataset(dfKey=None):
    """
        function to check which card and apply specific 
    """
    if dfKey == "complete":
        return ["#bebebe", "#0", "#d3d3d340"]
    else:
        return ["#0000CD", "#ffffff", "#5c9ac810"]

def generateBiomarkersComponent(dfKeyList):
    biomarkersComponentList = pn.Column()
    biomarkersComponentList.append(introSection)

    biomarkersDistributionList = distributionBiomarkers(dfKeyList)
    print(cardHeaderStylesheet)

    for (fig, name) in zip(biomarkersDistributionList, dfKeyList):
        cardColorList = highlightImputedDataset(name)

        biomarkersComponentList.append(
            pn.Card(pn.pane.Matplotlib(fig, tight=True),
            title=f"{name.capitalize()} dataset",
            header_background=cardColorList[0],
            header_color=cardColorList[1],
            background=cardColorList[2],
            stylesheets=[cardHeaderStylesheet],
            styles={'border-radius': '10px'}))

    return biomarkersComponentList