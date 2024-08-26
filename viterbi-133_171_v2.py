#Oliver Skou Olsen s205443
#Eksamens Projekt - Viterbi Dekoder
#34220 Coding in Communication Systems
#Kommentarer skrives på engelsk
import numpy as np


#NOT DONE. NEEDS TO BE EXPANDED, SO IT SUPPORTS 133, 171.
#CURRENT STATE: Copy of  1011, 1111, 1101

#Returns length of sequence (used for trellis diagram)
def sequence(seq: list) -> int:
    seq_elements = len(seq)
    return seq_elements


def trellis_construct(matrix_size: int, generator_states: list) -> list:

    # Twice the length of the generator, since each point can be accessed from two points
    trellis_hamming = np.zeros((2*len(generator_states), matrix_size))
    trellis_hamming_reduced = np.zeros((len(generator_states), matrix_size))
    return trellis_hamming, trellis_hamming_reduced



# Takes the generator state and calculates the hamming distance for the initial sequence "move"
def hammingDistance(generator_states: str, seq: str, previousDist: int) -> int:

    if generator_states[0] != seq[0]:
        previousDist = previousDist + 1

    if generator_states[1] != seq[1]:
        previousDist = previousDist + 1


    return previousDist


# Unintentional hard decision. Chooses the upper path at a tie, since the equal, is not smaller.
def lowestHamming(ham1: int, ham2: int) -> int:
    if ham1 > ham2:
        return ham2
    else:
        return ham1


# Calculates hamming distance by using the viterbi. Returns a list with the distances:
def viterbi_trellis(input_seq: list, generator_poly: list, store_hamming: list, hamming_path: list) -> list:


    # Used to make navigation easier
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5
    g = 6
    h = 7


    # First step
    # Starts in 0, therefore there is no previous hamming distance. This means it is 0 to start with.
    #  hamming_path[point][column] = hammingDistance(generator_poly[point][upOrDown], input_seq[column], hamming_path[prevPoint][prevColumn])
    hamming_path[a][0] = hammingDistance(generator_poly[a][0], input_seq[0], 0)                   # a0 -> a1
    hamming_path[b][0] = hammingDistance(generator_poly[a][1], input_seq[0], 0)                   # a0 -> b1



    # Second step
    # Second row uses the hamming distance from point a & b, from the first step.
    hamming_path[a][1] = hammingDistance(generator_poly[a][0], input_seq[1], hamming_path[a][0])  # a1 -> a2
    hamming_path[b][1] = hammingDistance(generator_poly[a][1], input_seq[1], hamming_path[a][0])  # a1 -> b2
    hamming_path[c][1] = hammingDistance(generator_poly[b][0], input_seq[1], hamming_path[b][0])  # b1 -> c2
    hamming_path[d][1] = hammingDistance(generator_poly[b][1], input_seq[1], hamming_path[b][0])  # b1 -> d2

    # Third step
    hamming_path[a][2] = hammingDistance(generator_poly[a][0], input_seq[2], hamming_path[a][1])  # a2 -> a3
    hamming_path[b][2] = hammingDistance(generator_poly[a][1], input_seq[2], hamming_path[a][1])  # a2 -> b3
    hamming_path[c][2] = hammingDistance(generator_poly[b][0], input_seq[2], hamming_path[b][1])  # b2 -> c3
    hamming_path[d][2] = hammingDistance(generator_poly[b][1], input_seq[2], hamming_path[b][1])  # b2 -> d3
    hamming_path[e][2] = hammingDistance(generator_poly[c][0], input_seq[2], hamming_path[c][1])  # c2 -> e3
    hamming_path[f][2] = hammingDistance(generator_poly[c][1], input_seq[2], hamming_path[c][1])  # c2 -> f3
    hamming_path[g][2] = hammingDistance(generator_poly[d][0], input_seq[2], hamming_path[d][1])  # d2 -> g3
    hamming_path[h][2] = hammingDistance(generator_poly[d][1], input_seq[2], hamming_path[d][1])  # d2 -> h3



    # loops for the remainder of columns/sequences left. The first two unique steps have been completed, therefore loop starts at 2.
    for elements in range(3, len(input_seq)):

        #Path to a from a and e. Lowest hamming distance is saved
        hamming_path[a][elements] = lowestHamming(hammingDistance(generator_poly[a][0], input_seq[elements], hamming_path[a][elements-1]),
                                                hammingDistance(generator_poly[e][0], input_seq[elements], hamming_path[e][elements-1]))

        #Path to b from a and e
        hamming_path[b][elements] = lowestHamming(hammingDistance(generator_poly[a][1], input_seq[elements], hamming_path[a][elements-1]),
                                                hammingDistance(generator_poly[e][1], input_seq[elements], hamming_path[e][elements-1]))

        #Path to c from b and f
        hamming_path[c][elements] = lowestHamming(hammingDistance(generator_poly[b][0], input_seq[elements], hamming_path[b][elements-1]),
                                                hammingDistance(generator_poly[f][0], input_seq[elements], hamming_path[f][elements-1]))

        #Path to d from b and f
        hamming_path[d][elements] = lowestHamming(hammingDistance(generator_poly[b][1], input_seq[elements], hamming_path[b][elements-1]),
                                                hammingDistance(generator_poly[f][1], input_seq[elements], hamming_path[f][elements-1]))

        #Path to e from c and g
        hamming_path[e][elements] = lowestHamming(hammingDistance(generator_poly[c][0], input_seq[elements], hamming_path[c][elements-1]),
                                                hammingDistance(generator_poly[g][0], input_seq[elements], hamming_path[g][elements-1]))

        #Path to f from c and g
        hamming_path[f][elements] = lowestHamming(hammingDistance(generator_poly[c][1], input_seq[elements], hamming_path[c][elements-1]),
                                                hammingDistance(generator_poly[g][1], input_seq[elements], hamming_path[g][elements-1]))

        #Path to g from d and h
        hamming_path[g][elements] = lowestHamming(hammingDistance(generator_poly[d][0], input_seq[elements], hamming_path[d][elements-1]),
                                                hammingDistance(generator_poly[h][0], input_seq[elements], hamming_path[h][elements-1]))

        #Path to h from d and h
        hamming_path[h][elements] = lowestHamming(hammingDistance(generator_poly[d][1], input_seq[elements], hamming_path[d][elements-1]),
                                                hammingDistance(generator_poly[h][1], input_seq[elements], hamming_path[h][elements-1]))

    return hamming_path




