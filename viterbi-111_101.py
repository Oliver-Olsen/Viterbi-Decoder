#Oliver Skou Olsen s205443
#Eksamens Projekt - Viterbi Dekoder
#34220 Coding in Communication Systems
#Kommentarer skrives på engelsk
import numpy as np

#print("WORKS")

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
    #print("hamming done")
    return previousDist

def lowestHamming(ham1: int, ham2: int) -> int:
    # Hard decision. chooses the upper path at a tie.
    #print(ham1, "ham1")
    #print(ham2, "ham2")
    if ham1 > ham2:
        return ham2
    else:
        return ham1

# Calculates hamming distance by using the viterbi. Returns a list with the distances:
def viterbi_trellis(input_seq: list, generator_poly: list, store_hamming: list, hamming_path: list) -> list:

    #store_hamming[ROW][COL] = hammingDistance(generator_poly[ABCD][01], input_seq[ELEMENT], store_hamming[ROW][COL])
    # 0,1 = A
    # 2,3 = B
    # 4,5 = C
    # 6,7 = D

    # Used to make easier navigate
    a = 0
    b = 1
    c = 2
    d = 3

    # First step
    hamming_path[a][0] = hammingDistance(generator_poly[a][0], input_seq[0], 0)                    # a0 -> a1

    hamming_path[b][0] = hammingDistance(generator_poly[a][1], input_seq[0], 0)                    # a0 -> b1

    # Second step
    hamming_path[a][1] = hammingDistance(generator_poly[a][0], input_seq[1], hamming_path[a][0])  # a1 -> a2
    hamming_path[b][1] = hammingDistance(generator_poly[a][1], input_seq[1], hamming_path[a][0])  # a1 -> b2
    hamming_path[c][1] = hammingDistance(generator_poly[b][0], input_seq[1], hamming_path[b][0])  # b1 -> c2
    hamming_path[d][1] = hammingDistance(generator_poly[b][1], input_seq[1], hamming_path[b][0])  # b1 -> d2

    # loops for the remainder of columns/sequences left. The first two unique steps have been completed, therefore loop starts at 2.
    for elements in range(2, len(input_seq)):

        #Path to a from a and c. Lowest hamming distance is saved
        hamming_path[a][elements] = lowestHamming(hammingDistance(generator_poly[a][0], input_seq[elements], hamming_path[a][elements-1]),
                                                hammingDistance(generator_poly[c][0], input_seq[elements], hamming_path[c][elements-1]))

        #Path to b from a and c
        hamming_path[b][elements] = lowestHamming(hammingDistance(generator_poly[a][1], input_seq[elements], hamming_path[a][elements-1]),
                                                hammingDistance(generator_poly[c][1], input_seq[elements], hamming_path[c][elements-1]))

        #Path to c from b and d
        hamming_path[c][elements] = lowestHamming(hammingDistance(generator_poly[b][0], input_seq[elements], hamming_path[b][elements-1]),
                                                hammingDistance(generator_poly[d][0], input_seq[elements], hamming_path[d][elements-1]))

        #Path to d from b and d
        hamming_path[d][elements] = lowestHamming(hammingDistance(generator_poly[b][1], input_seq[elements], hamming_path[b][elements-1]),
                                                hammingDistance(generator_poly[d][1], input_seq[elements], hamming_path[d][elements-1]))

        #print(input_seq[elements])
        #store_hamming[0][elements] = hammingDistance(generator_poly[0][0], input_seq[elements], store_hamming[0][elements-1])   #a->a
        #store_hamming[1][elements] = hammingDistance(generator_poly[2][0], input_seq[elements], store_hamming[][elements-1])
        #store_hamming[2][elements] = hammingDistance(generator_poly[0][1], input_seq[elements], store_hamming[0][elements-1])   #a->b

    return hamming_path




def corrected_sequence(hamming_tree: list, recieved_seq: list) -> list:

    #Stores the final row path, from right to left
    path = []

    #Used to store the cheapest path
    smallest = float('inf')

    # Minus 1 to be used as an index
    lastCol = len(recieved_seq) - 1



    #Finds the smallest hamming distance at the back of the hamming distance tree
    for row in range(4):
        #print(firstCol)
        if hamming_tree[row][lastCol] < smallest:
            smallest = hamming_tree[row][lastCol]
            currentRow = row

    #The smallest hamming values, row is chosen
    path.append(currentRow)

    #Movement rules. a = 0, b = 1, c = 2, d = 3. Controlls which points can be accessed from current row
    rules_move = {
        0: [0, 2],
        1: [0, 2],
        2: [1, 3],
        3: [1, 3]
        }

    for columns in range(lastCol, 1, -1):
        previousPos = rules_move[currentRow]
        smallest = float('inf')
        smallestPrevState = None

        for prev_position in previousPos:
            if hamming_tree[prev_position][columns - 1] < smallest:
                smallest = hamming_tree[prev_position][columns - 1]
                smallestPrevState = prev_position

        currentRow = smallestPrevState
        path.append(currentRow)


    smallest = float('inf')
    smallestPrevState = None
    for prev_position in [0, 1]:
        if hamming_tree[prev_position][0] < smallest:
            smallest = hamming_tree[prev_position][0]
            smallestPrevState = prev_position
    path.append(smallestPrevState)
    path.reverse()


    path.insert(0, 0)

    #Stores the corrected sequence
    cSeq = []

    moves_sequence = {
    #eg a->a seq00 decodes 0
        "00": ["00", "0"], #aa
        "01": ["11", "1"], #ab
        "12": ["10", "0"], #bc
        "13": ["01", "1"], #bd
        "20": ["11", "0"], #ca
        "21": ["00", "1"], #cb
        "32": ["01", "0"], #dc
        "33": ["10", "1"]  #dd
    }

    corrected_DATA = []
    for steps in range(1, len(path)):
        connectionPath = str
        prevPath = str(path[steps-1])
        currenPath = str(path[steps])
        connectionPath = prevPath + currenPath
        #print(connectionPath)
        corrected_DATA.append(moves_sequence[connectionPath])

    return corrected_DATA


def nicelyDisplayed(data: list):
    #print(data)
    sequence_new = []
    decodedMessage = []

    for elements in range(len(data)):
        sequence_new.append(data[elements][0])
        decodedMessage.append(data[elements][1])

    print("Corrected sequence")
    print(sequence_new)

    print("decoded message")
    print(decodedMessage)
    return





if __name__ == "__main__":

    # Generator polynomial
    #                        A             B             C             D
    generator111_101 = [["00", "11"], ["10", "01"], ["11", "00"], ["01", "10"]]

    # The above, but split into abcd
    #generator111_101_a = ["00", "11"]
    #generator111_101_b = ["10", "01"]
    #generator111_101_c = ["11", "00"]
    #generator111_101_d = ["10", "10"]




    # Sequence to be decoded. Entered as a list of strings
    input_sequence = ["11", "01", "01", "10", "01"]
    #input_sequence = ["01", "00", "01", "00", "00"]


    # Get length of sequence
    length_of_sequence = sequence(input_sequence)

    # Create matrix. Uses the length of the sequence to determine size
    ready_hamming, reduced_hamming = (trellis_construct(length_of_sequence, generator111_101))

    # DEMO row, column
    #ready_hamming[5][3] = 5


    hammign_matrix = viterbi_trellis(input_sequence, generator111_101, ready_hamming, reduced_hamming)
    print("All distancces (smallest one for each point)")
    print(hammign_matrix)

    mostLikely_sequence = corrected_sequence(hammign_matrix, input_sequence)
    
    nicelyDisplayed(mostLikely_sequence)


