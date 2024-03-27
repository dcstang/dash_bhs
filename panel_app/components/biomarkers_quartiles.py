import panel as pn
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

introSection = pn.pane.Markdown(
"""
## Background on biomarkers
The Biological Health Score (BHS) is made up of 14 `biomarkers`. These are derived from both blood and clinical measurements.  

The eventual scoring depends on somewhat arbitary thresholds / cutoff points in these measurements.   
We want to make sure that these levels are not skewed when imputing the population size.
""")

def testBiomarkers(dfKeyList):
    # needs to be able to handle list

    outputList = []

    for key in dfKeyList:
        df = pd.read_parquet(f"data/{key}_biomarkers.parquet")
            
        fig, ax = plt.subplots(figsize=(3,5))            
        sns.kdeplot(df["pulse_rate.0.0"], ax=ax)

        outputList.append(fig)

    return outputList

def generateBiomarkersComponent(dfKeyList):
    biomarkersComponentList = pn.Column()
    biomarkersComponentList.append(introSection)

    biomarkersComponentList.append(dfKeyList)

    biomarkersDistributionList = testBiomarkers(dfKeyList)

    for (fig, name) in zip(biomarkersDistributionList, dfKeyList):
        biomarkersComponentList.append(
            pn.Card(pn.pane.Matplotlib(fig, tight=True),
            title=f"{name.capitalize()} dataset"))

    return biomarkersComponentList