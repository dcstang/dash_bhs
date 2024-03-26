import panel as pn
import pandas as pd
import plotly.express as px
from functions.summariseDemographics import runTableOne

# completeDf = pd.read_parquet("data/complete_demographics.parquet")
# imputeDf = pd.read_parquet("data/impute_demographics.parquet")

sidebarInfo = pn.pane.HTML("<h2>⚙️ Settings</h2>")
sidebarMore = pn.pane.Markdown("Use these settings to explore variations of the results")
datasetType = pn.widgets.Select(name="Dataset type", 
                                options=["Original", "Imputed"], 
                                size=2, width=200)

template = pn.template.MaterialTemplate(
    title="Biological Health Score | Scientific Dashboard",
    sidebar=[sidebarInfo, sidebarMore, datasetType],
    collapsed_sidebar=True,
    sidebar_width=280
)

demographicsTable = pn.bind(runTableOne, datasetType)

template.main.append(
    pn.Tabs(
    ("Population Demographics", 
        pn.pane.HTML(demographicsTable, margin=25)),
    ("Biomarkers", pn.Accordion("test"))
))

template.servable()
