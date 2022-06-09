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
all players have perfect knowledge about the possible routes in the game, that is, they know which destination cards are
in the game. We also apply the simplification that all destination cards are distributed among the players. This
automatically removes the possibility to use a turn to obtain new route cards.

Additionally, to allow for knowledge to influence player decisions in a reasonable way, we limit the players to only two
ways to place trains: either claim a section of railway such that you progress on one of your own routes, or such that
you hinder your opponent based on what you know about their possible routes. This means that knowledge will directly
influence the strategies of the players. If a player cannot claim any routes that are allowed within the limitations of
the two possibilities, they can draw new train cards following the original game rules: two cards (open or closed), or 
one open joker card. Lastly, we initially omit the placement of train stations to simplify the procedure of the game.

It should be noted that real world players obtain a degree of knowledge from what colour cards an opponent draws. This
is however a very complex -- and definitely not foolproof -- strategy to implement. It would require an agent to take into
account all shortest routes with all colours that are relevant for those routes, and update its knowledge every round
in which cards are drawn. Additionally, players could draw certain cards to mislead players that use knowledge about
drawn cards. It is also possible that due to certain routes being claimed, the shortest route is no longer available, and
a certain colour might be drawn to cover a specific detour, adding more complexity. For this reason, no such knowledge
is used by our agents.

Due to the fact that players only have two possible moves when claiming routes, we can encounter a situation where no
player is allowed to claim a new route as there is no possible route that allows reaching the destination or hinder
opponents. This is a unique situation due to our simplifications and will be a cause for termination of the game when all
three players encounter this situation successively.


## Model
Let us define the following:
* $$A=\{a_1,a_2,\dots,a_m\}$$ be the set of $$m$$ agents;
* $$D=\{d_1,d_2,\dots,d_n\}$$ be the set of $$n$$ destination cards in the game;

Let $$M=\langle S, \pi, R_1, \dots, R_m \rangle$$ be the Kripke model where $$S$$ is the set of 
possible states (card distribution among the players (or hidden), so for $$s \in S$$ we have $$|s|=n$$), 
$$\pi$$ is the valuation function and $$R_i$$ is the set of relations for player $$i$$, $$i \in \{1,\dots,m\}$$.

Consider a player's turn, say player $i$.
Then it has this player has three options: pick two train cards (either from the visible or not visible cards), 
obtain a train route (when having the correct amount of cards), or 


We start with m=3 and n=9.



## Github stuff
You can use the [editor on GitHub](https://github.com/lennard134/TicketToRideLAMAS/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/lennard134/TicketToRideLAMAS/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
