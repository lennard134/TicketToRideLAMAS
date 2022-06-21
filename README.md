# Playing 'Ticket To Ride' Using Knowledge
***
mention loading route cards

*** 
## Design choices:
- Only using Western Europe
- If 2 segments of routes are equally optimal: choose segment of route with most score-points.

## Staying with blocking strategy
- only allow train placement based on own card
- unless 100% certain for agent x that agent y has card z
- then agent x can block agent z, but agent x has to PUBLICLY announce that it knows that y has card z 

## Switching away form blocking strategy
THIS IS NO LONGER RELEVANT, BUT I WILL NOT WASTE MY EFFORTS!
- only allow train placement based on own card
- this yields more knowledge of other players cards
- can implement win condition if player knows all cards of all players
- perhaps add strategies
  - vanilla
  - passive player