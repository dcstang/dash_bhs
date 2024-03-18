import dash
from dash import html, callback, Input, Output
import dash_mantine_components as dmc
import dash_ag_grid as dag
from functions.variable_store import *
from functions.load_datasets import *

dash.register_page(__name__)

layout = html.Div([

    html.Div(
        children=[
            html.Div(id="printbhsSelected",
                className="mx-auto text-center font-bold mt-8 -mb-2"),
            dmc.LoadingOverlay(html.Div(id="bhsPreviewTableMainScores",
                className='rounded-lg overflow-hidden shadow-lg align-center'),
                loaderProps={"size":"xl"},
                overlayBlur=1,
                overlayOpacity=0,
                className="m-4 w-11/12"),
            dmc.LoadingOverlay(html.Div(id="bhsPreviewTableSubsystemScores_baseline",
                className='rounded-md overflow-hidden shadow-lg'),
                loaderProps={"size":"xl"}, 
                overlayBlur=1,
                overlayOpacity=0,
                className="m-4 w-11/12"),
            dmc.LoadingOverlay(html.Div(id="bhsPreviewTableSubsystemScores_followup",
                className='rounded-md overflow-hidden shadow-lg'),
                loaderProps={"size":"xl"}, 
                overlayBlur=1,
                overlayOpacity=0,
                className="m-4 w-11/12")
        ], className="flex flex-col gap-2 items-center text-center"),

])

@callback(
    Output("printbhsSelected", "children"),
    Output("bhsPreviewTableMainScores", "children"),
    Output("bhsPreviewTableSubsystemScores_baseline", "children"),
    Output("bhsPreviewTableSubsystemScores_followup", "children"),
    Input("selectBhsType_radioItems", "value")
)
def showBhsPreview(selectBhsType_radioItems):
    df = getDf(selectBhsType_radioItems, filepathDict)
    ###--- preview tables section ---###
    scoresDf = dag.AgGrid(
        id="scores",
        rowData=(df[bhsScoreCols].head(8)
            .round(2)
            .to_dict('records')), 
        columnDefs=[{"field": i, "headerName": j}
                     for i,j in zip(bhsScoreCols, cleanBhsNames)],
        columnSize="responsiveSizeToFit",
        style={"height":"270px"},
        dashGridOptions={"pagination": True, "paginationPageSizeSelector": False,
                        "paginationPageSize": 4,
                            "suppressFieldDotNotation" : True})
    
    subsystemDf_baseline = dag.AgGrid(
        id="subsystemScorest0",
        rowData=(df[subsystemBaseline].head(8)
            .round(2)
            .to_dict('records')), 
        columnDefs=[{"field": i, "headerName": j + " (baseline)"}
                     for i,j in zip(subsystemBaseline, subsystemList)],
        columnSize="responsiveSizeToFit",
        style={"height":"270px"},
        dashGridOptions={"pagination": True, "paginationPageSizeSelector": False,
                        "paginationPageSize": 4,
                            "suppressFieldDotNotation" : True})

    subsystemDf_followup = dag.AgGrid(
        id="subsystemScorest1",
        rowData=(df[subsystemFollowup].head(8)
            .round(2)
            .to_dict('records')), 
        columnDefs=[{"field": i, "headerName": j + " (followup)"}
                     for i,j in zip(subsystemFollowup, subsystemList)],
        columnSize="responsiveSizeToFit",
        style={"height":"270px"},
        dashGridOptions={"pagination": True, "paginationPageSizeSelector": False,
                        "paginationPageSize": 4,
                            "suppressFieldDotNotation" : True})

    return f"Dataframe preview for {selectBhsType_radioItems}, N={len(df)}",\
        scoresDf, subsystemDf_baseline, subsystemDf_followup