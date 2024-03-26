import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
from itertools import repeat
import dash_mantine_components as dmc
from functions.variable_store import *
from functions.load_datasets import *
from functions.prettify_plots import *

dash.register_page(__name__, name="Descriptive Plots - Scores")

layout = html.Div([

    html.Div([
        dmc.LoadingOverlay(children=
            [html.Div(id="sexCompareViolin", className='mx-auto w-11/12'),
            html.Div(id="timeCompareViolin", className='mx-auto w-11/12'),],
            loaderProps={"size":"xl"},
            className="container mx-auto md:columns-2 min-h-20",
            overlayOpacity=0
        )], className="mx-auto w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),
    
    html.Div([
        dmc.LoadingOverlay(children=
            [html.Div(id="subsystemCompareViolin", className='mx-auto w-11/12'),
            html.Div(id="biomarkerCompareViolin", className='mx-auto w-11/12')],
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="conta,iner mx-auto md:columns-2 bg-opacity-0"
        )], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),

])  


def getSplitViolinDf(df):
    splitViolinDf = df[["sex"] + bhsScoreCols].copy().melt("sex")
    
    subsystemViolinDf = df[subsystemBaseline + subsystemFollowup].copy().melt()
    subsystemViolinDf = unmeltTimepoints(subsystemViolinDf)

    deltaSubsystemCols = ["delta_biomarker_" + x + "_score.1.0" for x in subsystemList]
    deltaBiomarkerViolinDf = df[deltaSubsystemCols].copy().melt()
    deltaBiomarkerViolinDf.loc[:,"type"] = "delta" 
    deltaBiomarkerViolinDf["variable"] = deltaBiomarkerViolinDf["variable"].str.replace("_score....", "", regex=True)
    deltaBiomarkerViolinDf["variable"] = deltaBiomarkerViolinDf["variable"].str.replace("delta_biomarker_", "", regex=True)

    deltaSubsystemDf = (df[subsystemFollowup] - df[subsystemBaseline].values).copy().melt()
    deltaSubsystemDf.loc[:,"type"] = "bhs"
    deltaSubsystemDf["variable"] = deltaSubsystemDf["variable"].str.replace("_score....", "", regex=True)
    deltaBiomarkerViolinDf = pd.concat([deltaBiomarkerViolinDf, deltaSubsystemDf])

    return splitViolinDf, subsystemViolinDf, deltaBiomarkerViolinDf

@callback(
    Output("sexCompareViolin", "children"),
    Output("timeCompareViolin", "children"),
    Output("subsystemCompareViolin", "children"),
    Output("biomarkerCompareViolin", "children"),
    Input("selectBhsType_radioItems", "value")
)
def showBhsPreview(selectBhsType_radioItems):
    df = getDf(selectBhsType_radioItems, filepathDict)

    # get violin df
    splitViolinDf, subsystemViolinDf, deltaBiomarkerViolinDf = getSplitViolinDf(df)

    ### make plots ###
    sexCompareViolin = dcc.Graph(figure=(go.Figure()
        .add_trace(go.Violin(
            x=splitViolinDf["variable"][ splitViolinDf["sex"] == "Male"],
            y=splitViolinDf["value"][ splitViolinDf["sex"] == "Male"], side='negative',
            width=0.5, name="Male"))
        .add_trace(go.Violin(
            x=splitViolinDf["variable"][ splitViolinDf["sex"] == "Female"],
            y=splitViolinDf["value"][ splitViolinDf["sex"] == "Female"], side='positive',
            width=0.5, name="Female"))
        .update_traces(meanline_visible=True)
        .update_layout(violinmode='overlay', violingap=0,
                        title=centerPlotTitle('Male vs Female'),
                        margin=dict(l=10,r=10,b=8),
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        legend=dict(orientation="h", yanchor="bottom", y=1.05,
                        xanchor="center", x=0.5))),
        config={'displayModeBar':False})
    
    timeCompareViolin = dcc.Graph(figure=(go.Figure()
        .add_trace(go.Violin(
            x=splitViolinDf["sex"][ splitViolinDf["variable"] == "bhs_score.0.0"],
            y=splitViolinDf["value"][ splitViolinDf["variable"] == "bhs_score.0.0"], side='negative',
            width=0.5, name="Baseline (t0)", line_color="black", fillcolor="yellow", opacity=0.6))
        .add_trace(go.Violin(
            x=splitViolinDf["sex"][ splitViolinDf["variable"] == "bhs_score.1.0"],
            y=splitViolinDf["value"][ splitViolinDf["variable"] == "bhs_score.1.0"], side='positive',
            width=0.5, name="Followup (t1)", line_color="black", fillcolor="limegreen", opacity=0.6))
        .update_traces(meanline_visible=True)
        .update_layout(violinmode='overlay', violingap=0,
                        title=centerPlotTitle('BHS Baseline vs Followup'),
                        margin=dict(l=10,r=10,b=8),
                        legend=dict(orientation="h", yanchor="bottom", y=1.05,
                        xanchor="center", x=0.5))),
        config={'displayModeBar':False})
    
    subsystemCompareViolin = dcc.Graph(figure=(go.Figure()
        .add_trace(go.Violin(
            x=subsystemViolinDf["variable"][ subsystemViolinDf["timepoint"] == "t0"],
            y=subsystemViolinDf["value"][ subsystemViolinDf["timepoint"] == "t0"], side='negative',
            width=0.5, name="Baseline (t0)", line_color="black", fillcolor="yellow", opacity=0.6))
        .add_trace(go.Violin(
            x=subsystemViolinDf["variable"][ subsystemViolinDf["timepoint"] == "t1"],
            y=subsystemViolinDf["value"][ subsystemViolinDf["timepoint"] == "t1"], side='positive',
            width=0.5, name="Followup (t1)", line_color="black", fillcolor="limegreen", opacity=0.6))
        .update_traces(meanline_visible=True)
        .update_layout(violinmode='overlay', violingap=0,
                        title=centerPlotTitle('Subsystem Scores <br>Baseline vs Followup'),
                        margin=dict(l=10,r=10,b=8),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="center", x=0.5))),
        config={'displayModeBar':False})
    
    biomarkerCompareViolin = dcc.Graph(figure=(go.Figure()
        .add_trace(go.Violin(
            x=deltaBiomarkerViolinDf["variable"][ deltaBiomarkerViolinDf["type"] == "bhs" ],
            y=deltaBiomarkerViolinDf["value"][ deltaBiomarkerViolinDf["type"] == "bhs" ], side='negative',
            width=0.5, name="BHS (t1-t0)", line_color="black", fillcolor="orange", opacity=0.6))
        .add_trace(go.Violin(
            x=deltaBiomarkerViolinDf["variable"][ deltaBiomarkerViolinDf["type"] == "delta" ],
            y=deltaBiomarkerViolinDf["value"][ deltaBiomarkerViolinDf["type"] == "delta" ], side='positive',
            width=0.5, name="Delta Biomarker", line_color="black", fillcolor="pink", opacity=0.6))
        .update_layout(violinmode='overlay', violingap=0,
                        title=centerPlotTitle('Subsystem comparison <br>∆BHS vs ∆Biomarker'),
                        title_automargin=True,
                        margin=dict(l=10,r=10,b=8),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="center", x=0.5))),
        config={'displayModeBar':False})

    return sexCompareViolin, timeCompareViolin, \
        subsystemCompareViolin, biomarkerCompareViolin

