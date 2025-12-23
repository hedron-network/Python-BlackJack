# Python-BlackJack

## Intent
This is a solo blackjack simulation written with the PyQt6 python library with basic dealer behavior.

## Scope
The user has to be able to "hit" or "stand", and the dealer will choose to hit until they have a 17 or higher total.
The app will have detailed animations for drawing and flipping cards, eventually an idle animation for the dealer.

## Goal
The final goal of the application is to provide an intuitive and professional looking interface for playing the game of blackjack.

---

## RoadMap / Progress
- V1 completed

---

**File Structure:**
```
Python-Blackjack/
├─ code/
|  ├─ main.py
|  ├─ custom-widgets.py
|  ├─ game_logic.py
|  ├─ QSS_blackjack.qss
│  ├─ assets/
│  │  ├─ asset_attribution
│  │  ├─ UI elements/..
│  │  ├─ cards/
│  │  |  ├─ backs/
│  │  |  |  ├─ Flat/..
│  │  |  |  └─ Isometric/..
│  │  |  └─ fronts/
│  │  ├─ chips/
│  │  |  ├─ Flat/..
│  │  |  └─ Isometric/..
│  │  └─ sounds/..
├─ README.md
├─ CODEOWNERS
└─ .gitignore
```
## Game Rules (21/Blackjack)

1. **Objective:** Get a hand value as close to 21 as possible without going over
2. **Card Values:**
   - Number cards (2-10): Face value
   - Face cards (J, Q, K): 10 points
   - Ace: 1 or 11 (whichever benefits the hand)
3. **Gameplay:**
   - Player and dealer each receive 2 cards
   - Player can "Hit" (draw card) or "Stand" (end turn)
   - Dealer reveals hidden card and hits until 17+
4. **Winning:** Highest hand ≤21 wins; ties are a "push"

---

## Credits & Attribution
UI & sound design: @hedron-network,  
game logic & custom track: @Hugomlr

### Asset Attributions:
#### Sprites:
- chips & card backs : https://screamingbrainstudios.itch.io/poker-pack
- cards front : https://kerenel.itch.io/pixelart-cards
- icons : https://www.flaticon.com
- impact bubble : https://www.freepik.com/free-psd/cartoon-comic-explosion-illustration_158196534.htm
- blackjack logo : https://www.pinterest.com/pin/blackjack-logo-on-white-background--80783387061327446/
- background : https://www.vecteezy.com/vector-art/24232274-green-casino-poker-table-texture-game-background
- button background: https://www.freepik.com/free-photo/walnut-wood-textured-background-design_18835110.htm#fromView=keyword&page=2&position=22&uuid=89604344-ab81-4897-8f85-7438b8b8b3a0&query=Dark+pine+wood+texture
#### Sound Effects
- card draw sound effect: https://pixabay.com/sound-effects/card-sounds-35956/
- card flip sound effect: https://pixabay.com/sound-effects/flipcard-91468/
- single chip : https://pixabay.com/sound-effects/poker-chips1-87592/
- allin : https://pixabay.com/sound-effects/allinpushchips-96121/
- error bet : https://pixabay.com/sound-effects/casual-click-pop-ui-10-262126/
