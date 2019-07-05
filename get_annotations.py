# get_annotations
# Get annotations from input.gaf and write to output.lst
# Author: James Zhang (jameszha@andrew.cmu.edu)

import re
import sys
import time

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_annotations.py <input.gaf>")
        exit()

    gaf_file_name = sys.argv[1]
    annotations_file_name = "annotations.lst"
    proteins_file_name = "proteins.lst"

    gaf_file = open(gaf_file_name,'r')
    annotations_file = open(annotations_file_name, 'w')

    annotation_count    = 0
    ignored_count       = 0

    protein_list = set()

    for line in gaf_file:

        line_data = line.split('\t')
        line_data = list(filter(None, line_data)) 

        if (line_data[0][0] != '!'): # Ignore header lines
            # Filter out annotations with no experimental data, e.g. those labeled with IEA and ND
            if (("IEA" in line_data) or ("ND" in line_data)):
                ignored_count = ignored_count + 1

            # Add good annotation to output annotations file
            elif (line_data[3].startswith("GO:")):
                protein_name = line_data[1]
                protein_list.add(protein_name)
                
                annotations_file.write(protein_name + " hasFunction " + line_data[3].replace(':', '_') + '\n')
                annotation_count = annotation_count + 1

    # Write out list of all proteins found
    with open(proteins_file_name, 'w') as f:
        for protein in protein_list:
            f.write("%s\n" % protein)

    gaf_file.close()
    annotations_file.close()

    print("Annotations found:       "    + str(annotation_count))
    print("Annotations ignored:     "  + str(ignored_count))
    print("Unique Proteins found:   "    + str(len(protein_list)))


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time taken: " + str(time.time() - start_time) + " seconds")