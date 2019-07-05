# E. Coli Datasets
- ```ecocyc.gaf``` contains GO annotations for yeast proteins.
- ```511145.protein.links.v11.0.txt.gz``` contains (a compressed file of) scored links between pairs of E. coli proteins. Useful for evaluating the generated E. coli embeddings in terms of protein-protein interaction prediction.
  - Uncompress using ```gunzip 511145.protein.links.v11.0.txt.gz```

The following are the download links for the datasets used to generate the E coli. embeddings.

- GO protein annotations: http://current.geneontology.org/products/pages/downloads.html 
  (direct link: http://current.geneontology.org/annotations/ecocyc.gaf.gz)
  
- Protein-protein interactions: https://string-db.org/cgi/download.pl 
  (direct link: https://stringdb-static.org/download/protein.links.v11.0/511145.protein.links.v11.0.txt.gz)
