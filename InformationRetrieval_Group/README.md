# Group Project – Academic Search Engine (Information Retrieval)

## Overview
This group project was completed as part of the MSc module **Information Retrieval**.
The aim was to design and implement a hybrid academic search engine that improves literature discovery by combining traditional lexical retrieval with modern semantic ranking.

## Problem
Academic literature is growing rapidly, making it increasingly difficult for researchers to find relevant papers using keyword-based search alone. Traditional IR models struggle to capture semantic meaning, while purely neural approaches are often too computationally expensive.

## Approach
- Implemented a **two-stage hybrid retrieval pipeline**
  - **BM25** for initial candidate retrieval
  - **SBERT** for semantic re-ranking
- Indexed a large academic corpus (arXiv dataset)
- Applied NLP preprocessing (tokenisation, stop-word removal, stemming)
- Evaluated retrieval quality using **MAP**, **nDCG**, precision, and recall
- Developed a **GUI-based search interface** for usability

## Technologies
- Python
- PyTerrier
- PyTorch
- SBERT
- NLTK
- NumPy, pandas
- Tkinter (GUI)

## Results
- Hybrid BM25 + SBERT approach improved semantic relevance over lexical-only retrieval
- SBERT re-ranking consistently improved top-k document ordering
- System demonstrated effective balance between efficiency and retrieval quality

## My Contributions
- Designed low- and high-fidelity **UI prototypes**
- Implemented the **graphical user interface**
- Contributed to system integration and usability testing
- Participated in evaluation analysis and project coordination

## Repository Notes
The full dataset is not included due to size constraints.
Core retrieval logic, preprocessing, and evaluation scripts are provided.

## Key Skills Demonstrated
- Information retrieval systems
- Hybrid lexical–semantic search
- Evaluation using IR metrics (MAP, nDCG)
- NLP preprocessing pipelines
- Team-based software development
