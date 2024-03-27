import panel as pn

# setup sidebar
sidebarInfo = pn.pane.Markdown(
"""
## ⚙️ Data settings
Explore variations of the results, either the original dataset or a imputed version  
""")

datasetType = pn.widgets.CheckBoxGroup(
    name="Dataset type", 
    value=["complete"],                                   
    options={"Original":"complete", "Imputed":"impute"}, 
    width=200)

sideBarWidgetsList = [sidebarInfo, datasetType]