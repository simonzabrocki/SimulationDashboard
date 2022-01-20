![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Simulation Dashboard
Simulation Dashboard is a web application for index vizualisation and policy simulation. It is deployed at https://gggi-simtool-demo.herokuapp.com/

## Purpose
The goal of this application is to display the index and simulation results. The app is divided into three components. The first is the green growth index which includes scores and vizualistations for all countries. The second is the simulation tool which allows to interact with models and simulate policies. The last is the evidence librabry which includes all the models, data and codes used in the analysis. 

## Installation
-------------------
```
$ git clone https://github.com/simonzabrocki/SimulationDashboard.git

$ python index.py
```

## Deployment
-------------------
The app can be deployed on Heroku via:

```
$ git push heroku main
```

Go to https://devcenter.heroku.com/articles/git for more details


## Project Structure 

    ├── data           
    │   
    │   └── indicators        <- Green Growth index indicator data
    │   └── sim               <- Simulation data
    │
    ├── assets                <- css and background
    |
    ├── ggmodel_dev           <- Graphmodel computation package
    |
    ├── outputs               <- Ressources downloadables in the interface
    |
    ├── pages                 <- Source code of individual pages

### Green Growth Index

From green growth index menu, we can access the three version of the index. (see version paragraph for details)
- 2020 index
- 2021 index
- Green-Blue Growth index 

For the most part, all pages in the SimulationDashboard are self contained. Each page has its dedicated python script. Common elements and functions are defined in utils.py or data_utils.py at the root of the project. Callbacks, graphs and html elements are defined with the page python file.

Due to its complexity, the simulation tool tab is defined using multiple python files.

#### Global overview

Global overview displays the world map of the Index values. A sortable table allows to look for individual scores for index and dimensions. 

#### Regional Outlook

Regional outlook page displays index results by regions (or continent)

#### Country profile

Country profile displays statistics on the Index results for a single country.

#### Country Comparison

Country Comparison allows comparing results for two countries at a time.

### Simulation Tool

Simulation tools displays results by country of choice 

### Evidence Library

Evidence library includes all the models, data, codes, and downloads used in the analysis. 

#### Models

Models allows exploring all models available in ggmodel.

#### Data

This tab is a data explorer. From there you can select individual indicators, understand their definitions and visualize the values for particular countries.

#### Codes

All codes should be clearly available from the app. For this purpose this page links to the three relevant github repositories:

- Green Growth Index: A python program to download, process and perform all the step to compute the green growth index.
- Graph Models: A python framework to compute and visualize GGGI models using computational graphs.
- Interface: A Dash web application to vizualize the index and simulate green growth policies

#### Downloads

Data and results are freely available to download in this section. The results for the index and simulation tool are split into 4 categories:

- Index: All index results.
- Indicators: All raw Indicators.
- Definitions: All indicators definitions.
- Models: All models specifications.

### Guidelines for plots and graphs

The colors of dimensions are defined in the table below. These colors must be used only for this purpose.  

|  | Color code |
| --- | --- |
| Main Color | #14ac9c |
| ESRU       | #8fd1e7 |
| NCP        | #f7be49 |
| GEO        | #9dcc93 |
| SI         | #d9b5c9 |


The order of dimensions in legend and bar plot is  1. ESRU, 2. NCP, 3.GEO, 4. SI for dimensions.

For categories the order is the following: 
1. ESRU: EE, EW, SL, ME
2. NCP: EQ, GE, BE, CV
3. GEO: GV, GT, GJ, GN
4. SI: AB, GB, SE, SP


## Versions

Because the index and simulation tool is fine tuned for each use case, the app is split into three versions each with its own branch:

1. Main: Includes 2020 green growth index and simulation tool
2. blueindex: Includes green-blue growth index only
3. index2021: Includes 2021 index green growth index only

### main

The main branch contain the core application. All graphs, callbacks and features should be provided on this branch. From this version, the other two versions should be accessible.

### blueindex

blueindex is simply a copy of the main branch with some theme adaptation (colors and texts) and custom data. The simulation tool is removed from this page

### index2021

index2021 is simply a copy of the main branch with updated data for the index. The simulation tool is removed from this page. 
 

# Roadmap

Code: 
- Fetch simulation data and model from external database
- Improve modularity by using a sub repo for ggmodel_dev.
- Improve simulation page to add new models more easily

Features:
- Improve country comparator
- Improve downloadable pdf report
- Add data explorer for simulation models (like the one for the index)

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# Contact
---------------
S. Zabrocki - simon.zabrocki@gggi.org

I. Nzimenyera - innocentnzime42@gmail.com

