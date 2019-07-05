from gensim.models import Word2Vec
import sys
import time

def main():
    if len(sys.argv) < 4:
        print("Usage: python word2vec.py <all_axioms.lst> <all_entities.lst> <vectors.lst>")
        exit()
    axiom_file_name = sys.argv[1]
    entity_file_name = sys.argv[2]
    vector_file_name = sys.argv[3]

    print("\nLoading corpus and Training model . . . \n")

    # Onto2Vec uses the following parmeters for Word2Vec
    #   sg          Choice of training algorithm (sg=1: skip-gram; sg=0: CBOW)                            1 
    #   size        Dimension of the obtained vectors                                                   200 
    #   min_count   Words with frequency lower than this value will be ignored                            1 
    #   window      Maximum distance between the current and the predicted word                          10 
    #   iter        Number of iterations                                                                  5 
    #   negative    Whether negative sampling will be used and how many 'noise words' would be drawn      4
    #
    model = Word2Vec(corpus_file=axiom_file_name, sg=1, size=200, min_count=1, window=10, iter=5, negative=4, workers=4)


    print("\nGenerating vectors for each entity . . . \n")

    entity_count = 0
    mismatched_count = 0

    entity_file = open(entity_file_name, 'r')
    vector_file = open(vector_file_name, 'w')

    # Iterate through list of entities, calculate their vector representations, and output the vector to vectors.lst
    for entity in entity_file:
        entity = entity.strip()
        if entity in model.wv.vocab:
            vector = model[entity]
            vector_file.write(entity + ' ' + ' '.join(str(element) for element in vector) + '\n')

            entity_count = entity_count + 1
            if (entity_count % 1000 == 0):
                print("Finished processing " + str(entity_count) + " entities\r" , end ='')

        else:
            mismatched_count = mismatched_count + 1

    print("\033[K",end='') 
    print("Entities embedded: "  + str(entity_count))
    print("Unmatched entities: " + str(mismatched_count))

    entity_file.close()
    vector_file.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")