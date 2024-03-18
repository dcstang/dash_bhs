import dash
from dash import html, dcc, callback, Input, Output
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import repeat
import dash_mantine_components as dmc
from functions.variable_store import *
from functions.load_datasets import *
from functions.prettify_plots import *

dash.register_page(__name__, name="Descriptive Plots - Biomarkers")

layout = html.Div([

    html.Div([
        dmc.LoadingOverlay(
            children=html.Div(id="allBiomarkersBox", className='mx-auto w-11/12'),
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="container mx-auto")
        ], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),

    html.Div([
        dmc.LoadingOverlay(
            children=[
                html.Div(id="changeBiomarkersFig", className='mx-auto w-11/12'),
                html.Div(id="scaledChangeBiomarkersFig", className='mx-auto w-11/12')],
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="container mx-auto"),            
        ], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),

    html.Div([
        dmc.LoadingOverlay(
            children=html.Div(id="changeBiomarkerScoresFig", className='mx-auto w-11/12'),
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="container mx-auto")
        ], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),

])  

@callback(
    Output("allBiomarkersBox", "children"),
    Output("changeBiomarkersFig", "children"),
    Output("scaledChangeBiomarkersFig", "children"),
    Output("changeBiomarkerScoresFig", "children"),
    Input("selectBhsType_radioItems", "value")
)
def showBhsPreview(selectBhsType_radioItems):
    df = getDf(selectBhsType_radioItems, filepathDict)

    # get biomarkers df
    allBiomarkerList = getBiomarkerNames([metabol, cardio, inflam, renal, hepato], ".0.0", ".1.0") 
    allBiomarkerDfListGen = map(allBiomarkersDistribution, repeat(df), allBiomarkerList, subsystemList)
    allBiomarkerDf = getBiomarkersPlotDf(allBiomarkerDfListGen)

    # biomarker change
    changeBiomarkersDfListGen = map(meanChangeDf, repeat(df), [metabol, cardio, inflam, renal, hepato], subsystemList)
    changeBiomarkersDf = getBiomarkersPlotDf(changeBiomarkersDfListGen)

    bhsScoreList = getBiomarkerNames([metabol, cardio, inflam, renal, hepato], "_score.0.0", "_score.1.0")
    changeBiomarkerScoresDfListGen = map(changeBiomarkersGroup, repeat(df), bhsScoreList, subsystemList)
    changeBiomarkerScoresDf = getBiomarkersPlotDf(changeBiomarkerScoresDfListGen)

    ###--- biomarkers section     ---###
     
    nRows = -(-len(shortenNameDict)//5) # ceiling division
    allBiomarkersBox = make_subplots(rows=nRows, cols=5,
                                    subplot_titles=list(shortenNameDict.values()))

    for idx, biomarker in enumerate(shortenNameDict.values()):
        allBiomarkersBox.add_trace(
            go.Box(name="t0",
            y=allBiomarkerDf[ (allBiomarkerDf["variable"] == biomarker) &
                              (allBiomarkerDf["timepoint"] == "t0") ]["value"],
            boxpoints=False, whiskerwidth=0.2), 
        row =idx//5+1, col=idx%5+1)
        allBiomarkersBox.add_trace(
            go.Box(name="t1",
            y=allBiomarkerDf[ (allBiomarkerDf["variable"] == biomarker) & 
                              (allBiomarkerDf["timepoint"] == "t1") ]["value"],
            boxpoints=False, whiskerwidth=0.2), 
        row =idx//5+1, col=idx%5+1)
    allBiomarkersBox.update_layout(
        title=centerPlotTitle("All Biomarkers"),
        margin=dict(l=10,r=10,b=5),
        showlegend=False)
        # legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5))

    allBiomarkersBox = dcc.Graph(figure=allBiomarkersBox,
        style={"height":700}, config={'displayModeBar':False})

    ### ----------- ###
    changeBiomarkersFig = dcc.Graph(figure=(
        px.scatter(changeBiomarkersDf, y="index", x="mean", 
                   error_x="ci", color="subsystem")
        .update_layout(
            yaxis_title=None,xaxis_title=None,
            margin=dict(l=10,r=10,b=5),
            title=centerPlotTitle("Mean change <br>(95%CI)"))),
        config={'displayModeBar':False})

    scaledChangeBiomarkersFig = dcc.Graph(figure=(
        px.scatter(changeBiomarkersDf, y="index", x="scaledMean", 
                   error_x="scaledCi", color="subsystem")
        .update_layout(
            yaxis_title=None,xaxis_title=None,
            margin=dict(l=10,r=10,b=5),
            title=centerPlotTitle("Mean change (Rescaled) <br>(95%CI)"))),
        config={'displayModeBar':False})

    changeBiomarkerScoresFig = make_subplots(rows=1, cols=5, shared_yaxes=True)
    for idx, col in enumerate(subsystemList):
         changeBiomarkerScoresFig.add_trace(
            go.Bar(name=col,
                x=changeBiomarkerScoresDf[ changeBiomarkerScoresDf["subsystem"] == col ]["variable"],
                y=changeBiomarkerScoresDf[ changeBiomarkerScoresDf["subsystem"] == col ]["value"],
                marker_line=dict(width=2, color='black')),
            row=1, col=idx+1 )
    changeBiomarkerScoresFig.update_layout(
        title=centerPlotTitle("Total score change <br>in biomarkers"),
        margin=dict(l=10,r=10,b=5),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
         
    changeBiomarkerScoresFig = dcc.Graph(figure=changeBiomarkerScoresFig,
            config={'displayModeBar':False})

    return allBiomarkersBox, changeBiomarkersFig, \
        scaledChangeBiomarkersFig,changeBiomarkerScoresFig


