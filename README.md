This a first-draft of a GSRS Python CLI rest client application.

  python3 bin/gsrspyclient.py --help

The main goals of this application project are to:

1) maintain a basic scaffold where core configuration, logging, and basic CRUD procedures are established.

2) create a mechanism whereby users can create quick plugins to automate data loading and update tasks.

3) encourage convenient logging of all crud operations to track successes and failures at a glance.

The configuration scheme allows you to set up and name various hosts

Plugins are added to the plugins folder.

For now they are registered in bin/gsrspycli.py. Later, they will be registered in the configuration file.

Plugins will hit the GSRS rest api to accomplish some task, such as adding or updating a batch of substances.

The CLI app uses the @click library in a way that each plugin can add commands to the CLI dispatcher(menu).

Two Demo plugins can currently be run like so:

  cat temp.txt | python3 bin/gsrspyclient.py substancesexist

  cat temp.txt | python3 bin/gsrspyclient.py addsubstanceconcepts
