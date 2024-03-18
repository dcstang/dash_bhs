import dash
from dash import Dash, html, dcc, callback,\
    Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from functions.variable_store import *
from functions.load_datasets import *

app = Dash(
    __name__,
    external_scripts=["https://cdn.tailwindcss.com"],
     meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    use_pages=True,
    title="BHS Explore",
    suppress_callback_exceptions=True
)

# app.scripts.config.serve_locally = False
navIconList=[
     "bi:house-door-fill",
     "bi:search",
     "bi:bar-chart",
     "bi:bar-chart",
     "bi:bar-chart"]

app.layout = html.Div([

    dcc.Location(id="url"),
    html.Div(children=[
        html.Div('Biological Health Score',
            className="inline text-white font-extrabold text-xl p-4")],
        className='flex bg-blue-900 border-b mx-2 mt-2 rounded-lg justify-between'),

    html.Div(children=
            [dmc.NavLink(
                label=f"{page['name']}", href=page["relative_path"],
                variant="subtle", id=page["name"], 
                childrenOffset=20, 
                icon=DashIconify(icon=navIconList[idx]),
                className="text-center justify-items-center")
                for idx, page in enumerate(dash.page_registry.values())]
        , id="bhsTablist", className="grid grid-flow-row auto-rows-max md:flex flex-row mx-2"),

    html.Div(
        children=[
            html.H2("Select dataset :"),
            dcc.RadioItems(
                list(filepathDict.keys()), list(filepathDict.keys())[0],
                inputClassName='ml-6 mr-2', id="selectBhsType_radioItems")
            ],
        id="upperOptionsDiv",    
        className='text-left max-w-xl m-4 px-12'),  

    dmc.LoadingOverlay(dash.page_container, 
                       overlayOpacity=0,
                       overlayBlur=2,
                       className="min-h-20"),

])  

@callback(
    [Output(page["name"], "active") for page in dash.page_registry.values()],
    [Input("url", "pathname")])
def handle_navbar(pathname):
    # check which and return list of active
        activeList = []
        for page in dash.page_registry.values():
            if page['relative_path'] == pathname:
                activeList.append(True)
            else:
                activeList.append(False)
        return activeList

@callback(
     Output("upperOptionsDiv", "style"),
     [Input("url", "pathname")],
     prevent_initial_call=True
)
def hide_dataset_choices(pathname):
     if pathname == "/":
          return {'display':'none'}

# clientside_callback(
#     """
#     function checkActive(pathname) {
#         console.log("Check running")
#         const activeList = [];
#         for (const page of Object.values(dash.page_registry)) {
#             if (page.relative_path === pathname) {
#                 activeList.push(true);
#             } else {
#                 activeList.push(false);
#             }
#         }
#         console.log(activeList);
#         return activeList;
#     }
#     """,    
#     [Output(page["name"], "active") for page in dash.page_registry.values()],
#     [Input("url", "pathname")]
# )