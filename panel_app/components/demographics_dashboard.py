import pandas as pd
import panel as pn
import plotly.express as px
from components.variable_store import cardHeaderStylesheet

    # for key in dfKeyList:
    #     df = pd.read_parquet(f"data/{key}_demographics.parquet")
    #     tableOneCols = [

            # "age.0.0",
            # "sex",
            # "BMI.0.0",
            # "qual_factor",
            # "smoking_status.0.0",
            # "reg_ps",
            # "alcohol.0.0"]

        # orderingDict = {
        #         "reg_ps"      : ["Yes", "No", "Unknown"],
        #         "qual_factor" : ["High school", "Diploma/Vocational", "Tertiary education"],
        # "smoking_status.0.0" : [ 'Current', 'Previous', 'Never', 'Prefer not to answer'],
        #         "alcohol.0.0" : ['Daily or almost daily', 'Once or twice a week',
        #                         'Three or four times a week', 
        #                         'Ocassionally to three times a month',
        #                         'Never', "Unknown"]
        # }
        # categoricalList = [
        #         "qual_factor", "sex",
        #         "smoking_status.0.0", "reg_ps", "alcohol.0.0"]
        
        # renameDict = {
        #     "n":"Population size",
        #     "age.0.0": "Age",
        #     "sex":"Sex",
        #     "BMI.0.0":"BMI",
        #     "qual_factor":"Education",
        #     "smoking_status.0.0":"Smoking",
        #     "reg_ps":"Prescription medications",
        #     "alcohol.0.0":"Alcohol intake"}

def highlightImputedDataset(dfKey=None):
    """
        function to check which card and apply specific 
    """
    if dfKey == "complete":
        return ["#bebebe", "#0", "#d3d3d340"]
    else:
        return ["#0000CD", "#ffffff", "#5c9ac830"]

def makeDashboardCardFirstRow(innerCardObject, cardWidth, cardHeight):
    # 3 cards in a row
    cardStyles = {
        'border': '1px solid black',
        'border-radius': '10px',
        'flex': '0 0 30%'
    }
    return pn.Card(
            innerCardObject, styles=cardStyles,
            hide_header=True, min_width=cardWidth, min_height=cardHeight)

def makeDashboardCardSecondRow(innerCardObject, cardWidth, cardHeight):
    # 2 cards in a row
    cardStyles = {
        'border': '1px solid black',
        'border-radius': '10px',
        'flex': '0 0 45%'
    }
    return pn.Card(
            innerCardObject, styles=cardStyles,
            hide_header=True, min_width=cardWidth, min_height=cardHeight)

def singleDatasetView(dfKey):
    """
        main dashboard function
        output: flexible and responsive cards in flexbox
        input : dataframe type
    """
    df = pd.read_parquet(f"data/{dfKey}_demographics.parquet")

    demographicsDashboard = pn.FlexBox(
        flex_direction="row",
        flex_wrap="wrap",
        justify_content="space-evenly",
        objects=[pn.Row(
            pn.HSpacer(),
            pn.pane.Markdown(f"# {dfKey.capitalize()} dataset"),
            pn.HSpacer()),
            pn.layout.Divider()])
    
    cardWidth = 200
    cardHeight = 147

    # top row cards
    firstRow = [
        makeDashboardCardFirstRow(
            cardWidth=cardWidth, 
            cardHeight=cardHeight,
            innerCardObject=pn.indicators.Number(
                value=len(df), default_color='darkgray', align="center",
                name="Total Patients", format='{value:,}')),
        makeDashboardCardFirstRow(
            cardWidth=cardWidth, 
            cardHeight=cardHeight,
            innerCardObject=pn.indicators.Number(
                value=df["age.0.0"].mean().astype(int), 
                default_color='darkgray', align="center",
                name="Avg age", format='{value} yr')),
        makeDashboardCardFirstRow(
            cardWidth=cardWidth, 
            cardHeight=cardHeight,
            innerCardObject=pn.pane.Plotly(
            (
                px.pie(
                    df.groupby(['sex'])['sex'].count().reset_index(name='count'), 
                    values="count", names="sex", hole=.45, color="sex",
                    height=cardHeight*0.9,
                    color_discrete_map={"Female": "#0000CD", "Male" : "lightgray"})
                .update_layout(margin=dict(l=0, r=0, t=0, b=0))
                .update_traces(
                    textposition='inside', textinfo='percent+label',
                    showlegend=False)
                .add_annotation(x=0.5,y=0.5,text="Sex",
                                showarrow=False, xanchor="center",
                                xref="paper",yref="paper",
                                font=dict(color='darkgray'))
            ),                 
                sizing_mode="stretch_width", 
                config={'displayModeBar': False}))
    ]

    demographicsDashboard.extend(firstRow)

    secondRow = [
        makeDashboardCardSecondRow(
            cardWidth=300,
            cardHeight=220,
            innerCardObject=pn.pane.Plotly(
            (   px.histogram(df, x="alcohol.0.0", histfunc="sum", 
                             template="simple_white", 
                             color_discrete_sequence=["#0000CD"])
                .update_layout(margin=dict(l=0, r=0, t=0, b=0),
                               yaxis_title="Counts",
                               xaxis_title=None,
                               xaxis={'categoryorder':'total descending'})
                .add_annotation(x=1,y=0.98,text="Alcohol Intake",
                                showarrow=False, xanchor="right",
                                xref="paper",yref="paper",
                                font=dict(color='darkgray',size=24))
            ),
                sizing_mode="stretch_width",
                config={'displayModeBar': False}
            )
        ),
        makeDashboardCardSecondRow(
            cardWidth=300,
            cardHeight=220,
            innerCardObject=pn.pane.Plotly(
            (   px.histogram(df, x="smoking_status.0.0", histfunc="sum", 
                             color_discrete_sequence=["#0000CD"],
                             template="simple_white")
                .update_layout(margin=dict(l=0, r=0, t=0, b=0),
                               yaxis_title="Counts",
                               xaxis_title=None,
                               xaxis={'categoryorder':'total descending'})
                .add_annotation(x=1,y=0.98,text="Smoking status",
                                showarrow=False, xanchor="right",
                                xref="paper",yref="paper",
                                font=dict(color='darkgray',size=24))
            ),
                sizing_mode="stretch_width",
                config={'displayModeBar': False}
            )
        )
    ]

    demographicsDashboard.extend(secondRow)

    return demographicsDashboard

def generateDemographicsDashboard(dfKeyList):

    # logic for cards display to enable dataset comparisons
    # instantiate col component that takes list of dashboards

    mainDashboard = pn.Column()

    for key in dfKeyList:
        mainDashboard.append(singleDatasetView(key))

    return mainDashboard