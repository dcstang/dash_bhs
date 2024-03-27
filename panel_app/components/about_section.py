import panel as pn

aboutSection = """
*This is a submission for the Ploomber Cloud <> Panel Hackaton.*    

## Visualisation app for the Biological Health Score project
This is part of an ongoing health research work that is undertaken by the Department of Epidemiology and Biostatistics at Imperial College, London UK.

Currently, the upstream analysis pipeline is already using `Ploomber`. This lives in [another repository](https://github.com/dcstang/tromso-delta-bhs). The study population from the UK Biobank Project is analysed via various population selection criteria and regression models.   
The main target users of this app is scientists within my laboratory and adjacent colaborating organizations.

## Technical details of this webapp
I am deploying some of the scientific results as a webapp, in hopes that more scientists can engage in the research.  
There is often a criticism that others can't get to touch have a feel of the data to provide better and detailed input.  
Initially, this was built as a `dash` application, but migration to `Panel` was quite seamless.

The main advantage is close intergration with other libraries in the PyData space and other scientific toolkits.  
Examples that I have used several other libraries in combination with Panel, including:
* matplotlib
* tableOne
* plotly
* numpy

The open-source code of this app is [available on Github](https://github.com/dcstang/dash_bhs). I have structured the code base via separate components for each 'tab'.  
As best as I could, I tried to make this app responsive. It's a bit tricky, the ability to use a global CSS with tailwindcss would give a bit more flexibility in this regard.  

Ploomber Cloud has also sped up the deployment process with an automated Docker building process. I can deploy easily in a few lines of commands via the `ploomber-cloud CLI`.

## Biological Health Score?
This is a way of quantifying how `healthy` individuals are in relation to the overall population. Eventually we plan to use this score for predictive tasks relating to cancer and cardiovascular disease.  
A large aspect of computing this score depends on setting thresholds / cutoff levels of who are at risk.  
I won't get too much into it but if you are interested, there is a [scientific paper published](https://pubmed.ncbi.nlm.nih.gov/33437953/) on it.


"""

aboutSectionPane = pn.pane.Markdown(aboutSection)