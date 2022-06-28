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
Ticket to ride is a popular board game designed by Alan R. Moon and published by Days of Wonder. 
The end goal of the game is to build a railway network that yields the highest amount of points. 
There are various versions of the game with different maps of parts of the world. 
On these maps, locations are marked as nodes, representing possible locations for a train station. 
These nodes are connected with railway connections, which can be claimed by a player in their turn. 
The length of the route determines the score a player receives for that part of railway. 
At the start of the game, each player is given a number of target routes, which yield additional points upon completion.

At each turn, a player has four options. 
First, the player can opt to gather colored cards which allow them to claim certain color-coded tracks in a next turn. 
Another possibility for a player is to claim a specific route. 
This is done by playing the number of cards of the length of the specific route, all with that route's color. 
Only one route can be claimed during a player's turn. 
Additionally, a player can build a train station to utilize a route that has already been claimed by another player. 
Lastly, a player has the possibility to obtain new route cards.

The route cards contain two cities between which the agent will have to create a route by placing trains on the connections 
between cities. When the route is finished, the player obtains the number of points as indicated by the route card. 
To place trains on a connection (i.e. claim a connection), a player can draw train cards. The connections have different 
colours indicating which colour train card is needed to claim that specific connection. The length of the connection indicates
how many train cards of a particular colour are needed. Furthermore, there are multiple joker cards in the game that can 
be used as any of the colours. Jokers are also necessary for claiming ferry connection (i.e. connections that go over water),
in the ferry connection regular cards can be combined with minimum of required jokers.

## Research goal
The goal of our research is to simulate and model (a simplification of) Ticket to Ride.

## Simplifications of the game
In the original version of Ticket to Ride Europe there are 47 cities (nodes), 90 connections (edges) and 46 route
cards, and the game can be played by 2 to 5 players ([here](https://towardsdatascience.com/playing-ticket-to-ride-like-a-computer-programmer-2129ac4909d9)).
For our research, this is too complex. Therefore, we simplify the game such that we have 3 agents playing 
the game.

We will begin our implementation with a subset of the original board layout. We choose the play the game using different 
western European cities. The number of route cards will be influenced by the subset of the nodes that we take, 
and we assume all agents have perfect knowledge about the possible routes in the game, that is, they know which route 
cards are in the game. We also apply the simplification that all route cards are distributed among the agents. This
automatically removes the possibility to use a turn to obtain new route cards.

Additionally, to allow for knowledge to influence agent decisions, we limit the agents to only two
ways to place trains: either claim a section of railway such that you progress on one of your own routes, or such that
you hinder your opponent based on what you know about their possible routes. This means that knowledge will directly
influence the strategies of the agents. If an agent cannot claim any routes that are allowed within the limitations of
the two possibilities, they can draw new train cards following the original game rules: two cards (open or closed), or 
one open joker card. Lastly, we initially omit the placement of train stations to simplify the procedure of the game.

It should be noted that real world agents obtain a degree of knowledge from what colour cards an opponent draws. This
is however a very complex -- and definitely not foolproof -- strategy to implement. It would require an agent to take into
account all shortest routes with all colours that are relevant for those routes, and update its knowledge every round
in which cards are drawn. Additionally, agents could draw certain cards to mislead agents that use knowledge about
drawn cards. It is also possible that due to certain routes being claimed, the shortest route is no longer available, and
a certain colour might be drawn to cover a specific detour, adding more complexity. For this reason, no such knowledge
is used by our agents.

Due to the fact that agents only have two possible moves when claiming routes, we can encounter a situation where no
agent is allowed to claim a new route as there is no possible route that allows reaching the destination or hinder
opponents. This is a unique situation due to our simplifications and will be a cause for termination of the game when all
three agents encounter this situation successively.

### Resources
We still have to think about this, but we have to specify the following:
* The number of trains each agent has to claim routes;
* The exact number of routes.


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
knows that only one of agents has a specific train card, that is, for all 
$$j \in \{1,\dots,n\}$$ and $$i \in \{1,\dots,m\}$$

$$M \models K_i (p_{1j} \lor \dots \lor p_{mj}),$$

and for all $$i \in \{1,\dots,m\}$$, for all $$l \in \{1,\dots,m\}\backslash\{i\}$$

$$M \models K_i p_{ij} \rightarrow K_i \lnot p_{lj}.$$

After the agents have looked at their route cards, the agents know which card they have, so for all 
$$i \in \{1,\dots,m\}$$ and all $$j \in \{1,\dots,n\}$$

$$M \models p_{ij} \rightarrow K_i p_{ij}.$$

### An agent's turn

Consider now an agent's turn, say agent $$i$$, $$i\in\{1,\dots,m\}$$.
This agent considers three options, in this order:
* Place trains on a connection between two cities to contribute to their own routes if they have the right number of train cards
* Place trains on a connection between two cities to block another agent if they have the right number of train cards
* draw train cards (either from the visible or not visible cards);

In case an agent chooses to place trains on a connection between two cities, it can only claim a connection when
it is part of the resulting shortest route or when it purposefully blocks another agent on its shortest route.
With purposefully blocking an opponent, we mean that it must know the card of the agent, and it claims a connection on the
shortest route of this opponent.
In case an agent chooses to draw train cards, the agent can draw the first card from either the (5) visible cards or the 
closed deck.
If the agent does not draw a joker card from the visible cards, it can pick another card from either the 
visible cards (but not a joker card) or the closed deck. 

Lastly, when an agent cannot claim any connection anymore, since, for example, there is no possible route for its 
route card anymore, and it cannot purposefully block another agent. This will be explained later and is found to be necessary as otherwise the game might continue infinitely,
as the agents might always pick train cards. When, after another agent's turn the agent can claim a connection again,
this will be 'announced' too.

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
...


### Shortest route
We will use the A* path planner to find the shortest route between two cities. Here the number of trains that is 
needed to claim a connection are the edge costs.


### End-game
The game can be ended in three ways:
* When an agent has claimed a connection, and it has left only two trains, every agent has only one turn left;
* When an agent accomplished all route cards;
* When all agents 'announced' in subsequent turns that they cannot claim any routes anymore.

## Findings
...