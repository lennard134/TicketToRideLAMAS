# Playing 'Ticket To Ride' Using Knowledge
***
mention loading route cards

***

# TODO: add assumption that we do not use tunnel connections

## Design choices:
- Only using Western Europe
- If 2 segments of routes are equally optimal: choose segment of route with most score-points. If score points are equal
  do a random choice
- Only single connections are allowed, in the real game with 3 players this is also the case JUSTIFIED

## Staying with blocking strategy
- only allow train placement based on own card
- unless 100% certain for agent x that agent y has card z
- then agent x can block agent z, but agent x has to PUBLICLY announce that it knows that y has card z 
- only allowed to block when also publicly announcing this
- we will not allow agents to find a shorter route in one step as this will add unwanted uncertainty
- a card is drawn from the open cards based on whether the route has the most points

- randomly select agent and connection if multiple are possible.

## Switching away form blocking strategy
THIS IS NO LONGER RELEVANT, BUT I WILL NOT WASTE MY EFFORTS!
- only allow train placement based on own card
- this yields more knowledge of other players cards
- can implement win condition if player knows all cards of all players
- perhaps add strategies
  - vanilla
  - passive player