def corrected_sequence(hamming_tree: list, recieved_seq: list) -> list:

    #Stores the final row path, from right to left
    path = []

    #Used to store the cheapest path. Set to infinite so the first compare is automatically the smallest
    smallest = float('inf')

    # Minus 1 to be used as an index
    lastCol = len(recieved_seq) - 1


    #Finds the smallest hamming distance at the back of the hamming distance tree
    for row in range(8):
        #print(firstCol)
        if hamming_tree[row][lastCol] < smallest:
            smallest = hamming_tree[row][lastCol]
            currentRow = row

    #The smallest hamming values, row is chosen
    path.append(currentRow)


    #Movement rules. a = 0, b = 1, c = 2, d = 3, e = 4, f = 5, g = 6, h = 7. Controlls which points can be accessed from current row
    rules_move = {
        0: [0, 4],
        1: [0, 4],
        2: [1, 5],
        3: [1, 5],
        4: [2, 6],
        5: [2, 6],
        6: [3, 7],
        7: [3, 7]
        }

    #Goes through the tree for each column, but stops at the second column
    for columns in range(lastCol, 2, -1):
        previousPos = rules_move[currentRow]
        smallest = float('inf')
        smallestPrevState = None

        #Uses the dictionary above (rules_move) to navigate through only paths allowed
        for prev_position in previousPos:
            if hamming_tree[prev_position][columns - 1] < smallest:
                smallest = hamming_tree[prev_position][columns - 1]
                smallestPrevState = prev_position

        #Cheapest hamming distance row to choose. Saves the current state in the path, but also for the next loop
        currentRow = smallestPrevState
        path.append(currentRow)



    smallest = float('inf')
    smallestPrevState = None
    if currentRow in [4, 5]:
        currentRow = 2
    elif currentRow in [6, 7]:
        currentRow = 3
    elif currentRow in [2, 3]:
        currentRow = 1

    else:
        currentRow = 0

    path.append(currentRow)


    #Manually handles first column, since the path options are fewer
    #Resets variables
    smallest = float('inf')
    smallestPrevState = None

    #chooses either a or b
    for prev_position in [0, 1]:
        if hamming_tree[prev_position][0] < smallest:
            smallest = hamming_tree[prev_position][0]
            smallestPrevState = prev_position

    #Saves the "last path" and reverses the list, since we entered from the back.
    path.append(smallestPrevState)
    path.reverse()

    #The actual final step from a or b to a is inserted in the path, since we always start at 0 (a).
    path.insert(0, 0)


    #Used to determine the way that has been chosen. a->a would mean a key called "00" which would output ["000", "0"]. The first element is the corrected sequence, the other is the message decoded
    moves_sequence = {
        "00": ["000", "0"],
        "01": ["111", "1"],
        "12": ["011", "0"],
        "13": ["100", "1"],
        "24": ["110", "0"],
        "25": ["001", "1"],
        "36": ["101", "0"],
        "37": ["010", "1"],
        "40": ["111", "0"],
        "41": ["000", "1"],
        "52": ["100", "0"],
        "53": ["011", "1"],
        "64": ["001", "0"],
        "65": ["110", "1"],
        "76": ["010", "0"],
        "77": ["101", "1"]
    }

    #Stores a list of lists that contains the corrected message and the decoded message
    corrected_DATA = []

    #Starts in 1, since we compare with previous
    print(path)
    for steps in range(1, len(path)):
        connectionPath = str


        prevPath = str(path[steps-1])
        currenPath = str(path[steps])
        connectionPath = prevPath + currenPath
        #print(connectionPath)
        #print(connectionPath)
        #Uses the dict to find the corrected sequence and message
        corrected_DATA.append(moves_sequence[connectionPath])

    #Returns the final data
    return corrected_DATA


