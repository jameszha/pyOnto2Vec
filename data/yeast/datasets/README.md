# Yeast Datasets
The following are the download links for the datasets used to generate the yeast embeddings. All of the following sources were downloaded on June 3, 2019.

- GO subset for yeast: http://geneontology.org/docs/go-subset-guide/ 
  (direct link: http://current.geneontology.org/ontology/subsets/goslim_yeast.owl)

- GO protein annotations: http://current.geneontology.org/products/pages/downloads.html 
  (direct link: http://current.geneontology.org/annotations/sgd.gaf.gz)
  
- Protein-protein interactions: https://string-db.org/cgi/download.pl?sessionId=Z7zXym5jIFS7&species_text=Saccharomyces+cerevisiae 
  (direct link: https://stringdb-static.org/download/protein.links.v11.0/4932.protein.links.v11.0.txt.gz)
  
Note that yeast proteins in the protein links file are annotated with their *systematic name*. These can be converted to their *SGD ID*s to match the other datasets using the conversion script and mapping table included in ```/data/yeast/supplementary_scripts/```.
