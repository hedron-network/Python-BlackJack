import random

""" Converts card into a string for displaying png image. """

def get_image_path(card):
    rank = card[:-1]
    suit_sym = card[-1]
    suit_map = {"♠": "Spades", "♥": "Hearts", "♦": "Diamonds", "♣": "Clubs"}
    return f"{rank}_{suit_map[suit_sym]}.png"


class Game21:
    """ Initializes the game and starts a fresh round. """

    def __init__(self):
        self.new_round()

    """ Prepares for a new round by creating a deck and resetting hands. """

    def new_round(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_hidden_revealed = False

    """ Deals two cards to both the player and the dealer. """

    def deal_initial_cards(self):
        self.player_hit()
        self.player_hit()
        self.dealer_hit()
        self.dealer_hit()

    """ Creates a standard 52-card deck as text strings. """

    def create_deck(self):
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    """ Removes and returns the top card from the deck. """

    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return None

    """ Converts a card string into its numeric value. """

    def card_value(self, card):
        rank = card[:-1]
        if rank in ["J", "Q", "K"]:
            return 10
        if rank == "A":
            return 11
        return int(rank)

    """ Calculates the best possible total score for a hand, handling Aces. """

    def hand_total(self, hand):
        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card.startswith("A"))
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    """ Handles player logic for hitting or standing. """

    def hit_or_stand_choice(self, player_choice):
        if player_choice == 'stand':
            return False
        elif player_choice == 'hit':
            self.player_hit()
            return self.player_total() < 21
        return True

    """ Adds a card to the player's hand and returns it. """

    def player_hit(self):
        card = self.draw_card()
        if card:
            self.player_hand.append(card)
        return card

    """ Returns the player's current hand total. """

    def player_total(self):
        return self.hand_total(self.player_hand)

    """ Adds a card to the dealer's hand and returns it. """

    def dealer_hit(self):
        card = self.draw_card()
        if card:
            self.dealer_hand.append(card)
        return card

    """ Returns True if the dealer is required to hit (score < 17). """

    def dealer_should_hit(self):
        return self.dealer_total() < 17

    """ Sets the dealer's hidden card to revealed status. """

    def reveal_dealer_card(self):
        self.dealer_hidden_revealed = True

    """ Returns the dealer's current hand total. """

    def dealer_total(self):
        return self.hand_total(self.dealer_hand)

    """ Evaluates the outcome of the round and returns a status key. """

    def decide_winner(self):
        p_score = self.player_total()
        d_score = self.dealer_total()

        if p_score > 21:
            return "BUST"
        if p_score == 21 and len(self.player_hand) == 2:
            if d_score == 21 and len(self.dealer_hand) == 2:
                return "PUSH"
            return "BLACKJACK"
        if d_score > 21:
            return "DEALER_BUST"
        if p_score > d_score:
            return "WIN"
        elif p_score < d_score:
            return "LOSS"
        else:
            return "PUSH"

    """ 
    Ask the player if they want to do another round (je suppose ça sera des cmdbutton)
    """
    def ask_to_play_again(ui_response):
        return ui_response


class BettingSystem:
    """ Initializes the bankroll and bet settings. """

    def __init__(self, starting_deposit=1000):
        self.balance = starting_deposit
        self.current_bet = 0

    """ Validates and sets the current bet amount. """

    def Bet(self, amount):
        if amount.lower() == "all in":
            actual_amount = self.balance
        else:
            try:
                actual_amount = int(amount)
            except ValueError:
                return False

        if 0 < actual_amount <= self.balance:
            self.current_bet = actual_amount
            self.balance -= actual_amount
            return True
        return False

    """ Updates balance based on result multipliers and returns payout. """

    def resolve_bet(self, result_key):
        multipliers = {
            "BUST": 0, "LOSS": 0, "PUSH": 1,
            "WIN": 2, "DEALER_BUST": 2, "BLACKJACK": 2.5
        }
        payout = int(self.current_bet * multipliers.get(result_key, 0))
        self.balance += payout
        self.current_bet = 0
        return payout


""" Handles the main game loop and user interaction. """


def main():
    starting_funds = 1000
    game_bank = BettingSystem(starting_funds)
    game = Game21()

if __name__ == "__main__":
    main()