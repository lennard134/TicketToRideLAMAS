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
![Ticket to Ride board overview \label{intro}](Figures/backgroundStartpage.jpg)
Test: figure is here: \ref{intro}.
Ticket to ride is a popular board game designed by Alan R. Moon and published by Days of Wonder. 
The end goal of the game is to build a railway network that yields the highest amount of points. 
There are various versions of the game with different maps of parts of the world. 
On these maps, locations are marked as nodes, representing possible locations for a train station. 
These nodes are connected with railway connections, which can be claimed by a player in their turn. 
The length of the route determines the score a player receives for that part of the railway. 
At the start of the game, each player is given the same number of unique target routes, which yield additional points upon completion.
Failing to complete one or more routes will cause points to be subtracted at the end of the game.

This project's research goal is simulate and model knowledge within (a simplification of) Ticket to Ride. The implementation should 
use the acquired knowledge to determine what next action (within some given constraints) a player should take. The knowledge is
acquired by observing other players, the board and their own cards.

## The original game Ticket to Ride
The game consists of different cards and objects for which the meaning and function will be explained in this section.
With this game, players should obtain as many points as possible. This is done by finishing route cards that are worth points.
Each **route card** contains two cities between which the player will have to create a route. A route is constructed by claiming connections 
by placing enough trains. A route card is completed when there is a route of adjoining connections owned by the player between
the two cities on the route card. When the route is finished, the player obtains the number of points as indicated by the route card. 
To place trains on a connection (i.e. claim a connection), a player can draw coloured **train cards**. The connections have different 
colours indicating which coloured train card is needed to claim that specific connection. The length of the connection indicates
how many train cards of a particular colour are needed. Furthermore, there are multiple **joker cards** in the game that can 
be used as any of the colours.


In the original game, there are three different kinds of connections. Regular connections between cities, ferry connections,
and tunnel connections. For claiming a regular connection, a player must have several train cards of a particular colour. 
The number of train cards that are needed to claim a connection corresponds to the length of the connection.
The ferry connection requires regular train cards combined with a minimum number of jokers,
indicated as locomotive icons on the connection. The tunnel connection is a bit more complex. For example, for a tunnel of length two and
colour green, a player would have to draw three new cards from the deck (this number does not depend on the length of the tunnel connection).
Then, the number of cards that match, in this case, the colour green will have to be added by the player. 

Another option for a player to complete a route is to place a train station on a city. 
This train station can then be used at the end of the game to use a connection owned by another player that adjoins the corresponding city.

In the original game, a player has four options at each turn. 
1) First, the player can opt to gather train cards which allow them to a claim connection in a consequent turn.
Train cards can be drawn from a deck. The deck consists of an open pile (5 train cards that are visible to everyone) and a closed pile.
A player may draw 2 cards from the open or closed pile (or a combination thereof), or only one joker card from the open pile.
2) Another possibility for a player is to claim a specific connection.
This is done by playing the number of train cards of the length of the specific connection, all with that connection's colour. 
Only one route can be claimed during a player's turn.
3) Additionally, a player can build a train station to utilize a route that has already been claimed by another player. 
4) Lastly, a player can obtain new route cards from a selection of the remaining route cards. 

The game ends when one player has 2 trains left. Then every player does one extra turn and after that, the points 
will be counted. Route cards that are not completed will give a penalty by subtracting the points the route is worth
from the total.

## Simplifications of the game

In order for us to achieve a feasible implementation of Ticket to Ride with knowledge, some simplifications had to be
made. These simplifications both address the scale of the game, and the removal of possible uncertainties when considering
knowledge of the agents.

Firstly, the number of cities is reduced from the original 47 cities to a more reasonable 24. With this reduction of
cities, this automatically reduces the number of connections as well. As mentioned, the regular game has both normal,
ferry and tunnel connections. These connections can also be doubled between two cities. In our version, only the normal
and ferry connections are considered. The removal of double connections and tunnel connections yields TODO!! connections
against the usual 90.

<span style="color:red">KEI MOOI PLATJE HIER</span>.

With the reduced map size, we also reduce the number of possible route cards. The original game contains 46 different
route cards, whereas our version only contains 16 different route cards. From this set of 16 route cards, all agents
get assigned an equal number of route cards. Based on the chosen number of route cards per agent and the number of agents,
this results in a subset of the total route card set. This subset is known to all agents, meaning they have perfect
knowledge of the possible route cards in the game. Additionally, agents cannot draw new route cards during the game, as
opposed to the original game where this is allowed.

If an agent chooses the option to claim a route on the board, this is only allowed if it helps their own route, or if it
directly blocks the route of another agent. This simplification is done to increase the available knowledge of all agents. Added
to this is the fact that for each agent and each route card, the shortest route is known based on the state of the board.
This means that if an agent claims a connection, other agents can verify which routes are possible routes of the placing
agent.

Furthermore, if an agent performs a block, it is forced to publicly announce which route it blocks from which agent.
Since blocking is only possible when being 100% certain about the owner of a route card, this public announcement allows
other agents to increase their knowledge as well. Additionally, this requirement for a public announcement allows all
agents to distinguish between a block and a regular claim by an agent. This public announcement might seem odd at first,
but could be compared to a real player taunting its opponent when performing a block.

The last simplification is made by removing the possibility to place train stations. This simplification is partly
made to simplify the coding itself, as there now cannot be multiple owners of a single connection. But this also simplifies
determining the shortest route, reduces computational complexity and keeps the knowledge extracted from the board more
simple.

___

THIS SHOULD PERHAPS BE MENTIONED IN A DISCUSSION
It should be noted that real-world agents might obtain a degree of knowledge from the colour cards that an opponent draws. 
However, it would require an agent to take into account all shortest routes with all colours that are relevant for those routes, 
and update its knowledge every round in which cards are drawn. Additionally,
agents could draw certain cards to mislead agents that use knowledge about drawn cards.
Hence, due to its complexity, we assume that no knowledge is acquired from drawing train cards. 

## Implementation
In this section we will discuss the various element of our implementation of the Ticket to Ride game. We will go over 
the most important sections that determine the workings of the system and the behaviour of the agents.

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
The game can be ended in three ways, the first way is when an agent has only two trains left, every agent can do a last turn
after which the game is ended. The second way is when an agent has finished all route cards, the game ends directly.
The last way to end a game is when all agents in subsequent turns cannot draw any card anymore, neither from the open, nor
from the closed deck. In that case the game ends as well. The winner is determined based on the points scored.
The score is based on the finished route cards which all have their own value. Besides that, an agent receives points 
for individual connections. If an agent did not finish a route card it will receive a penalty by deducting the route 
card's value from its score. 

## Kripke Model
Uitwerken:
  - Claimed connection that gives information -> Common knowledge \[connection of shortest route V ... V ... V ...\]
  - Public announcement after completing route -> Common knowledge
  - Public announcement after block -> Common knowledge after announcement
  
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
