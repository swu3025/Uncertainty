import os
import random
from random import randint
import re
import sys
import copy 

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

# MY CODE
def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob = {}
    length = len(corpus[page])
    
    if length > 0:
        for link in corpus:
            prob[link] = (1-damping_factor) / len(corpus)
        for link in corpus[page]:
            prob[link] += damping_factor / length
    else:
        for link in corpus:
            prob[link] = 1 / len(corpus)

    return prob

# MY CODE
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {}
    for page in corpus:
        distribution[page] = 0
    
    page = random.choice(list(corpus.keys()))

    for i in range(1, n):
        current_distribution = transition_model(corpus, page, damping_factor)
        for page in distribution:
            #multiplies the current average with i - 1 to get the total probability so it can add the new probability and reaverage that with i number of probabilities
            distribution[page] = ((i-1) * distribution[page] + current_distribution[page]) / i
        
        #choices(list,weight the possibility for each value, length of resulting list)
        page = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
    return distribution

# MY CODE
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    n = len(corpus)
    d = damping_factor

    ranks = {}
    for page in corpus:
        ranks[page] = 1 / n

    change = True
    while change:
        change = False
        distribution = ranks
        for page in corpus:
            ranks[page] = ((1 - d) / n) + (d * iterative_sum(corpus, distribution, page))
            change = change or abs(distribution[page] - ranks[page]) > 0.001

    return ranks

# MY CODE
def iterative_sum(corpus, distribution, page):
    s = 0
    
    for p,link in corpus.items():
        if page in link:
            s += distribution[p] / len(link)

    return s



if __name__ == "__main__":
    main()
