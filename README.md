# Playing 'Ticket To Ride' Using Knowledge

This game is based on the Ticket To Ride game, where we used the Europe version.

## Setup and Running
Our code was tested with `python3` on Windows.
After cloning the repository, you could make a new python environment (python version 3.9) and ensure it is activated.
Navigate in your terminal to the correct folder where the src folder and the data folder is placed.

## Requirements
Install the required packages in the **requirements.txt** file using the command line:

    pip install -r requirements.txt

This file includes all packages needed to run the code.


## Command Line Arguments
Code for running the Ticket To Ride interface is
        
    python ./src/main.py

There are various optional command line arguments, which can be shown using:

    python ./src/main.py -h

This will show:

    Ticket to Ride
    
    optional arguments:
      -h, --help            show this help message and exit
      --num_agents NUM_AGENTS, -n NUM_AGENTS
                            The number of agents. Options={1,2,...,5}.
      --num_route_cards NUM_ROUTE_CARDS, -m NUM_ROUTE_CARDS
                            The number of route cards per agent.


For example, to run the interface with three agents and two route cards, one can run the following:

    python ./src/main.py -n=3 -m=2


## Data
Data for the cities, route cards and train connections can be found in the data folder.
The **cities.txt** file can be expanded by adding more cities with coordinates from the Ticket to Ride version Europe.

## Additional (Important) Information
We advise you to set your settings of screen scaling to 100%.
In Windows, one can do this by navigating to _settings_, click _System_, and then under _Display_ and _Scale and layout_ change the size of text, apps, and other items to 100%.
This is because otherwise the screen might not capture the whole Ticket to Ride interface.

Default values for number of agents is three and for number of route cards is three.
We limit the number of agents from 1 to 5 (as is done in the actual game), and the total number of route cards is limited (implicitly) to 16.
The number of worlds and relations is exploding in the number of agents and route cards, so we warn you not to choose a high number of route cards, because it will be very, very slow with initializing the Kripke model.



## Copyright
Scripts (unless otherwise stated in the files) created by:

Sverre Brok (s3200124),
Jeroen van Gelder (s3813053),
Lennard Froma (s2676699)