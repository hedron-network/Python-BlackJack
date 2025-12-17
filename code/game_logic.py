import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.current_bet = 0
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        self.new_round()

    """Round management"""

    """
    Prepares for a new round
    """

    def new_round(self):

        self.deck = self.create_deck()
        random.shuffle(self.deck)

        # Index of the "next card" to deal
        self.deck_position = 0

        # Hands start empty
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    """
    Deal two cards each to player and dealer.
    """

    def deal_initial_cards(self):

        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    """
    Create a standard 52-card deck represented as text strings.
    """

    def create_deck(self):

        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        """
        Return the next card in the shuffled deck.
        """
        if self.deck_position < len(self.deck):
            card = self.deck[self.deck_position]
            self.deck_position += 1
            return card
        return None

    # --- HAND VALUES + ACE HANDLING ---

    def card_value(self, card):
        """
        Convert a card string into its numeric value.
        """
        rank = card[:-1]
        if rank in ["J", "Q", "K"]:
            return 10
        if rank == "A":
            return 11
        return int(rank)

    """
            Calculates the best possible total for a hand.
            Aces are counted as 11 unless this would bust the hand.
    """

    def hand_total(self, hand):

        total = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card.startswith("A"))

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    """
    Adds a card and checks if the player is allowed to continue.
    """

    def player_hit(self,deck, player_hand):
        player_hand.append(deck.pop())
        score = self.calculate_score(self.player_hand)

        if score > 21:
            return player_hand, False
        return player_hand, True

    """Return the player's total."""

    def player_total(self):

        return self.hand_total(self.player_hand)

    """ 
    Calculates the total value of a hand. 
    Aces are automatically treated as 11, but converted to 1 if the total exceeds 21 (J'ai check les règles). 
    """

    def calculate_score(self,hand):
        score = 0
        aces = 0
        for card in hand:
            if card['rank'] in ['Jack', 'Queen', 'King']:
                score = score + 10
            elif card['rank'] == 'Ace':
                aces += 1
                score += 11
            else:
                score += int(card['rank'])

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    """
    Dealer actions
    """

    """Called when the player presses Stand."""

    def reveal_dealer_card(self):
        self.dealer_hidden_revealed = True

    """Return the dealer's total."""

    def dealer_total(self):
        return self.hand_total(self.dealer_hand)

    """Dealer must hit until their total is 17 or more."""

    def dealer_turn(self):
        while self.dealer_total() < 17:
            self.dealer_hand.append(self.draw_card())

    """
           Evaluates player vs dealer hands.
           Returns a status string for the betting system and a display message.
    """

    def decide_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            return "BUST"

        if len(self.player_hand) == 2 and player_score == 21:
            if len(self.dealer_hand) == 2 and dealer_score == 21:
                return "PUSH"
            return "BLACKJACK"

        if dealer_score > 21:
            return "DEALER_BUST"

        if player_score > dealer_score:
            return "WIN"
        elif player_score < dealer_score:
            return "LOSS"
        else:
            return "PUSH"
    def Bet(self,amount):
        self.current_bet = amount
    def resolve_bet(self, result_key):
        multipliers = {
            "BUST": 0, "LOSS": 0, "PUSH": 1,
            "WIN": 2, "DEALER_BUST": 2, "BLACKJACK": 2.5
        }
        payout = int(self.current_bet * multipliers.get(result_key, 0))
        self.current_bet = 0
        return payout

"""
betting system
"""

class BettingSystem:
    def __init__(self, starting_deposit=1000):
        self.balance = starting_deposit
        self.current_bet = 0

    def Bet(self, amount):
        if amount == "All In":
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

