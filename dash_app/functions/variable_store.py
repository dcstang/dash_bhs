filepathList = ["data/06_ukbb_outcome_trimmed_diet_bhs_complete_cases_dash.parquet",
    "data/06_ukbb_outcome_trimmed_diet_bhs_complete_cases_pca_subsystem_dash.parquet",
    "data/06_ukbb_outcome_trimmed_diet_bhs_lq_complete_cases_dash.parquet",
    "data/06_ukbb_outcome_trimmed_diet_bhs_knn_impute_dash.parquet",
    "data/06_ukbb_outcome_trimmed_diet_bhs_knn_impute_pca_subsystem_dash.parquet",
    "data/06_ukbb_outcome_trimmed_diet_bhs_lq_knn_impute_dash.parquet"]

bhsNames = ["Complete cases",
            "Complete cases + PCA Biomarker BHS",
            "Complete cases + Q1 Scoring Biomarker BHS",
            "KNN impute",
            "KNN impute + PCA Biomarker BHS",
            "KNN impute + Q1 Scoring Biomarker BHS"]

filepathDict = dict(zip(bhsNames, filepathList))

# top badge decorations
badgeList = [
    "inline-flex mx-2 items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20",
    "inline-flex mx-2 items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10",
    "inline-flex mx-2 items-center rounded-md bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10",
    "inline-flex mx-2 items-center rounded-md bg-purple-50 px-2 py-1 text-xs font-medium text-purple-700 ring-1 ring-inset ring-purple-700/10"
]


# define columns
bhsScoreCols = ["bhs_score.0.0", "bhs_score.1.0", "delta_bhs", "delta_biomarker_bhs"]
cleanBhsNames = ["BHS (Baseline)", "BHS (Followup)", "\u0394 BHS", " \u0394 Biomarker Score"]
subsystemList = ["metabol", "cardio", "inflam", "renal", "hepato"]
subsystemBaseline = [x+"_score.0.0" for x in subsystemList]
subsystemFollowup = [x+"_score.1.0" for x in subsystemList]

metabol    = ["glycated_haemoglobin","HDL_cholesterol","LDL_direct","triglycerides"]
cardio     = ["systolic_bp","diastolic_bp","pulse_rate"]
inflam     = ["c.reactive_protein","IGF1"]
renal      = ["creatinine", "cystatin_C"]
hepato     = ["alanine_aminotransferase","aspartate_aminotransferase","gamma_glutamyltransferase"]

shortenNameDict = dict(zip(
    metabol + cardio + inflam + renal + hepato,
    ["A1c", "HDLc", "LDL", "TG"] + 
    ["Systolic BP", "Diastolic BP", "Pulse rate"] +
    ["CRP", "IFG-1"] +
    ["Creatinine", "Cystatin C"] +
    ["ALT", "AST", "GGT"]))
