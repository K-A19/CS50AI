from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave but noth both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    # If A is a knight, it is both a knave and knight, oherwise it is a knave
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is only either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    #B is only either a knight or a knave but not both
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    #If A is a knight, A and B are both knaves 
    Implication(AKnight, And(BKnave, AKnave)),

    #Otherwise A is a knave and B is a knight
    Implication(AKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is only either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    #B is only either a knight or a knave but not both
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    #A is a knight, B is a knight as well
    Implication(AKnight, BKnight),

    #If A is a knave, then B is a knight and vice versa
     Biconditional(AKnave, BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is only either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    #B is only either a knight or a knave but not both
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),

    # C is only either a knight or a knave but not both
    Or(CKnave, CKnight),
    Not(And(CKnave, CKnight)),    

    #If B is a knave, A is a knight and vice versa
    Biconditional(BKnave, AKnight),

    # If B is a knave, C is a knight and vice versa
    Biconditional(BKnave, CKnight),

    # If C is a knight, so is A and vice versa
    Biconditional(CKnight, AKnight),

    # If A is a knave, they called themself a knight
    Implication(AKnave, AKnight),

    # Otherwise A is a knight and called themself a knight
    Implication(AKnight, AKnight)
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
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