#Used to display the data nicely
def nicelyDisplayed(data: list):
    #print(data)

    #Strores the sequence (corrected)
    sequence_new = []

    #Stores the decoded message
    decodedMessage = []

    #Splits the data and displays it
    for elements in range(len(data)):
        sequence_new.append(data[elements][0])
        decodedMessage.append(data[elements][1])

    print("Corrected sequence")
    print(sequence_new, "\n")

    print("decoded message")
    print(decodedMessage)
    return





if __name__ == "__main__":

    # Generator polynomial
    #                         A               B               C               D               E               F               G               H
    generator133_171 = [["000", "111"], ["011", "100"], ["110", "001"], ["101", "010"], ["111", "000"], ["100", "011"], ["001", "110"], ["010", "101"]]

    # The above, but split into abcd
    #generator111_101_a = ["00", "11"]
    #generator111_101_b = ["10", "01"]
    #generator111_101_c = ["11", "00"]
    #generator111_101_d = ["10", "10"]




    # Sequence to be decoded. Entered as a list of strings. This sequence is from the slides
    input_sequence = ["000", "101", "000", "101", "000", "101", "000"]


    # Get length of sequence
    length_of_sequence = sequence(input_sequence)

    # Create matrix. Uses the length of the sequence to determine size
    ready_hamming, reduced_hamming = (trellis_construct(length_of_sequence, generator133_171))

    #print(reduced_hamming)
    # DEMO row, column
    #ready_hamming[5][3] = 5

    #Gets the hamming distances
    hammign_matrix = viterbi_trellis(input_sequence, generator133_171, ready_hamming, reduced_hamming)

    print("All distancces (smallest one for each point). It is only the first two rows in the first column that is used.\nThis means the rest of the column will always stay at 0, but the code will never use them in the hamming distance")
    print(hammign_matrix, "\n")

    #Calculates the corrected sequence and the decoded message
    mostLikely_sequence = corrected_sequence(hammign_matrix, input_sequence)

    print("Input Sequence:")
    print(input_sequence)
    print("\n")

    #Displays the data
    nicelyDisplayed(mostLikely_sequence)

    print("Expected sequence")
    print("000, 111, 100, 101, 001, 111, 000")


