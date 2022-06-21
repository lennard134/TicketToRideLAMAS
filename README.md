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
- only allowed to block when also publicly announcing this
- we will not allow agents to find a shorter route in one step as this will add unwanted uncertainty
- FOR NOW we will only allow agents to work on one route at a time. This is because we need to figure out a way to avoid
  incorrectly attributing connections of two separate route cards to a single route

## Switching away form blocking strategy
THIS IS NO LONGER RELEVANT, BUT I WILL NOT WASTE MY EFFORTS!
- only allow train placement based on own card
- this yields more knowledge of other players cards
- can implement win condition if player knows all cards of all players
- perhaps add strategies
  - vanilla
  - passive player