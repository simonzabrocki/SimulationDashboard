![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Simulation Dashboard
Simulation Dashboard is a web application for index vizualisation and policy simulation. It is deployed at https://gggi-simtool-demo.herokuapp.com/

# Purpose
The goal of this application is to display the index and simulation results. The app is divided into three components. The first is the green growth index which includes scores and vizualistations for all countries. The second is the simulation tool which allows to interact with models and simulate policies. The last is the evidence librabry which includes all the models, data and codes used in the analysis. 

# Installation
-------------------
```
$ git clone https://github.com/simonzabrocki/SimulationDashboard.git

$ python index.py
```

# Deployement
-------------------
The app can be deployed on Heroku via:
```
$ git push heroku main
```


# Project Structrue 

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


# Roadmap

Code: 
- Fetch simulation data and model from database
- Improves modularity by using a sub repo for ggmodel_dev.


Features:
- Improve country comparator
- Add data explorer for simulation models (like the one for the index)

# Authors
---------------
S. Zabrocki

