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

_Authors: Sverre Brok, Lennard Froma and Jeroen van Gelder_

## Introduction
![Ticket to Ride board, source:(https://www.lotana.be/blog/ticket-to-ride-europe-anniversary-edition)](Figures/backgroundStartpage.jpg)

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
Consider an agent's turn given the simplifications mentioned above. This agent considers three options, in this order:
* Place trains on a connection between two cities to contribute to their routes if they have the right number of train cards
* Place trains on a connection between two cities to block another agent if they have the right number of train cards
* draw train cards (either from the visible or not visible cards);

In case an agent chooses to place trains on a connection between two cities, it can only claim a connection when
it is part of its version of the shortest route for that route card or when it purposefully blocks another agent on its 
shortest route. By purposefully blocking an opponent, we mean that it must know the card of the agent, and it claims a 
connection on the shortest route of this opponent. If agents cannot claim a connection, they will draw train cards based
the general card drawing strategy, which will be expanded upon later.

#### Claiming a connection
As mentioned, an agent is only allowed to claim a connection that progresses it further on one of its own route cards,
or when it blocks another agent. A connection can only be claimed when the agent has enough train cards in the colour
corresponding to the colour of the connection. If a connection has a gray colour, the agent can choose which colour
train cards it uses, so long as all train cards are of the same colour. If the agent's hand does not suffice for claiming
a connection, it can choose to use joker cards to reach the required number of cards.

When the connection is claimed, the train cards played by the agent are removed from its hand and added to a discard stack.
This discard stack builds up with all played cards until the closed deck is empty. Then, the cards on the discard stack
are shuffled and used as the new deck. The claiming of a connection will also influence on the shortest route for an agent
for various route cards, hence all shortest routes are recalculated for all agents.

#### Shortest route
Agents will always claim connections on the shortest path between the cities on the route cards. We use Uniform Cost 
Search (UCS) to find the shortest route between two cities on a route card. Calculating the shortest route only uses the
information given by the board, which is available to all agents. Individual agents' hands are not considered as it will 
add unwanted uncertainty.

The number of trains that are needed to claim a connection is regarded as the cost of an edge. If an agent is already
owner of a connection in a possible shortest route, the cost of that edge will be zero for the owner. As two options
for claiming a connection may be equally optimal, we will perform a random choice. Since all agents are aware of the optimal
route for each other, this random choice will not influence the general knowledge about the state of the game.

#### Card drawing strategy
When drawing cards, an agent can choose to draw two coloured train cards from the closed deck. Alternatively, the agent 
can opt to draw a card from one of the five opened coloured train cards. After drawing an open card, the agents can again
choose to draw their second card from either the open or the closed train cards. However, if an agent takes a joker from 
the open cards, it cannot take a second card. Likewise, the second drawn card may never be a joker from the open train 
cards. 

Before deciding from which deck (open or closed) the agent will draw a train card, it will determine desired cards 
based on the routes it has to complete. For all routes, the agent checks how many train cards are needed to claim a 
connection on this route. Then, the agent checks the open deck and if there is a train card in the open deck which is 
also in the desired train cards, the agent will draw the card. Then, from the closed deck, another card is placed in the
open deck. The agent will repeat this process with a constraint that it is not allowed to select the joker card.

It should be noted that if a joker card is in the open deck and the agent has not yet drawn a card this turn, it will
always take this card. This means it ignores any other desired cards, as the joker card can fill in for this.

#### Obtaining knowledge 
As the strategic element of an agent's actions comes from its knowledge, we must consider various ways of expanding this
knowledge. The first and most straightforward method is when an agent looks at its cards after they have been
distributed. This will give the agent knowledge of its own cards. 

However, knowledge of ones own cards is not enough in most cases, thus agents must also be able to gather knowledge of
other route cards of other agents. When an agent finishes a route card, it will announce which route card it completed.
The public announcement of this card results in a smaller Kripke model as some worlds are now no longer possible.

By claiming a connection, an agent can give away which route card it has. As all agents know all cards and share the set of 
shortest routes, a connection belonging to only one route card can give away which card the agent is working on. (TODO EXAMPLE)
This knowledge can be used to block an agent. 

If an agent cannot claim a connection for one of its own route cards, it will explore the possibilities of blocking
another agent based on its knowledge. When blocking, an agent publicly announces that it knows another agent's
route card and then blocks a connection on that route. This gives other agents knowledge as well. This is done because
if an agent would not announce it knows and therefore blocks, other agents would not know if this agent claims a connection
for its route or for blocking. Then we would end up in a situation where agents will only gather knowledge from the
public announcements upon completion of route cards by other agents. Such knowledge would simply be too late to be useful,
causing agents to never block.

#### End-game
There are three different ways in which the game is ended. The first option is when one of the agent has two or less trains
left after claiming a connection. If this happens, all other agents are allowed to make one more move before the final
points are added up. The second option is when one of the agents completes all of its route cards. In this situation, 
the game is immediately finished. The third option is where the agents are no longer able to make moves. This is identified
when the deck of cards is empty. If this occurs, the game immediately terminates as well.

After ending the game, the final scores are determined. As mentioned before, claimed connections and completed route
cards yield agents points, whereas an incomplete route card gives penalty points, deducting the cards value from the
agent's score. Finally, based on the end scores, the winner of the game is announced. 

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
* $$S = \{(s_1,s_2,\dots,s_n) \, \vert \, s_i \text{ is the agent that owns the } i \text{-th card}\}l$$ is the set of 
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


## Example
In this section, we will go over an example of a complete game. We will highlight interesting turns for both actions by
the agents, and for the Kripke model.

<p float="middle">
  <img src="Figures/Example/1.%20init%20board%20crop.png" width="49%" />
  <img src="Figures/Example/1.%20init%20model%20crop.png" width="49%" /> 
</p>

![initial board](Figures/Example/1.%20init%20board%20crop.png)

## Findings
...
