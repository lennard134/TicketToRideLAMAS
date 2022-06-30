<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.css" integrity="sha384-yFRtMMDnQtDRO8rLpMIKrtPCD5jdktao2TV19YiZYWMDkUR5GQZR/NOVTdquEx1j" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.min.js" integrity="sha384-9Nhn55MVVN0/4OFx7EE5kpFBPsEMZxKTCnA+4fqDmg12eCTqGi6+BB2LjY8brQxJ" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous" onload="renderMathInElement(document.body);"></script>
<style>
.katex-display > .katex {
  display: inline-block;
  white-space: nowrap;
  max-width: 100%;
  overflow-x: scroll;
  text-align: initial;
}
.katex {
  font: normal 1.21em KaTeX_Main, Times New Roman, serif;
  line-height: 1.2;
  white-space: normal;
  text-indent: 0;
}
</style>
</head>

# Modelling Ticket to Ride

## Introduction
![title](Images/backgroundStartpage.jpg)
Ticket to ride is a popular board game designed by Alan R. Moon and published by Days of Wonder. 
The end goal of the game is to build a railway network that yields the highest amount of points. 
There are various versions of the game with different maps of parts of the world. 
On these maps, locations are marked as nodes, representing possible locations for a train station. 
These nodes are connected with railway connections, which can be claimed by a player in their turn. 
The length of the route determines the score a player receives for that part of the railway. 
At the start of the game, each player is given the same number of unique target routes, which yield additional points upon completion.
Failing to complete one or more routes will cause points to be subtracted at the end of the game.

This project's research goal is to model and simulate (a simplification of) Ticket to Ride. The implementation should 
use the acquired knowledge to determine what next action (within the given constraints) an agent should take. The knowledge is
acquired by observing other agents, the board and their own cards.

## The game
The game consists of different cards and objects for which the meaning and function will be explained in this section.
With this game, players should obtain as many points as possible. This is done by finishing route cards that are worth points.
The **route cards** contain two cities between which the agent will have to create a route by placing trains on the connections 
between cities. When the route is finished, the player obtains the number of points as indicated by the route card. 
To place trains on a connection (i.e. claim a connection), a player can draw coloured **train cards**. The connections have different 
colours indicating which colour train card is needed to claim that specific connection. The length of the connection indicates
how many train cards of a particular colour are needed. Furthermore, there are multiple **joker cards** in the game that can 
be used as any of the colours.

In the original game, there are three different kinds of connections. Regular connections between cities, ferry connections,
and tunnel connections. For claiming (i.e. placing trains on a connection) a regular connection, an agent must have several 
train cards of a particular colour. The ferry connection requires regular cards combined with a minimum number of jokers,
indicated as locomotive icons on the connection. The tunnel connection is a bit more complex. For a tunnel of length 2 and
colour green, an agent would have to draw 3 new cards from the deck (this number does not depend on the length of the tunnel connection).
Then, the number of cards that match, in this case, the colour green will have to be added by the agent. 

Another option for a player to use a connection is to build a train station at an already claimed connection. Using this
station it is possible to use another player's connection to complete a route card.

In the original game, a player has four options at each turn. 
1) First, the player can opt to gather coloured cards which allow them to claim certain colour-coded tracks in the next turn. 
2) Another possibility for a player is to claim a specific route. 
This is done by playing the number of cards of the length of the specific route, all with that route's colour. 
Only one route can be claimed during a player's turn. 
3) Additionally, a player can build a train station to utilize a route that has already been claimed by another player. 
4) Lastly, a player can obtain new route cards from a selection of the remaining route cards. 

The game ends when one player has 2 trains left. Then every player does one extra turn and after that, the points 
will be counted. Route cards that are not completed will give a penalty by subtracting the points the route is worth
from the total.

