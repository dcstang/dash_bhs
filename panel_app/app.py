import panel as pn
from components.sidebar_widgets import sideBarWidgetsList, datasetType
from components.demographics_dashboard import generateDemographicsDashboard
from components.demographics_table import generateDemographicsComponent
from components.biomarkers_quartiles import generateBiomarkersComponent
from components.about_section import aboutSectionPane

pn.config.raw_css = ["""
    img.app-logo { height: 20px !important; }
"""]

template = pn.template.MaterialTemplate(
    logo="assets/white_logo.png",
    favicon="assets/i_favicon.png",
    title="    🔬 Biological Health Score | Scientific Dashboard",
    sidebar=sideBarWidgetsList,
    collapsed_sidebar=True,
    sidebar_width=280,
    header_background="#0000CD"
)

# add reactivity between widget and data 
# pass output from datasetType (checkboxgroup component) as list
demographicsDashboard = pn.bind(generateDemographicsDashboard, dfKeyList=datasetType)
demographicsTable = pn.bind(generateDemographicsComponent, dfKeyList=datasetType)
biomarkersCards = pn.bind(generateBiomarkersComponent, dfKeyList=datasetType)

mainSection = pn.Tabs(
    ("🧑‍🤝‍🧑Population Dashboard", 
        demographicsDashboard),
    ("🧑‍🤝‍🧑Population Demographics (Tabular)", 
        demographicsTable),
    ("📈 Biomarkers", 
        biomarkersCards),
    ("❔About",
        aboutSectionPane),
    dynamic=True)

template.main.append(mainSection)
template.servable()
