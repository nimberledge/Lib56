# Lib56
Game Engine and PlayerStrategy template for 56, the card game. The plan is to expand this into a web-app, but after we get an initial framework up and running, the app stage should be easier.

HumanPlayerStrategy is probably the easiest player strategy to implement, we can have that work based on input, and adapt that to the web-app.

Highly incomplete as of date, but if I ever get off my ass and make this thing a reality it will be a nice day for us all.

For now, there's a badly written multi-player interface at https://github.com/nimberledge/try56
# Rules of the game
56 is a 4 or 6 player team game. Players sit in a circle labeled 1-6, with alternate players on the same team (1, 3, 5). The game is comprised of two rounds -
1. The bidding round
2. Table round
At the start of the game, players are dealt hands of 8 cards from 2 truncated decks.
The cards in this deck are 9, 10, J, Q, K, A, (of all suits) and 2 copies (from 2 decks) of each card. In the 4 player game, Kings and Queens are omitted. In the game, the precedence order is as follows:
	1. J - 3 points
	2. 9 - 2 points
	3. A - 1 point (higher than 10)
	4. 10 - 1 point (lower  than A)
	5. K - 0 points (higher than Q)
	6. Q - 0 points (lower than K)
	Based on the initial hand, players will bid various point amounts. A bid is essentially a wager that the bidding player's team will make X amount of points. One makes points during the second round.

	There's no good reason for the J-9-A-10 hierarchy of cards but it's a whole thing. Please just deal with it.
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
- The winner of the bidding round selects a card from their hand to put face down on the table. This card represents the "trump" suit, chosen by the winner of the bidding.
- Left of the dealer starts the first round, players play in turns counter clockwise
- Every subsequent player plays a card that matches the suit played by the starting player, if possible
- If not possible, players have the option of
	1. Playing a card of any other suit
	2. If the trump card is hidden, requesting the trump card
	3. If the trump is revealed, either i, or more specifically playing a card of the trump suit, aka a "cut"
- In each round, the highest card played wins. The player who played the card wins the round for their respective team. The winning player also starts the subsequent round.
- A card of the trump suit is higher than any card of any other suit
- Until the trump is revealed, trump suit cards hold no (higher) value
- Once the trump card is requested, the winner of the bid will uncover the card on the table, visible to all players, and return it to their hand. After this, all trump suit cards are higher than cards of other suits.
- At the end of 8 rounds, the sum of points in the rounds won by the bidding team is counted. Based on whether the bid is made, points are awarded based on the earlier mentioned scheme.
- Dealer shifts to the left, rinse and repeat ad nauseam

## Void rounds
- In real life, a game is void if a player sees cards that aren't their own or if the dealer deals an uneven number of cards. In this case the dealer does not shift, and the cards are re-shuffled and re-dealt
- In addition, if it becomes apparent during roundplay that the defending team had zero cards of the trump suit, the game is void and the cards are re-shuffled and re-dealt

## Playing irl
- Generally, the dealer has the sole say on how much shuffling is to be done in the deck
- After a few rounds of 56, cards tend to bunch up a bit by suit and less shuffling gives more favourable deals
- Right of the dealer cuts the deck after the dealer has shuffled
- The dealer deals 4 cards at a time to each player, starting with left of the dealer, going 2 rounds around the circle and dealing themselves the last 4 cards

If you want an example of a game, just run GameEngine.py. The logging is an ok representation. There's absolutely 0 logic in the default setting, so probably not good to base strategy on, but the game mechanics are consistent.

PS: help me write an imperfect shuffle for my 56 deck
