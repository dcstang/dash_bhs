import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import dash_mantine_components as dmc
import pingouin as pg
from functions.variable_store import *
from functions.load_datasets import *
from functions.prettify_plots import *

dash.register_page(__name__, name="Score correlations")

bhsType = filepathList[0]
df = pd.read_parquet(bhsType)[bhsScoreCols]
corrDf = df[bhsScoreCols].corr().round(2)

partialDf = df.pcorr().round(2)
partialCorrDf = pg.partial_corr(data=df, x="delta_bhs", y="delta_biomarker_bhs", covar="bhs_score.0.0")
print(partialCorrDf)

layout = html.Div([

    html.Div([
        dmc.LoadingOverlay(
            children=
                html.Div(
                children=dcc.Graph(figure=(
                    px.imshow(corrDf, text_auto=True)
                    .update_layout(coloraxis_showscale=False, 
                        title=centerPlotTitle("Correlation Matrix"))),
                    config={'displayModeBar':False}),
                className='mx-auto'),
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="container mx-auto")
        ], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),
    
    html.Div([
        dmc.LoadingOverlay(
            children=html.Div(
                children=dcc.Graph(figure=(
                    px.imshow(partialDf, text_auto=True)
                    .update_layout(coloraxis_showscale=False,
                        title=centerPlotTitle("Partial Correlation Matrix"))),
                    config={'displayModeBar':False}),
                className='mx-auto w-11/12'),
            loaderProps={"size":"xl"},
            overlayOpacity=0,
            className="container mx-auto")
        ], className="mx-auto mt-2 w-11/12 rounded-lg overflow-hidden shadow-lg bg-white"),

])  
