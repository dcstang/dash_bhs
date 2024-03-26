import pandas as pd
import numpy as np
import sys

sys.path.append("../")
from functions.variable_store import *

completeDf = pd.read_parquet("../data/06_ukbb_outcome_trimmed_diet_bhs_complete_cases_dash.parquet")
imputeDf = pd.read_parquet("../data/06_ukbb_outcome_trimmed_diet_bhs_knn_impute_dash.parquet")

def simpleFactoriseData(df):
    """
        simplified factors from main work for app demonstration purposes
    """
    df["reg_ps"] = np.select(
        [df["regular_prescription_meds.0.0"] == "Prefer not to answer",
        df["regular_prescription_meds.0.0"] == "Do not know",
        df["regular_prescription_meds.0.0"] == "No",
        df["regular_prescription_meds.0.0"] == "Yes - you will be asked about this later by an interviewer"],
        ["Unknown", "Unknown", "No", "Yes"],
        default="Unknown")

    df["qual_factor"] = np.select(
        [df["qualifications.0.0"] == "NVQ or HND or HNC or equivalent",
        df["qualifications.0.0"] == "Other professional qualifications eg: nursing, teaching",
        df["qualifications.0.0"] == "CSEs or equivalent",
        df["qualifications.0.0"] == "A levels/AS levels or equivalent",
        df["qualifications.0.0"] == "O levels/GCSEs or equivalent",
        df["qualifications.0.0"] == "College or University degree"],
        ["Diploma/Vocational", "Diploma/Vocational", "High school", "High school",
         "High school", "Tertiary education"],
        default="Unknown")  

    df["alcohol.0.0"] = np.where(
        df["alcohol.0.0"] == "Special occasions only",
        "One to three times a month",
        df["alcohol.0.0"])

    df["alcohol.0.0"] = np.where(
        df["alcohol.0.0"] == "Prefer not to answer",
        "Unknown",
        df["alcohol.0.0"])

    df["alcohol.0.0"] = np.where(
        df["alcohol.0.0"] == "One to three times a month",
        "Ocassionally to three times a month",
        df["alcohol.0.0"])

    df["smoking_status.0.0"] = np.where(
        pd.isnull(df["smoking_status.0.0"]),
        "Prefer not to answer",
        df["smoking_status.0.0"])

    return df

def getPopulationDemographics(df):
    df = simpleFactoriseData(df)
    demographicsList = ["age.0.0", "sex", "BMI.0.0", "alcohol.0.0", "smoking_status.0.0",
                        "reg_ps", "qual_factor"]
    return df[demographicsList]

getPopulationDemographics(completeDf).to_parquet("../data/subset/complete_demographics.parquet")
getPopulationDemographics(imputeDf).to_parquet("../data/subset/impute_demographics.parquet")
