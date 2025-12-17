import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
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
    Player action
    """

    def hit_or_stand_choice(player_choice, deck, player_hand):
        if player_choice == 'stand':
            return False
            """
             Ends the player's turn and authorizes the dealer to start playing.
             """

        elif player_choice == 'hit':
            player_continue = player_hit(deck, player_hand)
            return player_continue
        return True


    """
    Adds a card and checks if the player is allowed to continue.
    """

    def player_hit(deck, player_hand):
        player_hand.append(deck.pop())
        score = calculate_score(player_hand)

        if score > 21:
            return player_hand, False
        return player_hand, True

    """Return the player's total."""
    def player_total(self):

        return self.hand_total(self.player_hand)

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

        player_score = calculate_score(player_hand)
        dealer_score = calculate_score(dealer_hand)

        if player_score > 21:
            return "BUST"

        if len(player_hand) == 2 and player_hand == 21:
            if len(dealer_hand) == 2 and dealer_score == 21:
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

    def resolve_bet(self, result_key):
        multipliers = {
            "BUST": 0, "LOSS": 0, "PUSH": 1,
            "WIN": 2, "DEALER_BUST": 2, "BLACKJACK": 2.5
        }
        payout = int(self.current_bet * multipliers.get(result_key, 0))
        self.balance += payout
        self.current_bet = 0
        return payout


""" 
Converts card into a string for displaying png image. 
"""
def get_image_path(card):
    return f"{card['rank']}_{card['suit']}.png"

""" 
Checks if the current balance has doubled compared to the starting deposit.
Returns True if the Casino should get his revenge on you.
"""
def check_casino_revenge(current_balance, starting_deposit):
    return current_balance >= (starting_deposit * 2)


""" 
If check_casino_revenge = true : you are dans la merde
"""
def trigger_casino_revenge_messagebox():

    return "CASINO REVENGE: You have doubled your money! The house is watching... All your family i brutally murdered and you are sent to jail for that murder, you got raped and killed because the house alwys win"


"""
Main 
handle game system
"""

def main():
    game_bank = BettingSystem(1000)

    while game_bank.balance > 0:
        user_bet


        deck = shuffle_deck(create_deck())
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        player_ace_choice = None


        is_player_turn = True
        while is_player_turn:
            score = calculate_score(player_hand, player_ace_choice)
            if score > 21: #bust
                is_player_turn = False
                break
            """
            # Ace choice 
            if can_choose_ace_value(player_hand) and player_ace_choice is None:
                choice = 
                player_ace_choice = int(choice) if choice in ['1', '11'] else None
                continue
            """
            action = # doit relier au bouton hit ou stand
            hit_or_stand_choice(action)


        if calculate_score(player_hand, player_ace_choice) <= 21: #now dealer turn
            while dealer_should_hit(dealer_hand):
                new_card = deck.pop()
                dealer_hand.append(new_card)

        result = get_round_result(player_hand, dealer_hand, player_ace_choice)
        payout, revenge_triggered = game_bank.resolve_bet(result)


        # The 'Casino Revenge' Textbox logic
        if revenge_triggered:
            trigger_casino_revenge_messagebox()

        if not ask_to_play_again() :
            break



if __name__ == "__main__":
    main()