###### --------------------------------------------
## The author of these scripts is T. D. Devlin 
###### --------------------------------------------

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 1
# A says "I am both a knight and a knave."
# ----------------------------------------
##   write the statement(s) in PL

stat = And(AKnight, AKnave)

##   Fill in the knowledge base
knowledge1 = And(

    # A is either a knight or a knave
    Xor(AKnight, AKnave),

    # If A is knight, what A says is true
    Implication(AKnight, stat),

    # If A is knave, what A says is false
    Implication(AKnave, Not(stat))
)
# ----------------------------------------

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# ----------------------------------------
##   write the statement(s) in PL

statA = Or(And(AKnight, BKnight), And(AKnave, BKnave))

statB = Or(And(AKnight, BKnave), And(AKnave, BKnight))

##   Fill in the knowledge base
knowledge2 = And(

    # A is either a knight or a knave
    Xor(AKnight, AKnave),

    # B is either a knight or a knave
    Xor(BKnight, BKnave),

    # If A is a knight, what A says is true
    Implication(AKnight, statA),

    # If A is knave, what A says is false
    Implication(AKnave, Not(statA)),

    # If B is a knight, what B says is true
    Implication(BKnight, statB),

    # If B is knave, what B says is false
    Implication(BKnave, Not(statB))

)
# ----------------------------------------

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# ----------------------------------------
##   write the statement(s) in PL 

statA1 = AKnight
statA2 = AKnave

statB2 = CKnave

statC = AKnight

##   Fill in the knowledge base
knowledge3 = And(
    # A is either a knight or a knave
    Xor(AKnight, AKnave),

    # B is either a knight or a knave
    Xor(BKnight, BKnave),

    # C is either a knight or a knave
    Xor(CKnight, CKnave),

    # If B is a knight, the first thing B says is true (A says they are a knave)

    # Then, If A is a knight, What A says is true
    Implication(And(BKnight, AKnight), statA2),

    # But if A is a knave, then what A says is false
    Implication(And(BKnight, AKnave), Not(statA2)),

    # If B is a knave, the first thing B says is false (A says they are a knight)

    # Then, If A is a knight, What A says is true
    Implication(And(BKnave, AKnight), statA1),

    # But if A is a knave, then what A says is false
    Implication(And(BKnave, AKnave), Not(statA1)),

    # If B is a knight, the second thing B says is true
    Implication(BKnight, statB2),

    # If B is knave, the second thing B says is false
    Implication(BKnave, Not(statB2)),

    # If C is a knight, what C says is true
    Implication(CKnight, statC),

    # If C is knave, what C says is false
    Implication(CKnave, Not(statC))

)
# ----------------------------------------


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
