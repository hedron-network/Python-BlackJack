import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.current_bet = 0
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        self.new_round()

        """ Prepares for a new round. """
    def new_round(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_hidden_revealed = False
        self.deal_initial_cards()

    """ Deals two cards to both player and dealer. """
    def deal_initial_cards(self):
        self.player_draw()
        self.player_draw()
        self.dealer_draw()
        self.dealer_draw()

    """ Creates a standard 52-card deck. """
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

    """ Calculates the total score of a hand, handling Aces. """
    def hand_total(self, hand):
        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card.startswith("A"))
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    """ Returns True if the dealer must draw a card (score < 17). """
    def dealer_turn(self):
        return self.hand_total(self.dealer_hand) < 17

    """ Draws a card for the player and returns it. """
    def player_draw(self):
        card = self.draw_card()
        if card:
            self.player_hand.append(card)
        return card

    """ Draws a card for the dealer and returns it. """
    def dealer_draw(self):
        card = self.draw_card()
        if card:
            self.dealer_hand.append(card)
        return card

    """ Returns the player's hand total. """
    def player_total(self):
        return self.hand_total(self.player_hand)

    """ Returns the dealer's hand total. """
    def dealer_total(self):
        return self.hand_total(self.dealer_hand)


    """ Evaluates the outcome of the round. """
    def decide_winner(self):
        p_score = self.player_total()
        d_score = self.dealer_total()
        if p_score > 21: return "BUST"
        if p_score == 21 and len(self.player_hand) == 2:
            if d_score == 21 and len(self.dealer_hand) == 2: return "PUSH"
            return "BLACKJACK"
        if d_score > 21: return "DEALER_BUST"
        if p_score > d_score: return "WIN"
        elif p_score < d_score: return "LOSS"
        else: return "PUSH"


    def Bet(self, amount):
        self.current_bet = amount


    """ Updates balance based on result multipliers and returns payout. """

    def resolve_bet(self, result_key):
        multipliers = {
            "BUST": 0, "LOSS": 0, "PUSH": 1,
            "WIN": 2, "DEALER_BUST": 2, "BLACKJACK": 2.5
        }
        payout = int(self.current_bet * multipliers.get(result_key, 0))
        self.current_bet = 0
        return payout
