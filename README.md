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

### Phase 1: Core Game Logic
- [x] **Deck Mechanics** - Create and shuffle a standard 52-card deck
- [x] **Card Distribution** - Deal 2 cards to player (face up) and dealer (1 up, 1 down)
- [x] **Scoring System** - Calculate hand values correctly
- [x] **Ace Handling** - Implement dynamic Ace value (1 or 11) based on hand optimization
- [x] **Dealer Functionality** - Dealer hits on < 17, stands on ≥ 17
- [x] **Win Condition Logic** - Determine winner, handle push (tie), detect bust

### Phase 2: Required UI Features
- [x] **Responsive Window Design** - Layout reflows sensibly when resized
- [x] **Player Hand Display** - Show cards and current total clearly
- [x] **Dealer Hand Display** - Show cards with face-down card until reveal, display total
- [x] **Control Buttons** - Hit, Stand, and New Round buttons
- [x] **Scoreboard** - Display player and dealer hand totals prominently
- [x] **Visual Feedback** - Clear win/lose/push indication at round end
- [x] **Card Images** - Use graphical card images 

### Phase 3: Design & Accessibility
- [x] **External Stylesheet** - Separate QSS file for styling
- [x] **Images & Icons** - Integrate card images and UI icons
- [x] **Accessibility Features** - Large fonts, high contrast, clear labeling
- [x] **Turn Indicator** - Clear display of whose turn it is

### Phase 4: Additional Feature

**Options Under Consideration:**
- [x] **Statistics Tracker** - Track wins/losses/pushes across sessions
- [x] **Settings Panel** - Adjust font size, contrast, animation speed

### Phase 5: Animations & Polish
- [x] **Card Draw Animation** - Smooth card dealing animation
- [x] **Card Flip Animation** - Reveal dealer's face-down card with flip effect
- [x] **Chip Animations** - Chips animation for betting feedback
- [x] **Smooth Transitions** - Polish all state changes with subtle animations

### Phase 6: Documentation
- [x] **Code Comments** - Complete inline documentation for all methods and logic
- [ ] **UI Design Document** - Comprehensive design justification document including:
  - Layout choices and widget selection
  - Interaction flow diagrams
  - Color and font decisions
  - Accessibility considerations
  - Screenshots with annotations
  - References to Nielsen's 10 Heuristics and Gestalt Principles
  - Third-party asset credits
- [ ] **Video Demo** - 5-6 minute recorded demonstration with:
  - All team members presenting (cameras on)
  - Code walkthrough
  - Feature demonstration
  - Explanation of design decisions

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
