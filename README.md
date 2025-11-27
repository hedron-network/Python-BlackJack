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
- [ ] **Card Distribution** - Deal 2 cards to player (face up) and dealer (1 up, 1 down)
- [ ] **Scoring System** - Calculate hand values correctly
- [ ] **Ace Handling** - Implement dynamic Ace value (1 or 11) based on hand optimization
- [ ] **Dealer Functionality** - Dealer hits on < 17, stands on ≥ 17
- [ ] **Win Condition Logic** - Determine winner, handle push (tie), detect bust

### Phase 2: Required UI Features
- [ ] **Responsive Window Design** - Layout reflows sensibly when resized
- [ ] **Player Hand Display** - Show cards and current total clearly
- [ ] **Dealer Hand Display** - Show cards with face-down card until reveal, display total
- [ ] **Control Buttons** - Hit, Stand, and New Round buttons
- [ ] **Scoreboard** - Display player and dealer hand totals prominently
- [ ] **Visual Feedback** - Clear win/lose/push indication at round end
- [ ] **Card Images** - Use graphical card images (or clear text representations)

### Phase 3: Design & Accessibility
- [ ] **External Stylesheet** - Separate QSS file for styling
- [ ] **Images & Icons** - Integrate card images and UI icons
- [ ] **Accessibility Features** - Large fonts, high contrast, clear labeling
- [ ] **Turn Indicator** - Clear display of whose turn it is

### Phase 4: Additional Feature

**Options Under Consideration:**
- [ ] **Statistics Tracker** - Track wins/losses/pushes across sessions
- [ ] **Theme Switcher** - Light/Dark mode toggle
- [ ] **Best of 3 Mode** - Multi-round gameplay with series winner
- [ ] **Settings Panel** - Adjust font size, contrast, animation speed

### Phase 5: Animations & Polish
- [ ] **Card Draw Animation** - Smooth card dealing animation
- [ ] **Card Flip Animation** - Reveal dealer's face-down card with flip effect
- [ ] **Dealer Idle Animation** - Optional idle animation for dealer character
- [ ] **Smooth Transitions** - Polish all state changes with subtle animations

### Phase 6: Documentation
- [ ] **Code Comments** - Complete inline documentation for all methods and logic
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