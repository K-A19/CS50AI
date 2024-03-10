import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells in a sentencs are equal to the count, all of them are mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells

        # Otherwise you dont know if there are mines
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the cells in a sentence have a count of 0, none of them ar mines
        if self.count == 0:
            return self.cells

        # Otherwise you can't tell they are safe
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Checks to see if cells is in the sentence
        if cell in self.cells:
            # Removes the cell if it is present in the sentence
            self.cells.remove(cell)

            # Reduces the count by one as there will be one less mine
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Checks to see if cells is in the sentence
        if cell in self.cells:
            # Removes the cell if it is present in the sentence
            self.cells.remove(cell)

        # There is no need to change count as the number of mines has not decreased


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Adds cell to the moves made
        self.moves_made.add(cell)

        # Marks the cell as safe and updates any sentences containing the cell
        self.mark_safe(cell)

        # Creates a set to track the unknown neighbours
        neighbours = set()

        # Creates a variable to track known neighbouring mines
        mine_count = 0

        # Iterates over all of the cells neighbours
        for i in range((cell[0]-1), (cell[0]+2)):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Makes sure the cell is a valid cell on the board
                if -1 < i < self.height and -1 < j < self.width:

                    # Adds neighbouring cells to neighbours
                    if (i, j) != cell and (i, j) not in self.mines and (i, j) not in self.safes:
                        neighbours.add((i, j))

                    # Counts the number of known mines
                    if (i, j) in self.mines:
                        mine_count += 1
        
        # Makes a new sentence object about the cell's neighbours excluding those that are safe or mines
        neighbour = Sentence(neighbours, count-mine_count)

        # Makes sure it isn't an empty set
        if neighbour.cells != set():

            if len(neighbour.cells) > 0 and neighbour not in self.knowledge:

                # Adds the unidentified neighbours to the AI's knowledge base 
                self.knowledge.append(neighbour)

        change = 1

        while change != 0:
            change = 0

            # Checks if any new cells may be marked as safe or as mines
            for sentence in self.knowledge:

                # Checks to see if any new mines are discovered and marks them as such if there are
                if sentence.known_mines() != None:
                    mines = sentence.known_mines().copy()
                    for mine in mines:
                        change += 1
                        self.mark_mine(mine)

                # Checks to see if any new safes are discovered and marks them as such if there are
                if sentence.known_safes() != None:
                    safes = sentence.known_safes().copy()
                    for safe in safes:
                        change += 1
                        self.mark_safe(safe)

        # Iterates over every sentence in knowledge in order to check for the possibility of subset inferences
        for sentence in self.knowledge:
            for other in self.knowledge:

                # Makes sure other is a proper subset of the sentence
                if sentence.cells.issuperset(other.cells) and sentence != other:
                    # Makes use of the subset inference
                    info = Sentence(sentence.cells - other.cells, sentence.count - other.count)

                    # Makes sure that info isn't already in the Knowledge base and is not empty
                    if info not in self.knowledge and len(info.cells) > 0: 

                        # Marks more cells as mines if th new knowledge reveals more
                        if info.known_mines() != None:
                            mines = info.known_mines().copy()
                            for mine in mines:
                                self.mark_mine(mine)

                        # Marks more cells as safe if the new knowledge reveals more
                        if info.known_safes() != None:
                            safes = info.known_safes().copy()
                            for safe in safes:
                                self.mark_safe(safe)

                        if info not in self.knowledge and len(info.cells) > 0:
                            self.knowledge.append(info)

            # Creates a copy of the cells in the sentence
            info_two = sentence

            # Removes any knows safe cells from the sentence
            for safe in self.safes:
                info_two.mark_safe

            # Removes any known mines from the sentence
            for mine in self.mines:
                info_two.mark_mine

            if info_two not in self.knowledge and len(info_two.cells) > 0 :
                self.knowledge.append(info)

            # Makes sure there are no empty sentences
            if len(sentence.cells) < 1:
                self.knowledge.remove(sentence)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Ensures the move is safe
        for move in self.safes:
            # Returns a move if it has not be made before
            if move not in self.moves_made:
                return move

        # Returns None if there are no safe moves which haven't already been made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Creates a set of possible moves which haven't been made before and aren't mines
        possible = set()
       
        # Iterates over every single cell
        for i in range(self.height):
            for j in range(self.width):
                # Ensure the cell isn't a move already made and is not a mine
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    possible.add((i, j))

        # Return a random cell in the possible moves set
        return possible.pop()