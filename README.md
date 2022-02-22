This a first-draft of a GSRS Python CLI rest client application. 

  python3 bin/gsrspyclient.py --help 
 
The two main goals of this application project are to:

1) maintain a basic scaffold where core configuration, logging, and basic CRUD procedures are exablished.

2) create a mechanism whereby users can create quick plugins to automate data loading and update tasks.

3) Encourage convenient logging of all crud operations to track sucesses and failures at a glance. 

The configuration scheme allows you to set up and name various hosts 

Plugins are added to to the plugins folder. 

For now they are registered in bin/gsrspycli.py 

Plugins will hit the GSRS rest api to accomplish some task such as adding or updating a batch of substances. 

Plugins also include @click annotations so that procedures can be added automatically to a @click dispatcher 

Two Demo plugins can currently be run like so: 

  cat temp.txt | python3 bin/gsrspyclient.py substancesexist
  
  cat temp.txt | python3 bin/gsrspyclient.py addsubstanceconcepts

