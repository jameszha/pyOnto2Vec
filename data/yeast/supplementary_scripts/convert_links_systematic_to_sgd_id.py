
def main():
    mapping_file_name = "sgdid_to_systematic_map.lst"
    input_links_file_name = "4932.protein.links.v11.0.txt"
    output_links_file_name = "protein_links.lst"
    unmapped_proteins_file_name = "unmapped_proteins.lst"

    
    unconverted_link_count = 0


    mapping = dict()
    unmapped_proteins = set()

    with open(mapping_file_name, 'r') as f:
        for line in f:
            line_data = line.split()
            if (len(line_data) == 2):
                sgdid = line_data[0]
                systematic = line_data[1]
                if (systematic in mapping): print("Duplicate: " + systematic)
                mapping[systematic] = sgdid
            else:
                sgdid = line_data[0]
                unmapped_proteins.add(sgdid)

    print("Proteins in mapping: " + str(len(mapping)))
    

    converted_links = set()

    with open(input_links_file_name, 'r') as f:
        next(f) #skip column header
        for line in f:
            line_data = line.split()
            protein1 = line_data[0].split('.')[1]
            protein2 = line_data[1].split('.')[1]
            value = line_data[2]

            if (protein1 not in mapping):
                unmapped_proteins.add(protein1)
            if (protein2 not in mapping):
                unmapped_proteins.add(protein2)

            if ((protein1 in mapping) and (protein2 in mapping)):
                protein1 = mapping[protein1]
                protein2 = mapping[protein2]
                converted_links.add(protein1 + ' ' + protein2 + ' ' + value)
            else:
                unconverted_link_count = unconverted_link_count + 1

    print("Proteins with no mapping: " + str(len(unmapped_proteins)))
    print("Proteins links converted: " + str(len(converted_links)))
    print("Proteins links not converted: " + str(unconverted_link_count))

    with open(output_links_file_name, 'w') as f:
        for link in converted_links:
            f.write(link + '\n')

    with open(unmapped_proteins_file_name, 'w') as f:
        for protein in unmapped_proteins:
            f.write(protein + '\n')



if __name__ == '__main__':
    main()