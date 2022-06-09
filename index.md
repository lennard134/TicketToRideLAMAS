# Ticket to Ride

## Test
$x^2$

$$
x^2
$$

## Introduction hello
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
In the original version of Ticket to Ride Europe there are 47 nodes (cities), 90 edges (connections) and 46 destination cards (routes), and the game can be played by 2 to 5 players ([here](https://towardsdatascience.com/playing-ticket-to-ride-like-a-computer-programmer-2129ac4909d9)). 
For our research, this is simply too complex. 
Therefore, we aim to simplify the game such that we have 3 agents playing the game. 
We will begin our implementation with a subset of the original board layout. 
For example, only taking western Europe. 
The number of destination cards will be influenced by the subset of the nodes that we take, and we assume all players have perfect knowledge about the possible routes in the game, that is, they know which destination cards are in the game. 
We also make the simplification that all destination cards are distributed among the players. 
Lastly, placement of train stations is omitted.

## Model
Let $M=\langle S, \pi, R_1, \dots, R_m \rangle$ be the Kripke model where $S$ is the set of possible states (card distribution among the players (or hidden)), $\pi$ is the valuation function and $R_i$ is the set of relations for player $i$, $i \in \{1,\dots,m\}$.


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
