# Visualisation app for the Biological Health Score project 

This is part of an ongoing health research work that is undertaken by the Department of Epidemiology and Biostatistics at Imperial College, London UK.

Currently, the upstream analysis pipeline is already using `Ploomber`. This lives in [another repository](https://github.com/dcstang/tromso-delta-bhs). The study population from the UK Biobank Project is analysed via various population selection criteria and regression models. 

This is an outshoot from the project for the Ploomber<>Panel Hackaton. I aim to democratise access and understanding of the `health scores` that are being developed within the group, firstly to other scientists in the department -- for further colaboration and ideation. Eventually, I think this could be a useful tool for (rigorous) scientific peer review before actual use in the clinical setting.

As a bit of background, I was initially working on visualisations in Dash/Plotly. For the purpose of the hackaton, I will rescope the existing dash app to purely focus on one area of the project and rewriting it into the Panel framework. 

This project will be looking at the data as its original state and comparing it with an imputed version. We used a machine learning technique called `K-nearest neighbours` to infer missing biomarkers. So, it is useful to check if the study population has increased and if any demographic characteristics have been skewed due to this technique.

Visit the hackaton app here > [link to app on Ploomber cloud](https://plain-breeze-4374.ploomberapp.io)

## Features 
* interactivity and ability to compare two patient populations side-by-side
* responsive web-app to democratize access
* multi-page app with explaination of the project background. Extensibility with other scientific tools in the future

## Progress logs
====================
* 18th March : Ploomber cloud first build and successfully launched dash app
* 22nd March : Panel tutorials and rewrite
* 26th March : Redesign and rescope app, initial panel deployment
* 27th March : Base app pages and logic done, to fully build out viz section
* 29th March : add visualisation section of app
*  3rd April : update to Panel 1.4.0 API, add responsiveness, output SVG graphics, logo sizing tweak, update docs and about section of app with some details on K-nearest neighbours algorithm, add screenshots to github

## Preview screenshots
![dashboard main view](/panel_screenshots/screenshot_1.png "Main dashboard page")
![biomarkers view](/panel_screenshots/screenshot_2.png "Biomarkers section")