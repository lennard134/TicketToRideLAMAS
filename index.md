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

# Ticket to Ride

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

## Research goal
The goal of our research is to simulate and model (a simplification of) Ticket to Ride.

## Simplifications
In the original version of Ticket to Ride Europe there are 47 nodes (cities), 90 edges (connections) and 46 destination
cards (routes), and the game can be played by 2 to 5 players ([here](https://towardsdatascience.com/playing-ticket-to-ride-like-a-computer-programmer-2129ac4909d9)). 
For our research, this is simply too complex. Therefore, we aim to simplify the game such that we have 3 agents playing 
the game.

We will begin our implementation with a subset of the original board layout. For example, we can start by only taking
Western Europe. The number of destination cards will be influenced by the subset of the nodes that we take, and we assume
all agents have perfect knowledge about the possible routes in the game, that is, they know which destination cards are
in the game. We also apply the simplification that all destination cards are distributed among the agents. This
automatically removes the possibility to use a turn to obtain new route cards.

Additionally, to allow for knowledge to influence agent decisions in a reasonable way, we limit the agents to only two
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


## Model
Question: should we specify the model (K3, S4, S5, etc.)?

Let us define the following:
* $$A=\{a_1,a_2,\dots,a_m\}$$ be the set of $$m$$ agents;
* $$D=\{d_1,d_2,\dots,d_n\}$$ be the set of $$n$$ destination cards in the game;
* $$\mathbf{P}=\{p_{ij} \, \vert \, 1 \leq i \leq m, 1 \leq j \leq n\}$$ be the set of predicates where $$p_{ij}$$ 
  denotes agent $$i$$ has destination card $$j$$.

Here we take $$\frac{n}{m} \in \mathbb{N}$$, so the cards are evenly distributed among the agents. 

Now, let $$M=\langle S, \pi, R_1, \dots, R_m \rangle$$ be the Kripke model where
* $$S = \{(s_1,s_2,\dots,s_n) \, \vert \, s_i \text{ is the agent that owns the } i \text{-th card}\}$$ is the set of 
possible states;
* $$\pi : S \rightarrow \mathbf{P} \rightarrow \{t, f\}$$;
* $$R_i = \{\langle \mathbf{s}, \mathbf{t} \rangle \, \vert \, s_j = t_j \text{ for all } j \in \{1,\dots,n\} \text{ where } 
s_j = a_i\} \text{ for } 1 \leq i \leq m$$.

The set of states, $$S$$ is simply all combinations of destination card distributions over the agents, where each agent has the
same amount of destination cards. The valuation function $$\pi$$ assigns for each state a truth value to each predicate 
$$p_{ij} \in \mathbf{P}$$. The set of relations for agent $$i$$ is all relations between two states in which agent $$i$$
has the same destination cards.

At the start of the game, when the cards are evenly distributed among the agents, but the agents have not looked at their 
destination cards, each agent knows that each agent has $$\frac{n}{m}$$ destination cards. Moreover, each agent
knows that only one of agents has a specific train card, that is, for all 
$$j \in \{1,\dots,n\}$$ and $$i \in \{1,\dots,m\}$$

$$M \models K_i (p_{1j} \lor \dots \lor p_{mj}),$$

and for all $$i \in \{1,\dots,m\}$$, for all $$l \in \{1,\dots,m\}\backslash\{i\}$$

$$M \models K_i p_{ij} \rightarrow K_i \lnot p_{lj}.$$

After the agents have looked at their destination cards, the agents know which card they have, so for all 
$$i \in \{1,\dots,m\}$$ and all $$j \in \{1,\dots,n\}$$

$$M \models p_{ij} \rightarrow K_i p_{ij}.$$

### An Agent's turn

Consider now an agent's turn, say agent $$i$$, $$i\in\{1,\dots,m\}$$.
This agent has two options: 
* draw train cards (either from the visible or not visible cards);
* place trains on a connection between two cities (when having the correct amount of cards).

In case an agent chooses to draw train cards, the agent can draw the first card from either the (5) visible cards or the 
closed deck.
In case the agent does not draw a locomotive train card from the visible cards, it can pick another card from either the visible cards or the closed deck. 
In case an agent chooses to place trains on a connection between two cities, 

At the start of the game, the agents 


A* path finding voor beslissen waar agent heen gaat. Agent gaat altijd voor route vanaf start/eindpunt.
Hoe gaan we moves ranken?


### End-game
Einde van spel:
* Als een speler nog twee treinen over heeft mag iedereen nog 1 ronde spelen
* Een speler heeft alle routes gehaald
* Als het voor geen een speler meer mogelijk om een route te halen