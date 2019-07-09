
def main():
    mapping_file_name = "sgdid_to_systematic_map.lst"
    input_actions_file_name = "../datasets/4932.protein.actions.v11.0.txt"
    output_actions_file_name = "../datasets/protein_actions.lst"
    unmapped_proteins_file_name = "unmapped_proteins.lst"

    mapping = dict()
    unmapped_proteins = set()

    # Load mapping table between systematic to SGD IDs. Place each mapping into dict
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
    

    # Iterate through file of actions. Find all interactions of the following types:
    #   activation, binding, catalysis, reaction, inhibition
    # Convert the identifiers of the proteins associated with these actions to SGD IDs.

    # Keep track of number of each action type found in a dict {<type>:<count>}
    action_types = {'activation':0, 'binding':0, 'catalysis':0, 'reaction':0, 'inhibition':0}

    converted_actions = set()
    unconverted_action_count = 0

    with open(input_actions_file_name, 'r') as f:
        next(f) #skip column header
        for line in f:
            line_data = line.split()
            protein1 = line_data[0].split('.')[1]
            protein2 = line_data[1].split('.')[1]
            action = line_data[2]

            # Ensure that both proteins have entries in the mapping table.
            if (protein1 not in mapping):
                unmapped_proteins.add(protein1)
            if (protein2 not in mapping):
                unmapped_proteins.add(protein2)

            if ((protein1 in mapping) and (protein2 in mapping) and (action in action_types)):
                protein1 = mapping[protein1]
                protein2 = mapping[protein2]
                action_types[action] = action_types[action] + 1
                converted_actions.add(protein1 + ' ' + protein2 + ' ' + action)
            else:
                unconverted_action_count = unconverted_action_count + 1

    print("Proteins with no mapping: " + str(len(unmapped_proteins)))
    print("Proteins actions converted: " + str(len(converted_actions)))
    print("Number of each action type: " + str(action_types))




    print("Proteins actions not converted: " + str(unconverted_action_count))

    with open(output_actions_file_name, 'w') as f:
        for actions in converted_actions:
            f.write(actions + '\n')

    # If any proteins were found to have no mapping, export them in a file to allow for easy manual updating of the mapping.
    if (len(unmapped_proteins) > 0):
        with open(unmapped_proteins_file_name, 'w') as f:
            for protein in unmapped_proteins:
                f.write(protein + '\n')



if __name__ == '__main__':
    main()