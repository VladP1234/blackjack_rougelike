**Some info before you start playing**
Run `main.py` from the folder named `Blackjack`

1. Each card in your starting deck has an effect if you get blackjack
    - For example, if you have 16 and topdeck a 5 of hearts, then you heal for 5
    - Aces always give 11 worth irrespective of whether they are counted as 1 or 11
    - Hearts heal, clubs dead bonus damage, diamonds inflict bleeding, clubs give temporary hp
2. Merchant cards are broken
    - They have on reveal effects, i.e. whenever you draw the card, you get an effect. Most of them heal you for a lot
3. If you hit "d" during combat, you get to see your upcoming cards (in random order)
4. 'Alties' is a dev deck, use it if you wish to have no fun. Just spam hit and it will give you blackjack every time irrespective of your draw pile
5. Rules are as follows:
    - The person who has a lower score takes damage equal to the difference;
        - For example, you have 20 and the opponent scores a 15, the opponent takes 5 damage.
    - If a person goes bust, then they take damage equal to opponent's score - 11
    - If both go bust, then nothing happens
    - Some cards have on reveal effects - these effects happen when the card is drawn
    - Some have on blackjack effects - these effects happen when the card is drawn and the player's total reaches 21