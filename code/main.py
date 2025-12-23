
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QApplication,QMessageBox, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGridLayout
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QTimer
import sys

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21
from custom_widgets import AudioPlayer, FlippableCard, QLabel_clickable, Settings, Help,Statistic, MainMenu


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.canStartNewRound = True
        self.canActivateButtons = True
        self.betAmount = 0
        self.canBet=True
        self.muted = False
        self.playerMoney = 1_000
        self.hiddenCard = None
        self.setWindowTitle("Game of 21")

        # set the windows dimensions
        self.baseContainer = QWidget()
        self.setGeometry(100, 50, 1000, 700)
        self.mainContainer = QWidget(self.baseContainer)
        self.mainContainer.setObjectName("mainContainer")
        self.mainContainer.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.baseContainer)

        #region Asset Loading
        self.game = Game21()
        self.MainMenu = None
        self.logo = None
        self.QuitToMenuIcon= None
        self.settingsIcon = None
        self.settingsDialog= None
        self.helpIcon = None
        self.helpDialog = None
        self.statsIcon = None
        self.statsDialog = None
        self.soundButtonStates=[]
        self.chips = []
        self.isometricChips = []
        self.chipsValue = [5,10,25,50,100,500]
        self.cards = []
        self.cardBack = None
        self.deckAsset = None
        self.audioPlayer = None
        self.InfoBar = None
        self.soundEffectPlayer = None
        self.loadAssets()
        if len(self.cards) == 0 or self.cardBack is None or self.deckAsset is None:
            print("Error Loading Cards Assets")
        #endregion
        self.initUI()


    def initUI(self):
        #region Container Setup
        

        self.background = QLabel(self.mainContainer)
        self.background.setObjectName("background")
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

        #region Feedback
        self.feedBackLabel = QLabel(self.animationOverlayContainer)
        self.feedBackLabel.setObjectName("feedbackLabel")
        pixmap = QPixmap("./assets/UI elements/impact_bubble.png")
        self.feedBackLabel.setPixmap(pixmap)
        self.feedBackLabel.setScaledContents(True)
        self.feedBackLabel.setGeometry(self.width()//2,self.height()//2,0,0)
        self.feedBackText = QLabel(self.animationOverlayContainer)
        self.feedBackText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedBackText.setGeometry(
            0,
            self.height() // 4,
            self.width(),
            self.height() // 2
        )
        self.feedBackText.setObjectName("feedbackText")


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
        self.mediaInfoBarContainer.setGeometry(0, 64, 0, 40)  # Start with 0 width
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

        #region PlayerInformation
        self.PlayerInformationContainer = QWidget(self.topContainer)
        self.PlayerInformationContainer.setObjectName("PlayerInformationContainer")
        mainPlayerInfoLayout = QVBoxLayout()
        self.PlayerInformationContainer.setLayout(mainPlayerInfoLayout)
        self.moneyLayer = QHBoxLayout()
        self.moneyLayer.addStretch()
        staticMoneyLabel = QLabel("Money :")
        staticMoneyLabel.setObjectName("staticInfoLabel")
        self.moneyLayer.addWidget(staticMoneyLabel)
        self.CurrentMoneyLabel = QLabel("0")
        self.CurrentMoneyLabel.setObjectName("CurrentMoneyLabel")
        self.moneyLayer.addWidget(self.CurrentMoneyLabel)
        self.moneyLayer.addStretch()
        mainPlayerInfoLayout.addLayout(self.moneyLayer)

        self.betInfoLayer = QHBoxLayout()
        self.betInfoLayer.addStretch()
        staticBetLabel = QLabel("Bet:")
        staticBetLabel.setObjectName("staticInfoLabel")
        self.betInfoLayer.addWidget(staticBetLabel)
        self.CurrentBetLabel = QLabel("0")
        self.CurrentBetLabel.setObjectName("CurrentBetLabel")
        self.betInfoLayer.addWidget(self.CurrentBetLabel)
        self.betInfoLayer.addStretch()
        mainPlayerInfoLayout.addLayout(self.betInfoLayer)
        mainPlayerInfoLayout.addStretch()
        #endregion

        #region Betting
        self.bottomRightContainerLayout = QHBoxLayout()
        self.bottomRightContainerLayout.addStretch(4)
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
        self.ConfirmBetButton = QPushButton("Confirm Bet")
        self.ConfirmBetButton.clicked.connect(lambda : self.confirmBet())
        self.bettingLayout.addWidget(self.ConfirmBetButton)
        self.bettingLayout.addStretch()
        # endregion

        #region MuteButton
        soundButtonLayout = QHBoxLayout()
        soundButtonLayout.addStretch()
        self.soundButton = QLabel_clickable()
        self.soundButton.setObjectName("soundButton")
        self.soundButton.setPixmap(self.soundButtonStates[0])
        self.soundButton.clicked.connect(lambda : self.Mute())
        soundButtonLayout.addWidget(self.soundButton)
        self.bettingLayout.addLayout(soundButtonLayout)
        #endregion

        #region Settings Button
        self.topLeftContainerLayout = QVBoxLayout()
        self.topLeftContainer.setLayout(self.topLeftContainerLayout)
        self.SettingsLayout= QHBoxLayout()
        self.QuitButton = QLabel_clickable()
        self.QuitButton.setObjectName("quitButton")
        self.QuitButton.setPixmap(self.QuitToMenuIcon)
        self.QuitButton.clicked.connect(lambda : self.OpenMainMenu())
        self.SettingsLayout.addWidget(self.QuitButton)
        self.SettingsButton = QLabel_clickable()
        self.SettingsButton.setObjectName("settingsButton")
        self.SettingsButton.setPixmap(self.settingsIcon)
        self.SettingsButton.clicked.connect(lambda : self.OpenSettings())
        self.SettingsLayout.addWidget(self.SettingsButton)
        self.HelpButton = QLabel_clickable()
        self.HelpButton.setObjectName("helpButton")
        self.HelpButton.setPixmap(self.helpIcon)
        self.HelpButton.clicked.connect(lambda :self.OpenHelp())
        self.SettingsLayout.addWidget(self.HelpButton)
        self.StatsButton = QLabel_clickable()
        self.StatsButton.setObjectName("statsButton")
        self.StatsButton.setPixmap(self.statsIcon)
        self.StatsButton.clicked.connect(lambda: self.OpenStats())
        self.SettingsLayout.addWidget(self.StatsButton)

        self.SettingsLayout.addStretch()
        self.topLeftContainerLayout.addLayout(self.SettingsLayout)
        self.topLeftContainerLayout.addStretch()
        #endregion

        #region Chips
        self.bottomLeftContainerLayout = QVBoxLayout()
        self.bottomLeftContainer.setLayout(self.bottomLeftContainerLayout)
        self.chipsContainer = QWidget()
        self.chipsContainer.setFixedWidth(4*64)
        self.bottomLeftContainerLayout.addWidget(self.chipsContainer)
        self.playedChips= []
        for i in range(0,len(self.chips)):
            self.playedChips.append([])

        self.removeChipsButton = QPushButton("Remove Chips")
        self.removeChipsButton.clicked.connect(lambda :self.removeChips())
        self.removeChipsButton.setMaximumWidth(200)
        self.removeChipsButton.hide()
        self.bottomLeftContainerLayout.addWidget(self.removeChipsButton)
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

        #region Totals
        self.playerTotalContainer = QWidget(self.mainContainer)
        self.playerTotalContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.playerTotalContainer.setLayout(QVBoxLayout())
        self.playerTotalLabel = QLabel("Total :")

        self.playerTotalContainer.layout().addWidget(self.playerTotalLabel)

        self.dealerTotalContainer = QWidget(self.mainContainer)
        self.dealerTotalContainer.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.dealerTotalContainer.setLayout(QVBoxLayout())
        self.dealerTotalLabel = QLabel("Total :")
        self.dealerTotalContainer.layout().addWidget(self.dealerTotalLabel)
        #endregion

        self.dealerCards =0
        self.playerCards = 0
        #region Buttons
        self.BottomButtonContainer = QWidget(self.bottomContainer)
        self.hitButton = QPushButton("Hit")
        self.setObjectName("hitButton")
        self.hitButton.clicked.connect(lambda : self.on_hit())

        self.standButton = QPushButton("Stand")
        self.setObjectName("standButton")
        self.standButton.clicked.connect(lambda : self.on_stand())

        bottomLayout = QVBoxLayout()
        self.BottomButtonContainer.setLayout(bottomLayout)
        bottomLayout.addStretch()
        self.buttonLayout = QHBoxLayout()
        bottomLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.hitButton)
        self.buttonLayout.addWidget(self.standButton)
        self.buttonLayout.addStretch()
        #endregion
        #region Main Menu
        self.isMainMenuOpen = False
        self.MainMenu.play.connect(lambda : self.OpenMainMenu())
        self.MainMenu.resetMoney.connect(lambda : self.ResetMoney())
        self.MainMenu.close.connect(lambda : self.close())
        self.MainMenu.settings.connect(lambda : self.OpenSettings())
        #endregion


        self.animationOverlayContainer.raise_()
        self.audioPlayer.play()
        self.ShowCurrentTrack()
        self.on_new_round()
