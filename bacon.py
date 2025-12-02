# Jacob Reppeto
# Bacon.py

from __future__ import annotations
import sys

def buildGraphHelper(graph: dict[str, dict[str, str]], actors: list[str], film: str) -> None:
    """
        Helper function to help build the graph.
    We will add edges between all pairs of actors in the current film.
    For every pair of actors in `actors`, we add an edge both ways:
        graph[actorA][actorB] = film
        graph[actorB][actorA] = film
    We only add an edge if it doesn't already exist so the *first* film
    that connects the pair "wins" and later films won't overwrite it.
    :param graph: dict[str, dict[str, str]]
    :param actors: list[str]
    :param film: str
    :return: None
    """
    # If no film title or fewer than 2 actors, there are no pairs to connect.
    if not film or len(actors) < 2:
        return

    # Ensure adjacency dict exists exactly once per actor for this film
    for actor in actors:
        if actor not in graph:
            graph[actor] = {}

    # Generate all unique (i, j) pairs with i < j so each pair is handled once.
    actorLength = len(actors)

    #Nested loop to go through all pairs of actors
    for i in range(actorLength-1):
        actorA = actors[i]
        adjacentA = graph[actorA]
        for j in range(i + 1, actorLength):
            actorB = actors[j]
            adjacentB = graph[actorB]

            # Only add the edge if it doesn't already exist
            if actorB not in adjacentA:
                adjacentA[actorB] = film

            # Only add the edge if it doesn't already exist
            if actorA not in adjacentB:
                adjacentB[actorA] = film


def BuildGraph(filename: str) -> dict[str, dict[str, str]]:
    """
    Parse a film/actor list and build an undirected co-star graph in one pass.
    Expected file format (blank line separates films):
        Film Title (Year)
        Actor 1
        Actor 2

        Next Film (Year)
        Actor A
        Actor B
        ...

    :param filename: str
    :return: dict[str, dict[str, str]]
    """
    graph = {}
    currentFilm = None
    currentActors = []

    # Stream the file so memory use grows with the size of the graph, not the whole file.
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if line == '':

                # Blank line = end of a film block. If we have a valid block (film + ≥2 actors),
                if currentFilm and len(currentActors) >= 2:
                    buildGraphHelper(graph, currentActors, currentFilm)
                currentFilm = None
                currentActors = []

            elif currentFilm is None:
                # First non-blank line after a blank marks a new film title.
                currentFilm = line

            else:
                # Any subsequent non-blank lines until the next blank are actor names.
                currentActors.append(line)

        # After the loop, we may have a final film block to process.
        if currentFilm and len(currentActors) >= 2:
            buildGraphHelper(graph, currentActors, currentFilm)

    return graph


def breadthFirstSearch(graph: dict[str, dict[str, str]], startActor: str, targetActor: str) -> list[str] | None:
    """
    Preforms a breadth first search on the graph to find the shortest path from startActor to targetActor
    :param graph: dict[str, dict[str, str]]
    :param startActor: str
    :param targetActor: str
    :return: list[str] | None
    """

    # Check if startActor and targetActor are in the graph
    if startActor not in graph or targetActor not in graph:
        return None
    if startActor == targetActor:
        return [startActor]

    visited = {startActor}
    previous = {}
    queue = [startActor]
    head = 0

    #loop through queue and make sure we haven't found target actor
    while head < len(queue):

        #set current actor to head of queue and increment head
        currentActor = queue[head]
        head += 1

        #look at all neighbors of current actor
        for neighbor in graph[currentActor]:

            #if neighbor hasn't been visited yet, add to visited set and previous dict
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = currentActor

                # If we found the target actor, set found to True and break
                if neighbor == targetActor:
                    path = [targetActor]
                    current = targetActor
                    while current != startActor:
                        current = previous[current]
                        path.append(current)
                    path.reverse()
                    return path

                # Otherwise, add neighbor to the queue for further exploration
                queue.append(neighbor)

    return None
# ---------------------------------------------------------------------

def main(argv):

    if len(argv) > 1:
        filename = argv[1]
    else:
        filename = input('enter filename: ')
        print()

    graph = BuildGraph(filename)
    name = input('Enter Actor: ')

    while name != "":

        answer = breadthFirstSearch(graph, name, 'Kevin Bacon')

        #if we didn't find a path, print no path
        if answer is None:
            print(f'no path from {name} to Kevin Bacon')

        else:

            #go through answer list and print out each step
            for i in range(len(answer) - 1):
                a, b = answer[i], answer[i + 1]

                #print out both actors and the film they were in together
                print(f'{a} was in "{graph[a][b]}" with {b}')
        print()

        name = input('Enter Actor: ')

# ---------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)