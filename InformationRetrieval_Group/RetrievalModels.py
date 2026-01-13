import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

class BM25_Model:

    def __init__(self, documents, text_data, vocabulary, dataframe):

        self.documents = documents
        self.text_data = text_data
        self.vocabulary = vocabulary
        self.dataframe = dataframe
        
        self.k_1 =  1.2
        self.b = 0.75

        self.bm25_dataframe = self.calculate_scores()

# Checked!
    def calculate_scores(self):

        tfs = self.dataframe.div(self.dataframe.sum(axis = 1), axis = 0)
        dfs = (self.dataframe > 0).sum(axis = 0).to_numpy()
        idfs = np.log10(len(self.text_data) / dfs)
        #tf_idf = tfs * idfs

        dls = self.dataframe.sum(axis = 1).to_numpy()  # array of size N where N is the number of documents
        avgdl = np.mean(dls)  # single value

        numerator = np.array((self.k_1 + 1) * tfs)
        denominator = np.array(self.k_1 *((1 - self.b) + self.b * (dls / avgdl))).reshape(-1, 1) + np.array(tfs)

        BM25_tf = numerator / denominator

        BM25_score = idfs * BM25_tf

        bm25_dataframe = pd.DataFrame(BM25_score, columns = self.vocabulary)

        return bm25_dataframe

# Checked!
    def rank_documents(self, q_terms, top_n):

        q_terms_only_df = self.bm25_dataframe[q_terms]

        score_q_d = q_terms_only_df.sum(axis = 1)

        ranked_docs = sorted(zip(enumerate(self.text_data), score_q_d.values),
                     key = lambda tup:tup[1],
                     reverse = True)
        
        if top_n >  len(ranked_docs):

            top_n = len(ranked_docs)
        
        ranked_docs = [doc for doc in ranked_docs if doc[1] > 0]

        ranked_docs = ranked_docs[:top_n]

        for doc in ranked_docs:
          
          print(f'\nScore: {doc[1]:.4f}, Document {doc[0][0]}: "{doc[0][1]}"')
        
        return ranked_docs


class SBERT_Model:

    def __init__(self):

        self.sbert_model = SentenceTransformer('all-mpnet-base-v2')

    
    def rank_documents(self, ranked_docs, query, top_k):

        if top_k > len(ranked_docs):

            top_k = len(ranked_docs)

        doc_texts = [doc[0][1] for doc in ranked_docs]
        
        query_embedding = self.sbert_model.encode(query)

        doc_embeddings = self.sbert_model.encode(doc_texts)

        # Calculating Cosine similarity
        dot_product = np.dot(doc_embeddings, query_embedding)

        doc_norms = np.linalg.norm(doc_embeddings, axis = 1)

        query_norm = np.linalg.norm(query_embedding)

        similarities = dot_product / (doc_norms * query_norm)

        sorted_indices = np.argsort(similarities)[::-1]

        reranked_docs = [(ranked_docs[i][0], similarities[i]) for i in sorted_indices[:top_k]]

        for doc in reranked_docs:

            print(f'\nSemantic Score: {doc[1]:.4f}, Document {doc[0][0]}: "{doc[0][1]}"')

        return reranked_docs