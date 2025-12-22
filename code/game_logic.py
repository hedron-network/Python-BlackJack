import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.current_bet = 0
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        """Init statistics variables"""
        self.total_rounds = 0
        self.total_bet_amount = 0
        self.total_gain = 0
        self.total_player_score = 0
        self.total_dealer_score = 0

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
        else:
            return "PUSH"


    def Bet(self, amount):
        self.current_bet = amount


    """ Updates balance based on result multipliers and returns payout. """
    def resolve_bet(self, result_key):
        multipliers = {
            "BUST": 0, "LOSS": 0, "PUSH": 1,
            "WIN": 2, "DEALER_BUST": 2, "BLACKJACK": 2.5
        }

        payout = int(self.current_bet * multipliers[result_key])

        """Update Statistic"""
        self.total_rounds += 1
        self.total_bet_amount += self.current_bet
        self.total_gain += payout
        self.total_player_score += self.player_total()
        self.total_dealer_score += self.dealer_total()

        self.current_bet = 0
        return payout//1


    """Statistic Methods"""
    def average_bet(self):
        if self.total_rounds == 0:
            return 0
        return self.total_bet_amount / self.total_rounds


    def average_gain(self):
        if self.total_rounds == 0:
            return 0
        return self.total_gain / self.total_rounds


    def average_player_score(self):
        if self.total_rounds == 0:
            return 0
        return self.total_player_score / self.total_rounds


    def average_dealer_score(self):
        if self.total_rounds == 0:
            return 0
        return self.total_dealer_score / self.total_rounds


    def stats(self):
        return {
            "rounds_played": self.total_rounds,
            "total_gain": self.total_gain,
            "average_bet": round(self.average_bet(), 2),
            "average_gain": round(self.average_gain(), 2),
            "average_player_score": round(self.average_player_score(), 2),
            "average_dealer_score": round(self.average_dealer_score(), 2),
        }