#region Initial Setup
    """
    Loads the predefined Assets into the app
    returns void
    """
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
        audioSources =["./assets/sounds/la valse d'hugo.mp3","./assets/sounds/All That Jazz.mp3"]
        trackNames = ["la valse d'hugo","All That Jazz"]
        self.audioPlayer= AudioPlayer(audioSources,trackNames,self.mainContainer)
        self.InfoBar = QPixmap("./assets/UI elements/bar.png").scaled(200,5)
        soundEffects = ["./assets/sounds/card-draw-sound.mp3","./assets/sounds/flipcard.mp3","./assets/sounds/single_poker_chip.mp3","./assets/sounds/allin.mp3","./assets/sounds/error-bet.mp3"]
        soundNames = ["draw","flip","single_chip","allin","error-bet"]
        self.soundEffectPlayer = AudioPlayer(soundEffects,soundNames,self.mainContainer)
        self.soundButtonStates= [
            QPixmap("./assets/UI elements/speaker.png"),
            QPixmap("./assets/UI elements/mute.png")
        ]
        self.settingsIcon = QPixmap("./assets/UI elements/settings.png")
        self.settingsDialog = Settings(self.settingsIcon,self.audioPlayer,self.soundEffectPlayer,trackNames,self.mainContainer)
        self.helpIcon = QPixmap("./assets/UI elements/info.png")
        self.helpDialog = Help(self.helpIcon,self.mainContainer)
        self.statsIcon = QPixmap("./assets/UI elements/stats.png")
        self.statsDialog = Statistic(self.statsIcon, self.game, self.mainContainer)

        self.logo = QPixmap("./assets/UI elements/blackjack.png").scaled(300,300)
        self.QuitToMenuIcon = QPixmap("./assets/UI elements/logout.png")
        self.MainMenu = MainMenu(self.logo,self.baseContainer)

    """
    fix for contentsRect() returning incorrect values
    is triggered after the UI is fully loaded
    """
    def showEvent(self, event):
        super().showEvent(event)
        self.UpdateGeometry()
        self.OpenMainMenu()


    """
    Triggered when resizing occurs
    Resize all of the outside layouts containers
    """
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.UpdateGeometry()
    """
    Helper function to update the geometry of all of the main containers
    returns void
    """
    def UpdateGeometry(self):
        if hasattr(self, 'mainContainer'):
            self.mainContainer.setGeometry(self.baseContainer.contentsRect())
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
        if hasattr(self, 'playerTotalContainer'):
            self.playerTotalContainer.setGeometry(
                self.width() // 2 - self.playerTotalLabel.width()//4, self.height() // 2 + 100, 200, 100
            )
        if hasattr(self, 'dealerTotalContainer'):
            self.dealerTotalContainer.setGeometry(
                self.width() // 2 - self.playerTotalLabel.width() // 4, self.height() // 2 - 200, 200, 100
            )
        if hasattr(self, 'PlayerInformationContainer'):
            self.PlayerInformationContainer.setGeometry(self.width() // 4, 0, self.topContainer.width() // 2,
                                                        self.topContainer.height() // 2)
        if hasattr(self, 'feedBackText'):
            self.feedBackText.setGeometry(
                0,
                self.height() // 4,
                self.width(),
                self.height() // 2
            )
        if hasattr(self, 'MainMenu'):
            self.MainMenu.updateGeometry()
#endregion
#region Round Management
    """
    Handler for setting up a new round
    returns void
    """
    def new_round_setup(self):
        self.canActivateButtons = False
        self.DeleteChips()
        self.betAmount = 0
        self.CurrentMoneyLabel.setText(str(self.playerMoney))
        self.CurrentBetLabel.setText(str(self.betAmount))
        self.playerTotalLabel.setText("Total : "+ str(0))
        self.dealerTotalLabel.setText("Total : " + str(0))
        self.playerCards = 0
        self.dealerCards = 0
        self.clear_layout(self.playerCardsLayout)
        self.clear_layout(self.dealerCardsLayout)

        self.canBet = True

        self.canActivateButtons = True
        self.canStartNewRound = True
    """
    Handles the initial card draw animations
    returns void
    """
    def DrawInitialCards(self):
        for card in self.game.player_hand:
            self.CardDrawAnimation(card, True, True)
        self.update_dealer_cards()
        QTimer.singleShot(1500, lambda: self.FinishCardDraw())
    def FinishCardDraw(self):
        self.setPlayerTotal()
        self.canActivateButtons = True

    #endregion
#region Animation Handlers
    """
    Sets the font size of the feedback text
    args
        float size -> The new font size
        string res -> The text to display
    returns void
    """
    def setFeedbackFontSize(self, size,res):
        font = self.feedBackText.font()
        font.setPointSizeF(size)
        self.feedBackText.setFont(font)
        self.feedBackText.setProperty("_fontSize", size)
        self.feedBackText.setText(res)


    """
    Handles the feedback animation
    args
        string res -> The text to display
        bool out -> Whether the animation is playing in or out
    returns void
    """
    def FeedbackAnimation(self,res,out =True):
        self.feedBackAnim = QPropertyAnimation(self.feedBackLabel,b"geometry")
        self.feedBackAnim.setDuration(1000)

        self.textAnim = QPropertyAnimation(self.feedBackText, b"_fontSize")
        self.textAnim.setDuration(1000)

        
        start= QRect(
                self.width()//2, self.height()//2,
                0,0)
        end =QRect(
                self.width()//4, self.height()//4,
                self.width()//2, self.height()//2
            )
        if out:
            self.feedBackAnim.setStartValue(start)
            self.textAnim.setStartValue(8)
            self.feedBackAnim.setEndValue(end)
            self.textAnim.setEndValue(70)
            self.feedBackAnim.setEasingCurve(QEasingCurve.Type.OutElastic)
            self.textAnim.setEasingCurve(QEasingCurve.Type.OutElastic)
        else:
            self.feedBackAnim.setStartValue(end)
            self.textAnim.setStartValue(70)
            self.feedBackAnim.setEndValue(start)
            self.textAnim.setEndValue(8)
            self.feedBackAnim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.textAnim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.textAnim.valueChanged.connect(
            lambda v: self.setFeedbackFontSize(v,res)
        )


        self.feedBackAnim.start()
        self.textAnim.start()

        if out:
            QTimer.singleShot(1500, lambda: self.FeedbackAnimation(res,False))
        if not out:
            self.feedBackAnim.finished.connect(
                lambda: self.feedBackText.hide()
            )

    """
    Handles the money counting animation
    args
        int end -> The target money value
        int duration -> The duration between each increment
    returns void
    """
    def MoneyAnimation(self,end,duration):
        self.canBet = False
        if self.playerMoney<end:
            if self.playerMoney+10 <= end:
                self.playerMoney+=10
            else:
                self.playerMoney+=1
            self.CurrentMoneyLabel.setText(str(self.playerMoney))
            QTimer.singleShot(duration, lambda: self.MoneyAnimation(end,duration))
        else:
            self.canBet = True
    """
    Handles the card draw animation
    args
        string cardToDraw -> The card to draw
        bool isPlayerDrawing -> Whether the card is being drawn by the player
        bool reveal -> Whether to reveal the card after drawing
    returns void
    """
    def CardDrawAnimation(self,cardToDraw, isPlayerDrawing, reveal=True):
        if not self.muted:
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
    """
    Handles the card reveal animation
    args
        layout -> The layout to add the card to
        string card -> The card to reveal
        QRect positionGeometry -> The geometry of where the card is revealed
    returns void
    """
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
    """
    Cleanup active animations when the card reveal animation is finished
    args
        QtAnimation animation -> The finished animation
        layout -> The layout to add the card to
        string card -> The card to add
        FlippableCard TempCard -> The temporary card to delete
    returns void
    """
    def onAnimationFinished(self,animation,layout,card,TempCard):
        animation.deleteLater()
        self.activeAnimations.remove(animation)
        self.add_card(layout, card)
        TempCard.deleteLater()

    """
    Handles the chip play animation
    args
        int chipIndex -> The index of the chip to play
    returns void
    """
    # MAX CHIP STACK = 17
    def PlayChip(self, chipIndex):
        Newchip = QLabel(self.chipsContainer)
        Newchip.setGeometry(32 * chipIndex, 0, 64, 64)
        Newchip.setPixmap(self.chips[chipIndex])
        Newchip.show()
        offset = 10 * len(self.playedChips[chipIndex])
        self.playedChips[chipIndex].append(Newchip)
        animation = QPropertyAnimation(Newchip, b"geometry")
        animation.setDuration(500)
        if chipIndex % 2 == 0:
            targetHeight = self.chipsContainer.height() // 2 - offset
        else:
            targetHeight = self.chipsContainer.height() // 2 + 32 - offset
        for i in range(0, len(self.playedChips)):
            if i % 2 != 0:
                for chip in self.playedChips[i]:
                    chip.raise_()
        animation.setStartValue(QRect(32 * chipIndex, 0, 64, 64))
        animation.setEndValue(QRect(32 * chipIndex, targetHeight, 64, 64))
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.finished.connect(lambda: animation.deleteLater())
        self.activeAnimations.append(animation)
        animation.start()

    """
    Handles the media info bar animation
    args
        bool fold -> Whether to fold or unfold the bar
    returns void
    """
    def ShowCurrentTrack(self, fold=True):

        self.currentTrackLabel.setText("Currently Playing: " + self.audioPlayer.CurrentTrack())
        self.InfoBarAnimation = QPropertyAnimation(self.mediaInfoBarContainer, b"geometry")
        if fold:
            self.InfoBarAnimation.setStartValue(QRect(0, 40, 0, 40))
            self.InfoBarAnimation.setEndValue(QRect(0, 40, 200, 40))
        else:
            self.InfoBarAnimation.setStartValue(QRect(0, 40, 200, 40))
            self.InfoBarAnimation.setEndValue(QRect(0, 40, 0, 40))
        self.InfoBarAnimation.setDuration(1000)
        self.InfoBarAnimation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.InfoBarAnimation.valueChanged.connect(
            lambda: self.mediaInfoBar.setGeometry(0, 10, self.mediaInfoBarContainer.width(), 40)
        )
        if fold:
            self.InfoBarAnimation.finished.connect(
                lambda: QTimer.singleShot(3000, lambda: self.ShowCurrentTrack(False))
            )
        self.InfoBarAnimation.start()

    """
    Resets the deck after an animation is finished
    args
        QtAnimation animation -> The animation
        bool IsPlayerDrawing -> True iof the player is drawing
        string card -> The card to add
        QRect endGeometry -> The end geometry of the card
        FlippableCard animatedCard -> The animated card to delete
        bool reveal -> Whether to reveal the card or not
    returns void
    """
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
    """
    Helper function to get the starting geometry of the drawn card
    returns 
        QRect -> The starting geometry of the drawn card
    """
    def DrawCardStartGeometry(self):
        return QRect(self.width()-(88+10),0+10,88,124)
    """
    Helper function to convert a card to its pixmap
    args
        string card -> The card to convert
    returns
        QPixmap -> The pixmap
    """
    def CardToPixmap(self, card):
        if card =="??":
            return self.cardBack
        suit = card[-1]
        rank = card[:-1]
        suitIndex = self.game.suits.index(suit)
        rankIndex = self.game.ranks.index(rank)
        cardIndex = 13* suitIndex + rankIndex
        return self.cards[cardIndex]
    """
    Handles revealing the dealer's hidden card
    returns void
    """
    def ShowDealerCard(self):
        if self.dealerFaceDownCard == "":
            return
        if not self.muted:
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
    """
    Handles the player feedback animation
    args
        string res -> The text to display
    returns void
    """
    def PlayerFeedback(self,res):
        self.feedBackText.show()
        self.setFeedbackFontSize(8,res)
        self.feedBackText.setText(res)
        self.FeedbackAnimation(res)
#endregion

#region GameLogic Interface
    """
    Handles the player hitting
    returns void
    """
    def on_hit(self):
        if self.canBet or not self.canActivateButtons:
            self.soundEffectPlayer.stop()
            self.soundEffectPlayer.playAt(4)
            return
        self.canActivateButtons=False
        # Player takes a card
        card = self.game.draw_card()
        self.game.player_hand.append(card)
        score = self.game.player_total()
        print("Score: " + str(score))
        self.playerTotalLabel.setText("Total : "+ str(score))
        self.CardDrawAnimation(card, True)

        if self.game.player_total() > 21:
            QTimer.singleShot(3000,lambda :self.end_round())
        else:
            self.canActivateButtons=True

    """
    Handles the player standing
    returns void
    """
    def on_stand(self):
        if self.canBet or not self.canActivateButtons:
            self.soundEffectPlayer.stop()
            self.soundEffectPlayer.playAt(4)
            return
        self.canActivateButtons= False
        self.ShowDealerCard()
        self.dealerTotalLabel.setText("Total : " + str(self.game.dealer_total()))
        self.DealerTurn()

    """
    Handles the new round setup
    returns void
    """
    def on_new_round(self):
        if not self.canStartNewRound:
            return
        self.canStartNewRound = False
        self.game.new_round()
        self.new_round_setup()
    """
    Handles the dealer's initial draws
    returns void
    """
    def update_dealer_cards(self, full=False):
        self.dealerCards = 0
        self.dealerFaceDownCard = None

        for i, card in enumerate(self.game.dealer_hand):
            if i == 1 and not full:
                self.dealerFaceDownCard = card
                self.CardDrawAnimation("??", False, False)
            else:
                self.CardDrawAnimation(card, False, True)
                self.dealerTotalLabel.setText("Total : "+str(self.game.card_value(card)))
    """
    Handles the end of round logic
    returns void
    """
    def end_round(self):
        res = self.game.decide_winner()
        print(res)
        self.PlayerFeedback(res)
        money = self.playerMoney+self.game.resolve_bet(res)
        delta = money - self.playerMoney
        if delta>0:
            animtime = 2000//delta
            self.MoneyAnimation(money,animtime)

        self.on_new_round()
    """
    Handles going all
    args
        int betAmount -> The amount to bet
    returns void
    """
    def AllIn(self,betAmount):
        chips =[]
        for i in range (len(self.chipsValue)-1,-1,-1):
            while betAmount > self.chipsValue[i]:
                betAmount -= self.chipsValue[i]
                chips.append(i)
        while betAmount > 0:
            betAmount -= self.chipsValue[0]
            chips.append(0)
        self.StaggeredChips(chips)
    def StaggeredChips(self,chips):
        if len(chips)>0:
            chip = chips.pop(0)
            self.PlayChip(chip)
            QTimer.singleShot(50, lambda :self.StaggeredChips(chips))
    """
    Handles betting
    args
        int t -> The type of chip to bet
    returns void
    """
    def Bet(self, t):
        if t> self.playerMoney or self.playerMoney ==0 or not self.canBet:
            self.soundEffectPlayer.stop()
            self.soundEffectPlayer.playAt(4)
            return
        if not self.removeChipsButton.isVisible():
            self.removeChipsButton.show()
        if t==-1 and self.playerMoney>0:
            if not self.muted:
                self.soundEffectPlayer.stop()
                self.soundEffectPlayer.playAt(3)
            betAmount = self.playerMoney
            self.AllIn(betAmount)
        else:
            if len(self.playedChips[t])>=15 or self.chipsValue[t]>self.playerMoney:
                self.soundEffectPlayer.stop()
                self.soundEffectPlayer.playAt(4)
                return
            if not self.muted and self.playerMoney>=t:
                self.soundEffectPlayer.stop()
                self.soundEffectPlayer.playAt(2)
            betAmount = self.chipsValue[t]
            self.PlayChip(t)
        self.playerMoney -= betAmount
        self.betAmount+= betAmount
        self.CurrentMoneyLabel.setText(str(self.playerMoney))
        self.CurrentBetLabel.setText(str(self.betAmount))
#endregion

    #region Helper
    """
    Toggles the main menu
    returns void
    """
    def OpenMainMenu(self):
        print("Toggling Main Menu", self.isMainMenuOpen)
        self.MainMenu.setGeometry(self.baseContainer.contentsRect())
        if self.isMainMenuOpen:
            self.MainMenu.hide()
            self.mainContainer.show()
            self.isMainMenuOpen = False
        else:
            self.MainMenu.show()
            self.mainContainer.hide()
            self.isMainMenuOpen = True
        self.UpdateGeometry()
    """
    Handles resetting the player's money
    returns void
    """
    def ResetMoney(self):
        if self.canBet:
            self.MainMenu.FeedbackLabel.setText("Money has been reset to $1000")
            QTimer.singleShot(1500, lambda: self.MainMenu.FeedbackLabel.setText(""))
            self.removeChips()
            self.playerMoney = 1000
            self.CurrentMoneyLabel.setText(str(self.playerMoney))
        else:
            self.MainMenu.FeedbackLabel.setText("Cannot reset money during a round")
            QTimer.singleShot(1500, lambda: self.MainMenu.FeedbackLabel.setText(""))

    """
    Update the player total label
    returns void
    """
    def setPlayerTotal(self):
        self.playerTotalLabel.setText("Total : "+ str(self.game.player_total()))
    """
    Update the dealer total label
    returns void
    """
    def setDealerTotal(self):
        self.dealerTotalLabel.setText("Total : " + str(self.game.dealer_total()))
    """
    Clears all widgets from a layout
    args
        layout -> The layout to clear
    returns void
    """
    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    """
    Handles adding a card to a layout
    args
        layout -> The layout to add the card to
        string card -> The card to add
    returns void
    """
    def add_card(self,layout, card):
        NewCardLabel = QLabel(self.animationOverlayContainer)
        NewCardLabel.setPixmap(self.CardToPixmap(card))
        NewCardLabel.setFixedSize(88,124)
        if card == "??":
            self.hiddenCard = NewCardLabel
        layout.addWidget(NewCardLabel)
        NewCardLabel.show()
    """
    Removes all played chips and refunds the player
    returns void
    """
    def removeChips(self):
        if not self.canBet:
            return
        self.canBet= False
        for i in range(0,len(self.playedChips)):
            for chip in self.playedChips[i]:
                chip.deleteLater()
                self.playerMoney+=self.chipsValue[i]
            self.playedChips[i] = []
        self.CurrentMoneyLabel.setText(str(self.playerMoney))
        self.betAmount=0
        self.CurrentBetLabel.setText(str(self.betAmount))
        self.removeChipsButton.hide()
        self.canBet=True
    """
    Handles deleting played chips
    returns void
    """
    def DeleteChips(self):
        for chipType in self.playedChips:
            for chip in chipType:
                chip.deleteLater()
        for i in range(0, len(self.playedChips)):
            self.playedChips[i] = []

    """
    Auto-plays the next track when the current one ends
    args
        QMediaPlayer.MediaStatus status -> The current media status
    returns void
    """
    def NextTrack(self,status):
        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return
        if self.audioPlayer.selected<len(self.audioPlayer.AllTracks())-1:
            self.audioPlayer.selected+=1
        else:
            self.audioPlayer.selected=0
        self.audioPlayer.SelectTrack(self.audioPlayer.selected)
        QTimer.singleShot(1500, lambda: self.PlayTrack())
    def PlayTrack(self):
        self.audioPlayer.play()
        self.ShowCurrentTrack()

    """
    Toggles muting the audio
    returns void
    """
    def Mute(self):
        if self.muted:
            self.soundButton.setPixmap(self.soundButtonStates[0])
            self.audioPlayer.play()
            self.ShowCurrentTrack()
        else:
            self.soundButton.setPixmap(self.soundButtonStates[1])
            self.audioPlayer.stop()
        self.muted = not self.muted

    """
    Opens the settings dialog
    returns void
    """
    def OpenSettings(self):
        self.settingsDialog.exec()

    """
    Handles the dealer's turn
    returns void
    """
    def DealerTurn(self):
        DoesDealerDraw = self.game.dealer_turn()
        self.setDealerTotal()
        if DoesDealerDraw:
            card = self.game.dealer_draw()
            self.CardDrawAnimation(card,False)
            QTimer.singleShot(1000, lambda : self.DealerTurn())
        else:
            QTimer.singleShot(3000, lambda : self.end_round())# time for animations to finish

    #endregion
    """
    Confirms the player's bet and starts the round
    returns void
    """
    def confirmBet(self):
        if self.canBet and self.canActivateButtons and self.betAmount >0:
            self.game.Bet(self.betAmount)
            self.canBet=False
            self.DrawInitialCards()
            self.removeChipsButton.hide()
        else:
            self.soundEffectPlayer.stop()
            self.soundEffectPlayer.playAt(4)
    """
    Opens the help dialog
    returns void
    """
    def OpenHelp(self):
        self.helpDialog.exec()
    """
    Opens the statistics dialog
    returns void
    """
    def OpenStats(self):
        self.statsDialog.refresh()
        self.statsDialog.exec()
    """
    Handles the close event
    returns void
    """
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Quit Application',
                                     "Are you sure you want to quit ?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    



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
