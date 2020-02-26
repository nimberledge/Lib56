# Lib56
Game Engine and PlayerStrategy template for 56, the card game. The plan is to expand this into a web-app, but after we get an initial framework up and running, the app stage should be easier.

HumanPlayerStrategy is probably the easiest player strategy to implement, we can have that work based on input, and adapt that to the web-app.

Highly incomplete as of date, but if I ever get off my ass and make this thing a reality it will be a nice day for us all.

# Rules of the game
56 is a 4 or 6 player team game. Players sit in a circle labeled 1-6, with alternate players on the same team (1, 3, 5). The game is comprised of two rounds -
1. The bidding round
2. Table round
At the start of the game, players are dealt hands of 8 cards from a truncated deck.
The cards in this deck are 9, 10, J, Q, K, A. In the 4 player game, Kings and Queens are omitted. In the game, the precedence order is as follows:
	1. J - 3 points
	2. 9 - 2 points
	3. A - 1 point (higher than 10)
	4. 10 - 1 point (lower  than A)
	5. K - 0 points (higher than Q)
	6. Q - 0 points (lower than K)
	Based on the initial hand, players will bid various point amounts. A bid is essentially a wager that the bidding player's team will make X amount of points. One makes points during the second round.
## Bidding rules
- Left of the dealer starts, with a minimum compulsory bid of 28 points
- Players take turns counterclockwise to either bid a higher amount, or pass
- Bidding stops when (n-1) players pass in a row
- Bids in the 28-39 range give the bidding team 1 point for winning their bid, and -2 points if they lose their bid
- Bids in the 40-55 range give the bidding team 2 points for winning, and -3 points for losing the bid
- 56 is a special bid, called 'tani'. The bidding player plays without teammates, starts every round, and must simply win all rounds to achieve the bid. It is worth n points if won, and -n-1 if lost, where n is the number of players
- A player may not outbid a teammate's bid in the 28-39 range with anything less than a 40 bid
- A player may not bid twice in the 28-39 range

## Roundplay
- The winner of the bidding round selects a card from their hand to put face down on the table. This card represents the "trump" suite, chosen by the winner of the bidding.
- Left of the dealer starts the first round,
