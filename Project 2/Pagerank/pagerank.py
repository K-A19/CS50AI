import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Creates a dictionary to store the transition model
    transition_model = {}

    # Creates one of the variables which affects a page's pageranking    
    factor = ((1 - damping_factor)/float(len(corpus)))

    # If the page has no links it returns a probability distribution that chooses randomly among all pages with equal probability
    if len(corpus[page]) == 0:
        for pg in corpus:
            transition_model[pg] = factor

        return transition_model

    # Creates the second factor required to determine a page's pageranking
    factor_two = (damping_factor/float(len(corpus[page])))

    # Iterates over all the pages in the corpus
    for pg in corpus:

        # Includes all pages passed on the probability of picking a random page in the corpus
        transition_model[pg] = factor

        # Calculates the page ranking for the pages linked to by the current link
        if str(pg) in corpus[page]:
            transition_model[pg] += factor_two

    return transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Creates and populates a dict to keep track of all the page ranks
    pagerank = {}
    for key in corpus:
        pagerank[key] =  0

    # Rpeats the sampling process n times
    for i in range(n):

        # Chooses a random page if its the first sample page and updates it's page rank
        if i == 0:
            page = random.choice(list(corpus.keys()))
            pagerank[page] += 1
            pass

        # Creates a transition model based on the previous page
        sample = transition_model(corpus, page, damping_factor)

        # Makes a random weighed choice of a page
        page = random.choices(list(sample.keys()), weights = list(sample.values()), k = 1)[0]

        # Updates the pagerank dictionary
        pagerank[page] += 1

    # Normalizes all the values in the pagerank dictionary
    for page in corpus:
        pagerank[page] /= n

    # Return the dictionary of pageranks
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Creates and populates a dict to keep track of all the page ranks
    pagerank = {}
    for key in corpus:
        pagerank[key] =  1/len(corpus)

    # Causes a repition of pagerank calculation until the degree of 0.001 accuracy is met
    while True:

        # Creates a copy of the current pagerank dict to calculate the degree of accuracy later
        copy = pagerank.copy()

        for page in corpus:
            
            # Creates a list which will be used to help calculate the sum of PR(i)/ NumLinks(i)
            info = []

            # Iterates over all other pages except the current one
            for key in pagerank:

                # Ensures the current page is excluded from the calculation as well as ensure the current page is linked to by included pages
                if key != page and page in corpus[key]:

                    # Assumes a page with no links has links to every page
                    if len(corpus[key]) == 0:
                        info.append((pagerank[key], len(corpus)))

                    # Scenario for any other pages with their own links
                    else:
                        info.append((pagerank[key], len(corpus[key])))

            # Calculates the PR(i)/NumLinks(i)
            for i in range(len(info)):
                info[i] = info[i][0] / info[i][1]

            # Sums all the PR(i)/NumLinks(i) together
            sum = SUM(info)


            # Calculates the current page's new page rank
            copy[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * sum)

        for page in corpus:

            # Creates a variable which allows return of the pagerank dictionary when accuracy of 0.001 is met
            flag = True

            # Checks the difference between the current and old pangeranks to check the degree of accuracy
            if abs(pagerank[page] - copy[page]) > 0.001:
                flag = False
                
                # Updates the previous pagerank to be the same as the new one
                pagerank = copy
                break

        # Ends the infinite loop if a 0.001 degree of accuracy is reached
        if flag:
            return pagerank




# Creates a sum helper function
def SUM(sequence):
    sum = 0
    for num in sequence:
        sum += num

    return sum


if __name__ == "__main__":
    main()