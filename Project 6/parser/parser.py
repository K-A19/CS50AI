import nltk
nltk.download('punkt')
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP NP | S Conj S | S Conj VP NP | S Conj VP NP VP | S Conj NP VP NP Adv
NP -> Adj NP | Det NP | NP P NP | P NP | N 
VP -> V | Adv V | V Adv

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Gets a list of all the words in the sentence in lower case
    words = [word.lower() for word in  nltk.tokenize.word_tokenize(sentence)]

    # Removes words from the list which do not contain any letters
    for word in words:
        if not any(c.isalpha() for c in word):
            words.remove(word)

    # Returns the list of words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = [chunk for chunk in tree.subtrees(filter=lambda t : t.label() =="NP")]

    chunk_np = []

    for chunk in chunks :

        sub = 0

        for part in chunk.subtrees(filter=lambda t : t.label() =="NP"):
            
            if part == chunk:
                continue

            
            chunks.append(part)
            sub += 1

        if sub == 0 and chunk not in chunk_np:
            chunk_np.append(chunk)

    return chunk_np



if __name__ == "__main__":
    main()
