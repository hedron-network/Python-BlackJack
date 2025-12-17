import random
from typing import List

class Game21:
    def __init__(self) -> None:
        # Start immediately with a fresh round
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = self.create_deck()

        self.new_round()

    # ROUND MANAGEMENT

    def new_round(self) -> None:
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        random.shuffle(self.deck)

        # Instead of removing cards from the deck,
        # we keep an index of the "next card" to deal.
        self.deck_position = 0

        # Hands start empty; cards will be dealt after UI calls deal_initial_cards()
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    def deal_initial_cards(self) -> None:
        """
        Deal two cards each to player and dealer.
        """
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    # DECK AND CARD DRAWING

    def create_deck(self) -> List[str]:
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        return [f"{rank}{suit}" for rank in self.ranks for suit in self.suits]

    def draw_card(self) -> str:
        """
        Return the next card in the shuffled deck.
        """
        card = self.deck[self.deck_position]
        self.deck_position += 1
        return card

    # HAND VALUES + ACE HANDLING

    def card_value(self, card: str) -> int:
        """
        Convert a card string into its numeric value.

        Rules:
        - Number cards = their number (2–10)
        - J, Q, K = 10
        - A is normally 11, may later count as 1 if needed
        """
        rank = card[:-1]  # everything except the suit symbol

        if rank in ["J", "Q", "K"]:
            return 10

        if rank == "A":
            return 11  # Initially treat Ace as 11

        # Otherwise it's a number from 2 to 10
        return int(rank)

    def hand_total(self, hand: List[str]) -> int:
        """
        Calculates the best possible total for a hand.
        Aces are counted as 11 unless this would bust the hand,
        in which case they are reduced to 1.

        Suggested Process:
        1. Count all Aces as 11 initially.
        2. If total > 21, subtract 10 for each Ace, so it effectively makes them = 1
        """
        hand_value = 0
        aces_count = 0
        for card in hand:
            if card[:-1] == "A":
                aces_count += 1
            hand_value += self.card_value(card)

        while hand_value > 21 and aces_count > 0:
            hand_value -= 10
            aces_count -= 1

        return hand_value

    # PLAYER ACTIONS

    def player_hit(self):
        # TODO: Add one card to the player's hand and return it, so the UI can display the card. Remove pass when complete.
        pass

    def player_total(self):
        # TODO: Return the player's total. Remove pass when complete.
        pass

    # DEALER ACTIONS

    def reveal_dealer_card(self):
        # TODO: Called when the player presses Stand. After this, the UI should show both dealer cards. Remove pass when complete.
        pass


    def dealer_total(self):
        # TODO: Return the dealer's total. Remove pass when complete.
        pass

    def play_dealer_turn(self):
        # TODO: Dealer must hit until their total is 17 or more, then stand.  Remove pass when complete.
        pass

    # WINNER DETERMINATION

    def decide_winner(self):
        # TODO: Decide the outcome of the round.
        """
        Example: return the following text messages:
        - "Player busts. Dealer wins!"
        - "Dealer busts. Player wins!"
        - "Player wins!"
        - "Dealer wins!"
        - "Push (tie)."
        """

