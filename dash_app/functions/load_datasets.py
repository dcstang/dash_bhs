import pandas as pd
from functions.variable_store import *
from sklearn.preprocessing import MinMaxScaler

def getDf(bhsName, filepathDict):
    bhsFilepath = filepathDict[bhsName]
    df = pd.read_parquet(bhsFilepath)
    df = df.reset_index()
    return df

def unmeltTimepoints(df):
    # pullout t0 and t1 into separate col
    df.loc[df["variable"].str.contains(".0.0", regex=False),"timepoint"] = "t0" 
    df.loc[df["variable"].str.contains(".1.0", regex=False),"timepoint"] = "t1" 
    df["variable"] = df["variable"].str.replace("_score....", "", regex=True)
    df["variable"] = df["variable"].str.replace(".[0-9].[0-9]", "", regex=True)
    return df


    ### biomarkers section fx ###
def allBiomarkersDistribution(df, scoreList, subsystemName):
    """
        get all biomarkers, unmelt and specify:
            timepoint and subsystem
    """
    outputDf = unmeltTimepoints(df[scoreList].copy().melt())
    outputDf.loc[:,"subsystem"] = subsystemName

    return outputDf


def changeBiomarkersGroup(df, scoreList, subsystemName):
    """
        get all biomarkers, split by t0 vs t1
        subtract biomarker level summed score
        # crushing total score by using sum of values?
        # maybe groupby count instead of sum

        show biomarker score change on individual level ie
                cardio,t0    cardio,t1
        eid 1      0           1         -> change +1
        eid 2      0           0         -> change 0
        eid 3      1           0         -> change  -1
        eid 4      1           1         -> change 0 

                then show as grouped bar of 
                #1 - worsening change (+1)
                #2 - no change 
                #3 - improving change (-1)

    """
    outputDf = (df[scoreList]
        .copy().melt()
        .groupby("variable").sum()
        .astype(dict(value="int16"))
        .reset_index())
    
    outputDf = unmeltTimepoints(outputDf)
    outputDf.loc[:,"subsystem"] = subsystemName
    
    subtraction = (outputDf.groupby("variable").last()["value"] - 
        outputDf.groupby("variable").first()["value"]).reset_index()

    outputDf = (outputDf[["variable", "subsystem"]]
                .drop_duplicates("variable"))

    outputDf = pd.merge(outputDf, subtraction, how="left", on="variable")    

    return outputDf

def meanChangeDf(df, biomarkerList, subsystemName):
    """
        biomarker distribution t1 vs t0 comparison
        could be useful to check the mean change and ci
            df t1 - df t0
            df.mean() +/- df.sd()
    """
    scaler = MinMaxScaler((-100,100)).set_output(transform="pandas")

    interimDf = df[[x+".1.0" for x in biomarkerList]] - df[[x+".0.0" for x in biomarkerList]].values
    scaledInterimDf = scaler.fit_transform(interimDf)

    outputDf = (pd.concat([interimDf.mean(), 
                          1.96*interimDf.std(),
                          scaledInterimDf.mean(),
                          1.96*scaledInterimDf.std()], axis=1)
                    .rename(columns={0:"mean", 1:"ci", 2:"scaledMean", 3:"scaledCi"})
                    .reset_index())
    outputDf["index"] = outputDf["index"].str.replace(".1.0", "")
    outputDf["subsystem"] = subsystemName
    return outputDf

def expandBiomarkerString(subsystemList, expansion_string, expansion_string2):
    # exclude delta_biomarkers first
    expandedList = [ baseline+expansion_string for baseline in subsystemList ] + \
            [ followup+expansion_string2 for followup in subsystemList ] 
            # [ "delta_biomarker_"+delta+"_score.1.0" for delta in subsystemList]
    return expandedList

def getBiomarkerNames(bhsList, expansion_string, expansion_string2):
    return [expandBiomarkerString(x, expansion_string, expansion_string2) for x in bhsList]

def getBiomarkersPlotDf(dfListGenerator):
    # because we are using map to pull in multiple lists
    return pd.concat(list(dfListGenerator)).replace(shortenNameDict)