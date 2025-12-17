from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGridLayout
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, pyqtProperty, QTimer
import sys

from holoviews import Overlay

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21
from custom_widgets import AudioPlayer,FlippableCard, QLabel_clickable


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.playerMoney = 1_000
        self.hiddenCard = None
        self.setWindowTitle("Game of 21")

        # set the windows dimensions
        self.setGeometry(100, 50, 1000, 700)
        self.mainContainer = QWidget()
        self.mainContainer.setObjectName("mainContainer")
        self.mainContainer.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.mainContainer)

        #region Asset Loading
        self.game = Game21()
        self.chips = []
        self.isometricChips = []
        self.chipsValue = [5,10,25,50,100,500]
        self.cards = []
        self.cardBack = None
        self.deckAsset = None
        self.audioPlayer = None
        self.InfoBar = None
        self.soundEffectPlayer = None
        self.backgroundPixmap = None
        self.loadAssets()
        if len(self.cards) == 0 or self.cardBack is None or self.deckAsset is None:
            print("Error Loading Cards Assets")
        #endregion
        self.initUI()


    def initUI(self):
        #region Container Setup

        self.background = QLabel(self.mainContainer)
        self.activeAnimations = []
        self.dealerFaceDownCard = None
        self.animationOverlayContainer = QWidget(self.mainContainer) # makes an overlay widget
        self.animationOverlayContainer.setContentsMargins(0, 0, 0, 0)
        self.animationOverlayContainer.setObjectName("animationOverlayContainer")
        self.animationOverlayContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        mainVerticalLayout = QVBoxLayout(self.mainContainer)
        mainVerticalLayout.setContentsMargins(0,0,0,0)
        mainVerticalLayout.setSpacing(0)
        self.topContainer = QWidget()
        self.topContainer.setObjectName("topContainer")
        self.bottomContainer = QWidget()
        self.bottomContainer.setObjectName("bottomContainer")
        upperHorizontalLayout = QHBoxLayout()
        upperHorizontalLayout.setContentsMargins(0,0,0,0)
        upperHorizontalLayout.setSpacing(0)
        lowerHorizontalLayout = QHBoxLayout()
        lowerHorizontalLayout.setContentsMargins(0,0,0,0)
        lowerHorizontalLayout.setSpacing(0)
        self.mainContainer.setLayout(mainVerticalLayout)
        self.topContainer.setLayout(upperHorizontalLayout)
        self.bottomContainer.setLayout(lowerHorizontalLayout)
        mainVerticalLayout.addWidget(self.topContainer,1)
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

        self.cardToDrawStartingGeometry = QRect(self.width() - (88 + 10), 0 + 10, 88, 124)
        self.cardToDraw = QLabel(self.animationOverlayContainer)
        self.cardToDraw.setPixmap(self.cardBack)
        self.cardToDraw.setFixedSize(88, 124)
        self.cardToDraw.setGeometry(self.DrawCardStartGeometry())
        #endregion

        # region MediaInfoBar
        self.audioPlayer.player.mediaStatusChanged.connect(lambda status: self.NextTrack(status))
        self.mediaInfoBarContainer = QWidget(self.topLeftContainer)
        self.mediaInfoBarContainer.setGeometry(0, 0, 0, 40)  # Start with 0 width
        self.mediaInfoBar = QLabel(self.mediaInfoBarContainer)
        self.mediaInfoBar.setPixmap(self.InfoBar)

        # Create layout for the text on top
        layout = QHBoxLayout(self.mediaInfoBarContainer)
        self.currentTrackLabel = QLabel()
        self.currentTrackLabel.setObjectName("currentTrackLabel")
        self.currentTrackLabel.setStyleSheet("background: transparent;")  # Make text background transparent
        layout.addWidget(self.currentTrackLabel)

        self.ShowCurrentTrackButton = QPushButton("show current track")
        self.ShowCurrentTrackButton.clicked.connect(lambda: self.ShowCurrentTrack())
        # endregion

        #region Betting
        self.bottomRightContainerLayout = QHBoxLayout()
        self.bottomRightContainerLayout.addStretch(2)
        self.bottomRightContainer.setLayout(self.bottomRightContainerLayout)
        self.bettingLayout = QVBoxLayout()
        self.chipsLayout = QGridLayout()
        self.chipsLayout.setSpacing(0)
        self.chipsLayout.setContentsMargins(0,0,0,0)
        self.bettingLayout.addLayout(self.chipsLayout)
        self.bottomRightContainerLayout.addLayout(self.bettingLayout, Qt.AlignmentFlag.AlignRight)
        print(len(self.chips))
        for i in range(0,len(self.chips)):
            chipButton = QLabel_clickable()
            chipButton.setObjectName("chipButton")
            chipButton.setPixmap(self.chips[i])
            chipButton.clicked.connect(lambda t=i: self.Bet(t))
            self.chipsLayout.addWidget(chipButton,i//3,i%3)
            OverlayLabel = QLabel(chipButton)
            OverlayLabel.setGeometry(20,20,25,20)
            OverlayLabel.setText(str(self.chipsValue[i]) + "$")
            OverlayLabel.setObjectName("overlayLabel")
            OverlayLabel.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )
        self.AllInButton = QPushButton("All In")
        self.AllInButton.clicked.connect(lambda : self.Bet(-1))
        self.bettingLayout.addWidget(self.AllInButton)
        self.bettingLayout.addStretch()
        # endregion

        #region Chips
        self.bottomLeftContainerLayout = QVBoxLayout()
        self.bottomLeftContainer.setLayout(self.bottomLeftContainerLayout)
        self.chipsContainer = QWidget()
        self.chipsContainer.setFixedWidth(4*64)
        self.bottomLeftContainerLayout.addWidget(self.chipsContainer)
        self.playedChips= []
        for i in range(0,len(self.chips)):
            self.playedChips.append([])
        #endregion

        #region Cards Containers
        self.playerCardsContainer = QWidget(self.bottomContainer)
        self.playerCardsContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.playerCardsContainer.setObjectName("cardsContainer")
        self.playerCardsLayout = QHBoxLayout()
        self.playerCardsContainer.setLayout(self.playerCardsLayout)
        self.playerCardsLayout.setSpacing(5)
        self.playerCardsLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.playerCardsContainer.setGeometry(self.bottomContainer.contentsRect())




        self.dealerCardsContainer = QWidget(self.topContainer)
        self.dealerCardsContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.dealerCardsContainer.setObjectName("cardsContainer")
        self.dealerCardsLayout = QHBoxLayout()
        self.dealerCardsContainer.setLayout(self.dealerCardsLayout)
        self.dealerCardsLayout.addSpacing(5)
        self.dealerCardsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        self.dealerCardsContainer.setGeometry(self.topContainer.contentsRect())
        # endregion

        """
        self.bottomRightContainerLayout = QVBoxLayout()
        self.bottomRightContainer.setLayout(self.bottomRightContainerLayout)
        self.drawButton = QPushButton("Draw")
        self.bottomRightContainerLayout.addWidget(self.drawButton)

        self.drawButton.clicked.connect(lambda : self.StartRound())
        self.revealButton = QPushButton("Reveal")
        self.bottomRightContainerLayout.addWidget(self.revealButton)
        self.revealButton.clicked.connect( lambda : self.ShowDealerCard())
        self.bottomRightContainerLayout.addWidget(self.ShowCurrentTrackButton)
        """
        # TODO: Dealer Section with cards
        self.dealerCards =0
        # TODO: Player Section with cards
        self.playerCards = 0
        #  TODO: Buttons for hit, stand, new round
        self.BottomButtonContainer = QWidget(self.bottomContainer)
        self.hitButton = QPushButton("Hit")
        self.setObjectName("hitButton")
        self.hitButton.clicked.connect(lambda : self.on_hit())

        self.standButton = QPushButton("Stand")
        self.setObjectName("standButton")
        self.standButton.clicked.connect(lambda : self.on_stand())

        self.NewRoundButton = QPushButton("New Round")
        self.NewRoundButton.setObjectName("NewRoundButton")
        self.NewRoundButton.clicked.connect(lambda :self.StartRound())
        bottomLayout = QVBoxLayout()
        self.BottomButtonContainer.setLayout(bottomLayout)
        bottomLayout.addStretch()
        self.buttonLayout = QHBoxLayout()
        bottomLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.hitButton)
        self.buttonLayout.addWidget(self.standButton)
        self.buttonLayout.addWidget(self.NewRoundButton)
        self.buttonLayout.addStretch()
        #  TODO: Feedback

        #  TODO: Add widgets to layout

        #  TODO: Trigger a new layout with a new round
        self.background.setPixmap(self.backgroundPixmap)
        self.background.lower()
        self.animationOverlayContainer.raise_()
        self.audioPlayer.play()
        self.ShowCurrentTrack()
        self.StartRound()

    def loadAssets(self):
        for i in range(0,len(self.chipsValue)):
            self.chips.append(QPixmap("./assets/chips/Flat/sprite_" + str(i) + ".png").scaled(64,64))
            self.isometricChips.append(QPixmap("./assets/chips/Isometric/sprite_" + str(i) + ".png"))

        for suit in self.game.suits:
            for rank in self.game.ranks:
                pixmap = QPixmap("./assets/cards/fronts/" + rank + suit + "_card.png").scaled(88,124)
                self.cards.append(pixmap)
        self.cardBack = QPixmap("./assets/cards/backs/Flat/Card_Back.png")
        self.deckAsset = QPixmap("./assets/cards/backs/Flat/Card_DeckA-88x140.png").scaled(88, 140)
        audioSources =["./assets/sounds/All That Jazz.mp3"]
        trackNames = ["All That Jazz"]
        self.audioPlayer= AudioPlayer(audioSources,trackNames,self.mainContainer)
        self.InfoBar = QPixmap("./assets/UI elements/bar.png").scaled(200,5)
        soundEffects = ["./assets/sounds/card-draw-sound.mp3","./assets/sounds/flipcard.mp3","./assets/sounds/single_poker_chip.mp3","./assets/sounds/allin.mp3"]
        trackNames = ["draw","flip","single_chip","allin"]
        self.soundEffectPlayer = AudioPlayer(soundEffects,trackNames,self.mainContainer)

        self.backgroundPixmap = QPixmap("./assets/UI elements/background.jpg")

    """fix for self.bottomContainer.contentsRect() returning incorrect values"""
    def showEvent(self, event):
        super().showEvent(event)
        self.playerCardsContainer.setGeometry(
            self.bottomContainer.contentsRect()
        )
        self.dealerCardsContainer.setGeometry(self.topContainer.contentsRect())
        self.background.setGeometry(self.mainContainer.contentsRect())
        self.BottomButtonContainer.setGeometry(
            self.bottomContainer.width() // 3, 0,
            self.bottomContainer.width() // 3, self.bottomContainer.height()
        )


    """Resize overlays"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background"):
            self.background.setGeometry(self.mainContainer.contentsRect())
        if hasattr(self, 'animationOverlayContainer'):
            self.animationOverlayContainer.setGeometry(self.mainContainer.rect())
        if hasattr(self, 'cardToDraw'):
            self.cardToDraw.setGeometry(self.DrawCardStartGeometry())
        if hasattr(self, 'playerCardsContainer'):
            self.playerCardsContainer.setGeometry(self.bottomContainer.contentsRect())
        if hasattr(self, 'dealerCardsContainer'):
            self.dealerCardsContainer.setGeometry(self.topContainer.contentsRect())
        if hasattr(self, 'mediaInfoBar') and hasattr(self, 'mediaInfoBarContainer'):
            self.mediaInfoBar.setGeometry(
                self.mediaInfoBarContainer.geometry().x(),
                self.mediaInfoBarContainer.geometry().y()+10,
                self.mediaInfoBarContainer.size().width(),
                self.mediaInfoBarContainer.size().height()
            )
        if hasattr(self, 'BottomButtonContainer'):
            self.BottomButtonContainer.setGeometry(
                self.bottomContainer.width()//3,0,
                self.bottomContainer.width()//3, self.bottomContainer.height()
            )
    # BUTTON ACTIONS

    def StartRound(self):
        self.game.new_round()
        self.ClearChips()
        self.playerCards = 0
        self.dealerCards=0
        self.clear_layout(self.playerCardsLayout)
        self.game.player_hand = ["A♠", "A♥"]
        self.game.dealer_hand = ["A♦", "A♣"]
        for card in self.game.player_hand:
            self.CardDrawAnimation(card, True, True)
        self.update_dealer_cards()
    def CardDrawAnimation(self,cardToDraw, isPlayerDrawing, reveal=True):
        self.soundEffectPlayer.playAt(0)
        animatedCard = QLabel(self.animationOverlayContainer)
        animatedCard.setPixmap(self.cardBack)
        animatedCard.setGeometry(self.DrawCardStartGeometry())
        animatedCard.show()
        startPosition = animatedCard.geometry()

        cardDrawAnimation = QPropertyAnimation(animatedCard, b"geometry")
        cardDrawAnimation.setStartValue(startPosition)
        if isPlayerDrawing:
            print(self.playerCards)
            cardsInHand = self.playerCards
            self.playerCards+=1
            endPosition = QRect(
                int(self.width() // 2 - animatedCard.width() // 2* cardsInHand + (animatedCard.width() + 3) * cardsInHand),
                self.height()//2+9,
                animatedCard.width(),
                animatedCard.height())
            cardDrawAnimation.setEndValue(endPosition)
        else:
            cardsInHand = self.dealerCards
            self.dealerCards+=1
            endPosition = QRect(
                int(self.width() // 2 - animatedCard.width() // 2 * cardsInHand + (
                            animatedCard.width() + 3) * cardsInHand),
                int(self.height()//2-animatedCard.height()-18),
                animatedCard.width(),
                animatedCard.height())
            cardDrawAnimation.setEndValue(endPosition)

        cardDrawAnimation.setDuration(1000)
        cardDrawAnimation.setEasingCurve(QEasingCurve.Type.InOutExpo)
        cardDrawAnimation.finished.connect(lambda : self.ResetDeck(cardDrawAnimation,isPlayerDrawing,cardToDraw,endPosition,animatedCard,reveal) )
        self.activeAnimations.append(cardDrawAnimation)
        cardDrawAnimation.start()

    def CardRevealAnimation(self, layout,card, positionGeometry):
        TempCard = FlippableCard(self.cardBack, self.CardToPixmap(card),self.animationOverlayContainer)
        TempCard.setGeometry(positionGeometry)
        TempCard.show()
        FlipAnimation = QPropertyAnimation(TempCard, b"flip")
        FlipAnimation.setDuration(500)
        FlipAnimation.setStartValue(0.0)
        FlipAnimation.setEndValue(1.0)
        FlipAnimation.finished.connect(lambda : self.onAnimationFinished(FlipAnimation,layout,card,TempCard))
        self.activeAnimations.append(FlipAnimation)
        FlipAnimation.start()

    def onAnimationFinished(self,animation,layout,card,TempCard):
        animation.deleteLater()
        self.activeAnimations.remove(animation)
        self.add_card(layout, card)
        TempCard.deleteLater()

    def DrawCardStartGeometry(self):
        return QRect(self.width()-(88+10),0+10,88,124)
    def ResetDeck(self,animation,IsPlayerDrawing,card, endGeometry,animatedCard, reveal):
        animation.deleteLater()
        self.activeAnimations.remove(animation)
        animatedCard.deleteLater()
        if IsPlayerDrawing:
            layout = self.playerCardsLayout
        else:
            layout = self.dealerCardsLayout
        if reveal:
            self.CardRevealAnimation(layout, card,endGeometry )
        else:
            self.add_card(layout,card)

    def CardToPixmap(self, card):
        if card =="??":
            return self.cardBack
        suit = card[-1]
        rank = card[:-1]
        suitIndex = self.game.suits.index(suit)
        rankIndex = self.game.ranks.index(rank)
        cardIndex = 13* suitIndex + rankIndex
        return self.cards[cardIndex]

    def on_hit(self):
        # Player takes a card
        #card = self.game.player_hit()
        card = "10♠"
        self.CardDrawAnimation(card, True)

        """if self.game.player_total() > 21:
          # TODO: what should happen if a player goes over 21? Remove pass when complete
          pass"""

    def on_stand(self):
        #self.game.player_stand()
        self.ShowDealerCard()


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
        if card == "??":
            self.hiddenCard = NewCardLabel
        layout.addWidget(NewCardLabel)
        NewCardLabel.show()

    def update_dealer_cards(self, full=False):
        self.clear_layout(self.dealerCardsLayout)
        self.dealerCards = 0
        self.dealerFaceDownCard = None

        for i, card in enumerate(self.game.dealer_hand):
            if i == 1 and not full:
                self.dealerFaceDownCard = card
                self.CardDrawAnimation("??", False, False)
            else:
                self.CardDrawAnimation(card, False, True)

        # TODO: update relevant labels in response to dealer actions. Remove pass when complete
        if full:
            pass
        else:
            pass
    def ShowDealerCard(self):
        if self.dealerFaceDownCard == "":
            return
        self.soundEffectPlayer.playAt(1)
        cardGeometry = self.DrawCardStartGeometry()
        geometry = QRect(
            int(self.width() // 2 - cardGeometry.width() // 2 * 0 + (
                    cardGeometry.width() + 3) * 0),
            int(self.dealerCardsContainer.geometry().y() + self.dealerCardsContainer.height() - (124 + 5)),
            cardGeometry.width(),
            cardGeometry.height())
        self.CardRevealAnimation(self.dealerCardsLayout, self.dealerFaceDownCard,geometry)
        self.hiddenCard.deleteLater()
        self.dealerFaceDownCard = ""


    def new_round_setup(self):
        for chipType in self.playedChips:
            for chip in chipType:
                chip.deleteLater()
        # TODO: Prepare a fresh visual layout

        # TODO: update relevant labels (reset dealer and player totals)

        # TODO: display new cards for dealers and players

        # TODO: enable buttons for Stand and Hit - Remove pass when complete
        pass


    def end_round(self):
        # TODO: Disable button actions after the round ends. Remove pass when complete
        pass

    def NextTrack(self,status):
        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return
        if self.audioPlayer.selected<self.audioPlayer.sounds:
            self.audioPlayer.selected+=1
        else:
            self.audioPlayer.selected=0
        self.audioPlayer.SelectTrack(self.audioPlayer.selected)
        self.audioPlayer.play()

    def ShowCurrentTrack(self,fold=True):

        self.currentTrackLabel.setText("Currently Playing: " + self.audioPlayer.CurrentTrack())
        self.InfoBarAnimation = QPropertyAnimation(self.mediaInfoBarContainer, b"geometry")
        if fold:
            self.InfoBarAnimation.setStartValue(QRect(0, 0, 0, 40))
            self.InfoBarAnimation.setEndValue(QRect(0, 0, 200, 40))
        else:
            self.InfoBarAnimation.setStartValue(QRect(0, 0, 200, 40))
            self.InfoBarAnimation.setEndValue(QRect(0, 0, 0, 40))
        self.InfoBarAnimation.setDuration(1000)
        self.InfoBarAnimation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.InfoBarAnimation.valueChanged.connect(
            lambda: self.mediaInfoBar.setGeometry(0, 10, self.mediaInfoBarContainer.width(), 40)
        )
        if fold:
            self.InfoBarAnimation.finished.connect(
                lambda: QTimer.singleShot(2000, lambda: self.ShowCurrentTrack(False))
            )
        self.InfoBarAnimation.start()
    def PlayChip(self, chipIndex):
        Newchip = QLabel(self.chipsContainer)
        Newchip.setGeometry(32*chipIndex, 0,64,64)
        Newchip.setPixmap(self.chips[chipIndex])
        Newchip.show()
        offset = 10*len(self.playedChips[chipIndex])
        self.playedChips[chipIndex].append(Newchip)
        animation = QPropertyAnimation(Newchip, b"geometry")
        animation.setDuration(500)
        if chipIndex %2== 0:
            targetHeight= self.chipsContainer.height()//2-offset
        else:
            targetHeight= self.chipsContainer.height()//2+32-offset
        for i in range(0,len(self.playedChips)):
            if i %2 !=0:
                for chip in self.playedChips[i]:
                    chip.raise_()
        animation.setStartValue(QRect(32*chipIndex, 0, 64, 64))
        animation.setEndValue(QRect(32 * chipIndex, targetHeight,64,64))
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.finished.connect(lambda : animation.deleteLater())
        self.activeAnimations.append(animation)
        animation.start()
    def AllIn(self,betAmount):
        for i in range (len(self.chipsValue)-1,-1,-1):
            while betAmount > self.chipsValue[i]:
                betAmount -= self.chipsValue[i]
                self.PlayChip(i)
        while (betAmount > 0):
            betAmount -= self.chipsValue[0]
            self.PlayChip(0)
    def Bet(self, t):
        if t> self.playerMoney:
            return
        if t==-1:
            self.soundEffectPlayer.playAt(3)
            betAmount = self.playerMoney
            self.AllIn(betAmount)
        else:
            self.soundEffectPlayer.playAt(2)
            betAmount = self.chipsValue[t]
            self.PlayChip(t)
        self.playerMoney -= betAmount

    def ClearChips(self):
        for chipType in self.playedChips:
            for chip in chipType:
                chip.deleteLater()


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
