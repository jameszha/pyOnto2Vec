import sys
import time


def main():
    input_actions_file_name = "../datasets/protein_actions.lst"
    input_vectors_file_name = "../embeddings/vectors_singleancestor.lst"
    output_file_name = "../output.dat"

    embeddings = dict()

    #
    with open(input_vectors_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            protein = line_data[0]
            vector = line_data[1:]
            embeddings[protein] = vector

    print("Protein embeddings loaded: " + str(len(embeddings)))

    output_file = open(output_file_name, 'w')
    action_types = {'activation':'+1', 'binding':'-1', 'catalysis':'+1', 'reaction':'-1', 'inhibition':'-1'}

    converted_action_count = 0
    unconverted_action_count = 0

    with open(input_actions_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            protein1 = line_data[0]
            protein2 = line_data[1]
            action = line_data[2]

            if (protein1 in embeddings) and (protein2 in embeddings) and action in (action_types):
                features = embeddings[protein1] + embeddings[protein2]
                for i, value, in enumerate(features):
                    features[i] = str(i+1) + ':' + value
                features = ' '.join(features)

                target = action_types[action]

                output_file.write(target + ' ' + features + '\n')

                converted_action_count = converted_action_count + 1
                if (converted_action_count % 1000 == 0): print("Converted actions: " + str(converted_action_count) + "\r" , end ='')

            else:
                unconverted_action_count = unconverted_action_count + 1

    print("\033[K",end='') 
    print("Converted actions: " + str(converted_action_count))
    print("Unconverted actions: " + str(unconverted_action_count))

    output_file.close()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")