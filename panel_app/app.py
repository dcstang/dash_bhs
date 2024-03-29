import panel as pn
from components.sidebar_widgets import sideBarWidgetsList, datasetType
from components.demographics_table import generateDemographicsComponent
from components.biomarkers_quartiles import generateBiomarkersComponent
from components.about_section import aboutSectionPane

template = pn.template.MaterialTemplate(
    logo="assets/white_logo.png",
    favicon="assets/i_favicon.png",
    title="    🔬 Biological Health Score | Scientific Dashboard",
    sidebar=sideBarWidgetsList,
    collapsed_sidebar=False,
    sidebar_width=280,
    header_background="#0000CD"
)

# add reactivity between widget and data 
# pass output from datasetType (checkboxgroup component) as list
demographicsTable = pn.bind(generateDemographicsComponent, dfKeyList=datasetType)
biomarkersCards = pn.bind(generateBiomarkersComponent, dfKeyList=datasetType)

mainSection = pn.Tabs(
    ("Population Demographics", 
        demographicsTable),
    ("Biomarkers", 
        biomarkersCards),
    ("About",
        aboutSectionPane),
    dynamic=True)

template.main.append(mainSection)
template.servable()
