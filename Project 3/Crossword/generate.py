import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterates over each variable in the crossword with their domains
        for variable in self.domains:

            # Creates a copy of the variable's domain so that the variable's domain can be changed without errors
            copy = self.domains[variable].copy()

            # Iterates over each word in the variable's domain
            for word in copy:
                
                # Removes the word from that variable's domain if it isnt the right length
                if len(word) != variable.length:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Creates a variable to track whether or not the domain of x was revised
        revised = False

        # Creates a variable to store the number of possible combinations of words in the domains of variables x and y
        possible = 0

        # Stores the pair representing an overlap if there is any
        overlap = self.crossword.overlaps[x, y]

        # There is no constraining arc between x and y so no revisions will be made
        if overlap == None:
            return revised
        
        # Creates a copy of x's domain to iterate over instead of the original so an error does not occur if the domain is changed
        x_copy = self.domains[x].copy()

        # Iterates over all the words in x's domain to compare them with all the words in y's domain
        for x_word in x_copy:

            # Creates a variable to store the number of possible combinations of words in the domains of variables x and y
            possible = 0

            for y_word in self.domains[y]:
                
                # Checks if the word from variable x has at least one other agrreing word in the second variable y 
                if x_word[overlap[0]] == y_word[overlap[1]]:
                    possible += 1
                
            if possible == 0:

                # If there is a conflict in which character would be the value of a square, the word is removed from x as no words agreed
                self.domains[x].remove(x_word)

                # Revised is changed to true to indicater that there ws a change made to x's domain
                revised = True
                
                    
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Includes all the arcs in the problem if arcs is None
        if arcs == None:
            arcs =[]
            for v1 in self.domains:
                for v2 in self.domains:
                    if v1 != v2:
                        if self.crossword.overlaps[v1, v2] != None:
                            arcs.append((v1, v2))

        # Creates a queue of the arcs
        queue = [arc for arc in arcs]
        
        while len(queue) != 0:
            # Chooses an arc from the que
            (i, j) = queue.pop(0)

            if self.revise(i, j):
                # If the domain is empty the problem cannot be solved so false is returned
                if len(self.domains[i]) == 0:
                    return False
                
                # Adds the neighbours to the current variable arc to the queue as long as it is not the original neighbour
                for neighbour in self.crossword.neighbors(i):
                    if neighbour != j:
                        queue.append((neighbour, i))
                        
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            # Returns false if a variable is not present in the assignment
            if variable not in assignment:
                return False 
            
            # Return false if a variable has no value 
            if assignment[variable] == None:
                return False
        
        # Otherwise returns true as every variable has been assigned a value
        return True
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Iterates over the value in the assignment with two different variables
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2:
                    # Returns false if not all the values for the variables are distinct
                    if assignment[v1] == assignment[v2]:
                        return False
                    
                    # Returns false if the value doesnt have the correct length
                    if v1.length != len(assignment[v1]):
                        return False
                    
                    # Creates a variable to store the possible overlap of both variables
                    overlap = self.crossword.overlaps[v1, v2]

                    # Makes sure there are no conflicts with assigned values if there is an overlap of both variables, and if there is false is returned
                    if overlap != None:
                        if assignment[v1][overlap[0]] != assignment[v2][overlap[1]]:
                            return False

        # Otherwise returns true as the assignment passed all checks
        return True
                    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Creates a list to store the values in the domain of var in order of their constraint value
        domain = []

        # Populates the domain list with all the words in the variables domain
        for word in self.domains[var]:
            domain.append(word)
        
        # Sorts list based on each words constraint_value
        sorted(domain, key= lambda word: self.constraint_value(word, var, assignment))

        return domain


        
    def constraint_value(self, word, var, assignment):
        """
        Returns the number of word choices for a variables's neighbours
        which are eliminated if the given word is assigned to the variable
        """
        # Stores the number of word choices for the neighbouring variables which are eliminated if the word is chosen
        constraint_count = 0

        # Makes sure to not consider variables already in the assignment list
        for variable in self.crossword.variables:
            if variable not in assignment:

                # Makes sure the cureent variable being iterated over isnt equal to the initial variable
                if variable != var:

                    # Stores the possible overlap of both variables
                    overlap = self.crossword.overlaps[var, variable]

                    # Confirms the twovariables are neighbours
                    if overlap != None:

                        # Iterates over all the possible values of the neighbouring variables
                        for test_word in self.domains[variable]:

                            # Increments the constraint_count variable if a conflict is found between the variables
                            if word[overlap[0]] != test_word[overlap[1]]:
                                constraint_count += 1

        return constraint_count


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Creates a variable to store and track the best variable to select next
        best_variable = None

        # Creates a counter variable to ensure  during the first loop the best variable is set to the current variable as there was no previous best variable
        counter = 0

        # Searches variables which have not already been assigned a value
        for variable in self.domains:
            if variable not in assignment:

                # Makes the current variable the best variable during the first run of the loop
                if counter == 0:
                    # Increments counter so that other loops use the best_variable gotten in the previous loop
                    counter += 1
                    best_variable = variable
                    continue
                
                # Changes the best variable to the current variable if it has fewer values in its domain
                if len(self.domains[variable]) < len(self.domains[best_variable]):
                    best_variable = variable
                    continue

                # Changes the best variable to the current variable if they have the same number of value in their domains but the current variable has more neighbours
                if len(self.domains[variable]) == len(self.domains[best_variable]):
                    if len(self.crossword.neighbors(variable)) >= len(self.crossword.neighbors(best_variable)):
                        best_variable = variable

            

        return best_variable


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)

        for word in self.domains[variable]:
            copy = assignment.copy()
            copy[variable] = word
            if self.consistent(copy):
                assignment[variable]= word
                result = self.backtrack(assignment)

                if result != None:
                    return result
                
                del assignment[variable]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