## Simplifications of the game
In the original version of Ticket to Ride Europe, there are 47 cities (nodes), 90 connections (edges), and 46 route
cards and the game can be played by 2 to 5 players, as can be seen ([here](https://towardsdatascience.com/playing-ticket-to-ride-like-a-computer-programmer-2129ac4909d9)).
For our research, this is too complex. Therefore, we simplify the game such that, by default, we have 3 agents playing 
the game. This can be altered by the user upon initialization of the game.

We will play our game with a subset of the original board layout. We choose to play the game using 24 European cities. KEI MOOI PLATJE HIER 
With this default subset, the number of route cards will depend on the number of agents that play the game, and the
number of route cards each agent has. Users can vary from 2 to 5 agents who, by default, have 3 route cards each. 
There are a maximum of 16 route cards available for the subset of the game board used in this simplified implementation.
Each agent must have the same number of route cards, hence there is an implicit limit of e.g. 3 route cards for 5 agents.
Within this implicit limit, the user can vary the number of route cards per agent.

We assume all agents have perfect knowledge about the possible routes in the game, that is, they know which route 
cards are in the game. We also apply the simplification that all route cards are distributed among the agents. This
automatically removes the possibility to use a turn to obtain new route cards.

Additionally, to allow for knowledge to influence agent decisions, we limit the agents to only two
ways to place trains: either claim a section of the railway such that you progress on one of your routes, or such that
you hinder your opponent based on what you know about their route cards. This means that knowledge will directly
influence the strategies of the agents. If an agent cannot claim any routes that are allowed within the limitations of
the two possibilities, they can draw new train cards following the original game rules: two cards (open or closed), or 
one open joker card. Lastly, we initially omit the placement of train stations to simplify the procedure of the game.

It should be noted that real-world agents obtain a degree of knowledge from what colour cards an opponent draws. This
is however a very complex strategy to implement. It would require an agent to take into account all shortest routes with
all colours that are relevant for those routes, and update its knowledge every round in which cards are drawn. Additionally,
agents could draw certain cards to mislead agents that use knowledge about drawn cards. It is also possible that due to 
certain routes being claimed, the shortest route is no longer available, and a certain colour might be drawn to cover a 
specific detour, adding more complexity. For this reason, no such knowledge is used by our agents.

Since agents only have two possible moves when claiming routes, we can encounter a situation where no
agent is allowed to claim a new route as there is no possible route that allows reaching the destination or hinder
opponents. This is a unique situation due to our simplifications and will be a cause for termination of the game when all
three agents encounter this situation successively.

### Design choices in implementation
The code is built up such that all the parameters like the number of route cards or trains for example can be changed easily. 
For simplicity, we now assume that we have three agents that each received three unique route cards at the beginning
of the game. Besides, the agents all receive 45 trains which can be placed on connections.

The code is implemented using Western European cities where the most westerly city is Lisboa and the most easterly is Brindisi.
In total, there are 24 cities in the game, and the agents receive three out of a total of 16 route cards. On the Ticket
to Ride board, there are often double connections between cities which can be utilized if there are more than 3 players.
As we have restricted ourselves to just three players by default, we only use single connections.

#### An agent's turn
Consider now an agent's turn given the simplifications and design choices. This agent considers three options, in this order:
* Place trains on a connection between two cities to contribute to their routes if they have the right number of train cards
* Place trains on a connection between two cities to block another agent if they have the right number of train cards
* draw train cards (either from the visible or not visible cards);

In case an agent chooses to place trains on a connection between two cities, it can only claim a connection when
it is part of the resulting shortest route or when it purposefully blocks another agent on its shortest route.
By purposefully blocking an opponent, we mean that it must know the card of the agent, and it claims a connection on the
shortest route of this opponent. In case an agent chooses to draw train cards, the agent can draw the first card from 
either the (5) visible cards or the closed deck. If the agent does not draw a joker card from the visible cards,
it can pick another card from either the visible cards (but not a joker card) or the closed deck. 007 WAS HERE

#### Card drawing strategy  
An agent can choose to draw two train cards from the closed deck, or draw two train cards from the open deck where the second card
may not be a joker. Before deciding which from which deck (open or closed) the agent will draw a train card, it will determine
desired cards based on the routes it has to complete. For all routes, the agent checks how many train cards are needed to
claim a connection on this route. Then, the agent checks the open deck and if there is a train card in the open deck
which is also in the desired train cards, the agent will draw the card. Then, from the closed deck, another card is placed
in the open deck. The agent will repeat this process with a constraint that it is not allowed to select the joker card.

#### Shortest route
Agents will always claim connections on the shortest path between the cities on the route cards. 
We will use Uniform Cost Search (UCS) to find the shortest route between two cities on a route card. Calculating the
shortest route only uses the information given by the board, which is available to all agents. Individual agents' hands
are not considered as it will add unwanted uncertainty.
Here the number of trains that are needed to claim a connection is the edge costs. As two options
for claiming a connection may be equally optimal, we choose that the agent will claim the connection on the route that is 
worth the most points. If the number of points is equal as well, we will perform a random choice.

#### Obtaining knowledge 
As mainly the knowledge determines the agent's strategy, we will have to define the different ways this knowledge can
be obtained. The first and most straightforward method is when an agent looks at its cards after they have been
distributed. This will give the agent knowledge of its cards. The next way is, when an agent finishes a route card,
it will announce this. The public announcement of this card results in a smaller Kripke model as some worlds are not
possible anymore.

By claiming a connection, an agent can give away which route card it has. As all agents know all cards and share the set of 
shortest routes, a connection belonging to only one route card can give away which card the agent is working on. (EXAMPLE)
This knowledge can be used to block an agent. If an agent cannot claim a connection itself, it explores the possibilities
based on its knowledge to block another agent. When blocking, an agent publicly announces that it knows another agent's
route card and then blocks a connection on that route. This gives other agents knowledge as well. This is done because
if an agent would not announce it knows and therefore blocks, other agents would not know if this agent claims a connection
for its route or for blocking. In this situation, only a public announcement would yield knowledge and an agent would never
block as we only want an agent to block if it knows who is the owner of the route card.

#### Drawing cards
An agent can choose to draw a train card from the open deck based on what train cards it needs for the connections on
the route cards. If there are multiple routes for which the agent needs a train card from the open deck, it will select the 
train card that will add to the route card worth the most points. 

#### End-game
The game can be ended in three ways:
* When an agent has claimed a connection, and it has only two trains left, every agent has only one turn left;
* When an agent accomplished all route cards;
* When all agents in subsequent turns cannot draw any cards anymore, neither from the open nor closed deck.

## Model

Let us define the following sets:
* $$A=\{a_1,a_2,\dots,a_m\}$$ be the set of $$m$$ agents;
* $$D=\{d_1,d_2,\dots,d_n\}$$ be the set of $$n$$ destination cards in the game;
* $$\mathbf{P}=\{p_{ij} \, \vert \, 1 \leq i \leq m, 1 \leq j \leq n\}$$ be the set of predicates where $$p_{ij}$$ 
  denotes agent $$i$$ has destination card $$j$$.

Here we take $$\frac{n}{m} \in \mathbb{N}$$, so the cards can be evenly distributed among the agents. 

Now, let $$M=\langle S, \pi, R_1, \dots, R_m \rangle$$ be the Kripke model where
* $$S = \{(s_1,s_2,\dots,s_n) \, \vert \, s_i \text{ is the agent that owns the } i \text{-th card}\}$$ is the set of 
possible states;
* $$\pi : S \rightarrow \mathbf{P} \rightarrow \{t, f\}$$;
* $$R_i = \{\langle \mathbf{s}, \mathbf{t} \rangle \, \vert \, s_j = t_j \text{ for all } j \in \{1,\dots,n\} \text{ where } 
s_j = a_i\} \text{ for } 1 \leq i \leq m$$.

The set of states, $$S$$ is simply all combinations of route card distributions over the agents, where each agent has the
same amount of route cards. The valuation function $$\pi$$ assigns for each state a truth value to each predicate 
$$p_{ij} \in \mathbf{P}$$. The set of relations for agent $$i$$ is all relations between two states in which agent $$i$$
has the same route cards.

At the start of the game, when the cards are evenly distributed among the agents, but the agents have not looked at their 
route cards, each agent knows that each agent has $$\frac{n}{m}$$ route cards. Moreover, each agent
knows that only one of the agents has a specific train card, that is, for all 
$$j \in \{1,\dots,n\}$$ and $$i \in \{1,\dots,m\}$$

$$M \models K_i (p_{1j} \lor \dots \lor p_{mj}),$$

and for all $$i \in \{1,\dots,m\}$$, for all $$l \in \{1,\dots,m\}\backslash\{i\}$$

$$M \models K_i p_{ij} \rightarrow K_i \lnot p_{lj}.$$

After the agents have looked at their route cards, the agents know which card they have, so for all 
$$i \in \{1,\dots,m\}$$ and all $$j \in \{1,\dots,n\}$$

$$M \models p_{ij} \rightarrow K_i p_{ij}.$$

### An agent's turn

Consider now an agent's turn given the simplifications and design choices, say agent $$i$$, $$i\in\{1,\dots,m\}$$.
Sverre, do your logic magic :sunglasses: 

### Public announcements
If an agent completes a route from its route cards, this completion is (instantly) publicly announced to all agents. 
This means that upon route completion:

$$[p_{ij}] p_{ij}$$

With this, the model changes such that all states in which $$\neg p_{ij}$$ holds, can be removed for simplification. 

Another 'announcement' that modifies the model is that of claiming routes. When an agent claims a route, it gives
information to the other agents. As earlier mentioned, an agent may only claim a route, when it is part of the shortest 
route of one of its route cards, or when it purposefully blocks an opponent (see explanation above). Hence, claiming
routes gives information to other agents as it must be one of the two.

### Map
Consider the problem as a network $$\mathcal{G} = (\mathcal{N}, \mathcal{A})$$, where each arc (connection) 
$$a \in \mathcal{A}$$ has weight $$w_a$$, which is the number of trains that is needed to claim the connection.
The nodes correspond to the cities.



## Findings
...
