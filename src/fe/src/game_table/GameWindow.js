var myGameWindow = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 480;
        this.canvas.height = 270;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        this.interval = setInterval(updateGameArea, 20);
        },
    clear : function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

// num_players             int
// state                   enum, refer GameEngine.py
// players                 list of json objects, see PlayerStrategy.py
// player_hands            list of lists of cards representing hands available to players
// starting_player         int, index of left of the dealer
// bid_history             list of json object, see Bid.py
// game_rounds             list of json object, see Round.py
// imminent_trump_request  bool True/False depending on if a trump card has been requested
// red_overall_pts         int, points secured by red team over presumably > 1 game
// blue_overall_pts        int, points secured by blue team over presumably > 1 game
// game_bid                bid json object, see Bid.py, represents the bid that the table settled on
// current round           json object if currently playing rounds, None otherwise
// hidden_trump_card       None if revealed, or not yet initialized

function update_game_window(game_engine, player_index) {
    this.num_players = game_engine.num_players;
    this.state = game_engine.state;
		this.players = game_engine.players;
		this.player_hands = game_engine.player_hands;
    this.starting_player_index = game_engine.starting_player;
    this.bid_history = game_engine.bid_history;
    this.game_rounds = game_engine.game_rounds;
    this.current_round = game_engine.current_round;
    this.game_bid = game_engine.game_bid;
    this.imminent_trump_request = game_engine.imminent_trump_request;
		this.red_overall_pts = game_engine.red_overall_pts;
		this.blue_overall_pts = game_engine.blue_overall_pts;

		this.hand_position = (myGameArea.canvas.width / 3, myGameArea.canvas.height / 2);
		this.card_width = 10
		this.card_height = 35

		// Needs to render card images for the current hand
    this.update = function() {
        ctx = myGameArea.context;
				shown_hand = this.player_hands[player_index];
				// Render shown hand
				function render_my_cards(card, pos) {
					var img = document.getElementByID(card.rank + card.suit);
					ctx.drawImage(img, this.hand_position[0]+pos*this.card_width, this.hand_position[1], this.card_width, this.card_height);
				}
				for (let i = 0; i < shown_hand.length; i++) {
					render_my_cards(shown_hand[i], i);
				}
				let i = 1;

				let pos_right = (4 * myGameArea.canvas.width / 5, 2 * myGameArea.canvas.height / 3);
				let pos_left = (1 * myGameArea.canvas.width / 5, 2 * myGameArea.canvas.height / 3);
				let pos_opp = (myGameArea.canvas.width / 3, 4 * myGameArea.canvas.height / 5);
				let pos = (pos_right, pos_left, pos_opp);

				function render_facedown(x, y, orient) {
					var img = document.getElementByID('face-down');
					ctx.drawImage(img, x, y, this.card_width, this.card_height)
				}

				function render_card(x, y, card) {
					var img = document.getElementByID(card.rank + card.suit);
					ctx.drawImage(img, x, y, this.card_width, this.card_height);
				}

				while i < this.num_players {
					if this.num_players == 4 {
						for (let j = 0; j < player_hands[i + player_index]; j++) {
							render_facedown(pos[i-1][0] + this.card_width*j, pos[i-1][1])
						}
					}
					i++;
			}

			let positions = {0 : (myGameArea.canvas.width / 3, (myGameArea.canvas.height / 2) + 2*this.card_height),
			1 : (4 * myGameArea.canvas.width / 5 - 5*this.card_width, (2 * myGameArea.canvas.height / 3),
			2 : (myGameArea.canvas.width / 3 , (4 * myGameArea.canvas.height / 5) - 2*this.card_height),
		 	3: (1 * myGameArea.canvas.width / 5 + 5*this.card_width, (2 * myGameArea.canvas.height / 3)}
			if (!!this.current_round) {
				if (this.game_rounds.length == 0) {
					let round_starter = this.starting_player;
				} else {
					let round_starter = this.game_rounds[this.game_rounds.length - 1].winning_player.number;
				}
				for (let j = 0; j < this.current_round.cards_played.length; j++) {
					render_card(positions[(round_starter+j) % this.num_players][0], positions[(round_starter+j) % this.num_players][1], this.current_round.cards_played[j]);
				}

			}
    }
}
