# README

These files contain the code necessary to replicate the results in *A Natural Language Processing Approach to Assessing Treatment Adherence and Consistency Using Semantic Similarity.*

While the files contained in the folder, **teachsim**, are ideosyncratic to the TeachSIM context, the files contained in **library** will be of general use to readers wishing to apply semantic similarity to their contexts.


The files assume the following directory structure:

docsim
|
data
    |_ raw
    |_ clean
results
    |_ raw
    |_ clean
|
setup.py
|
docsim
    |
    --library
    |
    --teachsim


where scripts in **library** are locally installed. To do that, navigate to the docsim folder in your terminal. Then run: "pip install -e .".

You should customize the location of your files in **start.py**.

# General-Use Files
The most useful functions in the library include:

vectorize_text - Takes dataframe of text and returns a document term matrix 
cosine_similarity_row - Calculates similarity between two rows of doc-term dataframe


Other potentially useful functions:

import_text - Saves plain text from a folder containing transcripts stored in docx files. This function assumes that each new paragraph is a new speaker.





# Replication Files
The replication files need to be run in order: 01_vectorizations.py, 02_tables.py, 03_figures.py, methodological_appendix.py. 

The replication files require one restricted file to run -- text_transcripts.csv. Though we do not include the raw text in that file, we do include a template file for demonstration. 




