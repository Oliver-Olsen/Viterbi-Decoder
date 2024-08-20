#Oliver Skou Olsen
#Eksamens Projekt - Viterbi Dekoder
#34220 Coding in Communication Systems
#Kommentarer skrives på engelsk
import numpy as np



#Returns length of sequence (used for trellis diagram)
def sequence(seq: list) -> int:
    seq_elements = len(seq)
    return seq_elements


def trellis_construct(matrix_size: int, generator_states: list)-> list:
    # Twice the length of the generator, since each point can be accessed from two points
    trellis_hamming = np.zeros((2*len(generator_states), matrix_size))
    return trellis_hamming








if __name__ == "__main__":

    # Generator polynomial
    generator111_101 = [["00", "11"], ["10", "01"], ["11", "00"], ["01", "10"]]




    # Sequence to be decoded. Entered as a list of strings
    input_sequence = ["11", "01", "01", "10", "01"]


    # Get length of sequence
    length_of_sequence = sequence(input_sequence)

    # Create matrix. Uses the length of the sequence to determine size
    print(trellis_construct(length_of_sequence, generator111_101))
