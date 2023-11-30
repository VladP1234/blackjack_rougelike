# Problem Definition
"People", or, to be specific a "person" would like me to build a prototype of a modernised version of blackjack. For reasons beyond my comprehension, this person is utterly disgusted by the concept of felt, more specifically green felt. Despite these reasons being beyond my comprehension, I will comply with with that "person's" request and fullfil his request of building a modernised version of blackjack.

Therefore, the blackjack game will be designed explicitly to avoid the ways that the original blackjack is played.

# Needs and Objectives
The project needs to be NOT like the original blackjack game. I was recently captivated by a game called Wildfrost, so I will be building a ~~rougelike~~ roguelike-ish game where the person goes through rooms and climbs floors.

**Compulsory Components**
1. NO GREEN FELT
2. The player has their own deck and the ability to hit/stand
    - The player should have agency in their starting deck
    - And in how their deck progresses throughout a run
3. The enemies must have different capabilities, some being more or less aggressive and, at the later stages, be able to see the top card of their deck.
4. The basic rules of blackjack
    - Both the player and the enemy having the ability to go bust
    - A way for both to take damage as a function of the difference of scores
5. An intuitive layout with tooltips/additional information to explain the game if necessary
6. The code is to have
    - "Modular design"
    - And utilise "OOP methodologies"

These are the minimum requirements that I agreed upon with the "person" and therefore the highest priority at the beginning of the game development.

**Optional Objectives**

Once the compulsory components are completed, the optional objectives ought to be operationalised

1. Multiple floors of combats
2. A variety of merchant cards and costs
3. Status effects inflicted upon the player and/or the enemy based on what card is drawn or what card gets the player/enemy to blackjack
4. All the data stored in json files

# Feasibility Report

## General Concerns

### Legal
I need to avoid plagiarism of other games. I will do that by not copying other games. I am not aware of any deckbuilder blackjack games, so this should not be an issue

### Other products
As said in the legal section, the "person" with whom I have discussed the specifications of the game asked me specifically to design this game. Since the game is mostly inspired by blackjack rather than a digital version of it, It should be easy to avoid falling into the trap of making a disgusting table with green felt.

### Social and Ethical
None. It's blackjack-esque deckbuilder, there aren't going to be social and ethical issues with building it. The game is a prototype that will be tested by one (1) person without any notable disabilities and therefore there are no concerns about inclusivity. The tester does not have a history of gambling/card games so the design of the game will not cause any concerns. This will only need to be addressed if and only if the game will be commecrially available.

## Specific Issues

### Cost Effectiveness
Since I will be paid with imaginary numbers that for some reason will significantly impact the course of my immediate future, this project is extremely cost effective for my client. Moreover, the client will be paid by an entity originating from the far lands of Scotland throughout my completion of this project with the only stipulation being that they will have to help me. Thus, this project is the most cost effective project that is hypothetically possible.

### Scheduling
I have 8 weeks to complete this project. This should be ample time for me to complete it. The compulsory components should be implemented within the first couple weeks, leaving me 6 or so weeks to complete the optional objectives. I am expecting to enjoy this project, so scheduling should not be an issue.

### Technical
The hardware provided to me (2020 Macbook Air with 8GB of RAM) is plenty for a full completion of this project. This is because the scope of the project is pretty small, with an expected size of < 50MB including all the data. I should not run into performace issue due to the project being a turn based game with no animations.

### Operational
The compulsory components describes a mostly simple game, which I should be capable of completing in a short time. Since the solution specifications were discussed with the "person", the solution should fit the requirements perfectly.

## Conclusion
Yep, feasible.

# Evaluation for Implementation Methods

## Parallel
Irrelevant, there is no preexisting software and therefore impossible to run the new and the non-existent simultaniously.

## Phased
Same as parallel, irrelevant due to lack of preexisting software

## Direct Cutover
One of two viable methods by process of elimination. It is a fine method, but due to me building a prototype, it is not the best

## Pilot
The best implementation method due to me designing a prototype which may be later developed into a full game

# Data Flow Diagram
Is in the file named "data flow diagram". Note that this is not perfectly exhaustive as making an exhaustive dfd for the couple thousand lines of code is mostly insane

