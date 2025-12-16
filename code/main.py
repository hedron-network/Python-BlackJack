from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QBoxLayout
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect
import sys

from tenacity import retry_unless_exception_type

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of 21")

        # set the windows dimensions
        self.setGeometry(200, 50, 700, 700)
        self.game = Game21()
        self.cards = []
        self.cardBack = None
        self.deckAsset = None
        self.loadAssets()
        if len(self.cards) == 0 or self.cardBack is None or self.deckAsset is None:
            print("Error Loading Cards Assets")
        self.initUI()


    def initUI(self):
        # Create and arrange widgets and layout. Remove pass when complete.
        pass

        #region Container Setup
        self.mainContainer = QWidget()
        self.mainContainer.setObjectName("mainContainer")
        self.mainContainer.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.mainContainer)

        self.animationOverlayContainer = QWidget(self.mainContainer) # makes an overlay widget
        self.animationOverlayContainer.setContentsMargins(0, 0, 0, 0)
        self.animationOverlayContainer.setObjectName("animationOverlayContainer")
        self.animationOverlayContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        mainVerticalLayout = QVBoxLayout(self.mainContainer)
        mainVerticalLayout.setContentsMargins(0,0,0,0)
        mainVerticalLayout.setSpacing(0)
        topContainer = QWidget()
        topContainer.setObjectName("topContainer")
        self.bottomContainer = QWidget()
        self.bottomContainer.setObjectName("bottomContainer")
        upperHorizontalLayout = QHBoxLayout()
        upperHorizontalLayout.setContentsMargins(0,0,0,0)
        upperHorizontalLayout.setSpacing(0)
        lowerHorizontalLayout = QHBoxLayout()
        lowerHorizontalLayout.setContentsMargins(0,0,0,0)
        lowerHorizontalLayout.setSpacing(0)
        self.mainContainer.setLayout(mainVerticalLayout)
        topContainer.setLayout(upperHorizontalLayout)
        self.bottomContainer.setLayout(lowerHorizontalLayout)
        mainVerticalLayout.addWidget(topContainer,1)
        mainVerticalLayout.addWidget(self.bottomContainer,1)

        self.topLeftContainer = QWidget()
        self.topLeftContainer.setObjectName("topLeftContainer")
        self.topRightContainer = QWidget()
        self.topRightContainer.setObjectName("topRightContainer")
        self.bottomLeftContainer = QWidget()
        self.bottomLeftContainer.setObjectName("bottomLeftContainer")
        self.bottomRightContainer = QWidget()
        self.bottomRightContainer.setObjectName("bottomRightContainer")

        upperHorizontalLayout.addWidget(self.topLeftContainer,1)
        upperHorizontalLayout.addWidget(self.topRightContainer,1)
        lowerHorizontalLayout.addWidget(self.bottomLeftContainer,1)
        lowerHorizontalLayout.addWidget(self.bottomRightContainer,1)
         #endregion

        #region Deck
        self.topRightContainerLayout = QVBoxLayout()
        self.topRightContainerLayout.setContentsMargins(0,0,0,0)
        self.topRightContainer.setLayout(self.topRightContainerLayout)
        self.deckLabel = QLabel()
        self.deckLabel.setObjectName("deck")
        self.topRightContainerLayout.addWidget(
            self.deckLabel,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop

        )
        self.deckLabel.setPixmap(self.deckAsset)
        #endregion

        self.bottomRightContainerLayout = QVBoxLayout()
        self.bottomRightContainer.setLayout(self.bottomRightContainerLayout)
        self.drawButton = QPushButton("Draw")
        self.bottomRightContainerLayout.addWidget(self.drawButton)


        self.cardToDrawStartingGeometry = QRect(self.width()-(88+10),0+10,88,124)
        self.cardToDraw = QLabel(self.animationOverlayContainer)
        self.cardToDraw.setPixmap(self.cardBack)
        self.cardToDraw.setFixedSize(88,124)
        self.cardToDraw.setGeometry(self.DrawCardStartGeometry())

        self.playerCardsContainer = QWidget(self.bottomContainer)
        self.playerCardsContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.playerCardsContainer.setObjectName("cardsContainer")
        self.playerCardsLayout = QHBoxLayout()
        self.playerCardsContainer.setLayout(self.playerCardsLayout)
        self.playerCardsLayout.setSpacing(5)
        self.playerCardsLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        self.playerCardsContainer.setGeometry(self.bottomContainer.rect())
        self.drawButton.clicked.connect(lambda : self.CardDrawAnimation("10♠",True))

        # TODO: Dealer Section with cards
        self.dealerCards =[]
        # TODO: Player Section with cards
        self.playerCards = []
        #  TODO: Buttons for hit, stand, new round

        #  TODO: Feedback

        #  TODO: Add widgets to layout

        #  TODO: Trigger a new layout with a new round

        self.animationOverlayContainer.raise_()

    def loadAssets(self):
        for suit in self.game.suits:
            for rank in self.game.ranks:
                pixmap = QPixmap("./assets/cards/Fronts/" + rank + suit + "_card.png").scaled(88,124)
                self.cards.append(pixmap)
        self.cardBack = QPixmap("./assets/cards/backs/Flat/Card_Back.png")
        self.deckAsset = QPixmap("./assets/cards/backs/Flat/Card_DeckA-88x140.png").scaled(88, 140)

    """Resize overlays"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'animationOverlayContainer'):
            self.animationOverlayContainer.setGeometry(self.mainContainer.rect())
        if hasattr(self, 'cardToDraw'):
            self.cardToDraw.setGeometry(self.DrawCardStartGeometry())
        if hasattr(self, 'playerCardsContainer'):
            self.playerCardsContainer.setGeometry(self.bottomContainer.rect())
    # BUTTON ACTIONS
    def CardDrawAnimation(self, cardToDraw, isPlayerDrawing):
        cardsInHand =0
        self.cardDrawAnimation = QPropertyAnimation(self.cardToDraw, b"geometry")
        startPosition = self.cardToDraw.geometry()
        self.cardDrawAnimation.setStartValue(startPosition)
        if isPlayerDrawing:
            cardsInHand = len(self.playerCards)
            endPosition = QRect(
                self.width() // 2 + self.cardToDraw.width() // 2 * cardsInHand,
                self.playerCardsContainer.geometry().y() + self.bottomContainer.pos().y(),
                self.cardToDraw.width(),
                self.cardToDraw.height())
            self.cardDrawAnimation.setEndValue(endPosition)
        else:
            pass
        self.cardDrawAnimation.setDuration(1000)
        self.cardDrawAnimation.setEasingCurve(QEasingCurve.Type.InOutExpo)
        self.cardDrawAnimation.start()
        self.cardDrawAnimation.finished.connect(lambda : self.ResetDeck(cardToDraw) )
    def DrawCardStartGeometry(self):
        return QRect(self.width()-(88+10),0+10,88,124)
    def ResetDeck(self,card):
        self.cardToDraw.setGeometry(self.DrawCardStartGeometry())
        self.add_card(self.playerCardsLayout, card)

    def CardToPixmap(self, card):
        suit = card[-1]
        rank = card[:-1]
        suitIndex = self.game.suits.index(suit)
        rankIndex = self.game.ranks.index(rank)
        cardIndex = 14* suitIndex + rankIndex
        return self.cards[cardIndex]

    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)

        if self.game.player_total() > 21:
          # TODO: what should happen if a player goes over 21? Remove pass when complete
          pass

    def on_stand(self):
        # TODO: Player ends turn; dealer reveals their hidden card and plays. Remove pass when complete
        pass

    def on_new_round(self):
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS

    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self,layout, card):
        NewCardLabel = QLabel(self.animationOverlayContainer)
        NewCardLabel.setPixmap(self.CardToPixmap(card))
        NewCardLabel.setFixedSize(88,124)
        layout.addWidget(NewCardLabel)
        NewCardLabel.show()

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, "??")   # face-down
            else:
                self.add_card(self.dealerCardsLayout, card)

        # TODO: update relevant labels in response to dealer actions. Remove pass when complete
        if full:
            pass
        else:
            pass

    def new_round_setup(self):
        # TODO: Prepare a fresh visual layout

        # TODO: update relevant labels (reset dealer and player totals)

        # TODO: display new cards for dealers and players

        # TODO: enable buttons for Stand and Hit - Remove pass when complete
        pass


    def end_round(self):
        # TODO: Disable button actions after the round ends. Remove pass when complete
        pass


# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)
    with open("QSS_Blackjack.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
