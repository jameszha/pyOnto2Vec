# pyOnto2Vec

## Introduction
(Mostly) Python re-implementation of Onto2Vec. The functionality of these scripts remain unchanged; however, these implementations are largely more efficient, output useful statistics, and are in Python (need we say more?). 

Based on the paper: *Onto2Vec: joint vector-based representation of biological entities and their ontology-based annotations* by Fatima Zohra Smaili, Xin Gao, and Robert Hoehndorf. 2018. https://academic.oup.com/bioinformatics/article/34/13/i52/5045776

The original version in Perl can be found at: https://github.com/bio-ontology-research-group/onto2vec/

## Dependencies
```
Groovy
Python
gensim
```
## How to
- First, obtain the necessary datasets. You will need:
  - A gene ontology. This should be in ```.owl``` format.
  - Gene ontology annotations for the proteins to be embedded. This should be in ```.gaf``` format.
- Extract the existing axioms and inferring new axioms from the gene ontology:
  ```
  groovy get_axioms.groovy <ontology_file.owl>
  ```
- Extract the annotation axioms from the ```.gaf``` file:
  ```
  python get_annotations.py <annotations.gaf>
  ```
- You should now have:
  - ```axioms.lst```, which contains a list of all *SubsetOf*, *EquivalentTo*, and *DisjointWith* axioms found in the ```<ontology_file.owl>```.
  - ```classes.lst```, which contains a list of all classes found in the ```<ontology_file.owl>```.
  - ```annotations.lst```, which contains a list of all annotation axioms found in the ```<annotations.gaf>```.
  - ```proteins.lst```, which contains a list of all proteins found in the ```<annotations.gaf>```.
- *Optional:* Filter the ```proteins.lst``` to keep only the desired proteins. Or leave it unmodified to generate embeddings for all the proteins
- *Optional:* Add additional ancestor axioms by connecting the proteins to the ancestors of the classes with which the proteins are already annotated. This can be done for only direct parents:
  ```
  python get_ancestors_single.py
  ```
  or the annotations can be propogated up the entire ontology:
  ```
  python get_ancestors_full.py
  ```
- Combine gene ontology axioms with the annotations axioms:
  ```
  cat axioms.lst annotations.lst > all_axioms.lst
  ```
- Generate embeddings for your proteins:
  ```
  python word2vec.py <all_axioms.lst> <proteins.lst> <vectors.lst>
  ```
- The ```<vectors.lst>``` now contains embeddings for each of the proteins, with one protein per row. The first column contains the name of the protein. The remaining columns are the elements of the vector.

## Precomputed embeddings
Embeddings for certain species have already been generated. The embeddings, as well as the datasets used to generate them, can be found under ```/data/```.

The following species are included:
- Yeast


