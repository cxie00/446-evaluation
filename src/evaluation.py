import math


qrels = "C:/Users/chloe/cs446/5evaluation/evaluation-data/qrels"
bm25 = "C:/Users/chloe/cs446/5evaluation/evaluation-data/bm25.trecrun"
ql = "C:/Users/chloe/cs446/5evaluation/evaluation-data/ql.trecrun"
sdm = "C:/Users/chloe/cs446/5evaluation/evaluation-data/sdm.trecrun"
stress = "C:/Users/chloe/cs446/5evaluation/evaluation-data/stres.trecrun"
#  trecrun also a map of { query_id : [ (docid, rankings) ] }
def map_trec(trecrun_file):
    L = {}
    with open(trecrun_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        tokens = line.split()
        query_id = tokens[0]
        doc_id = tokens[2]
        ranking = tokens[3]
        if query_id in L:
            L[query_id].append((doc_id, ranking))
        else:
            L[query_id] = [(doc_id, ranking)]
    return L

# { query_id : { docid : relevance } }
# qrels
def map_qrels(qrels_file):
    R = {}
    with open(qrels_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()  
    for line in lines:
        tokens = line.split()
        query_id = tokens[0]
        doc_id = tokens[2]
        rel = tokens[3]        
        if query_id in R:
            R[query_id][doc_id] = rel
        else:
            R[query_id] = {doc_id:rel}
    return R

    # for query_id in L:
    #     print (f'key: {query_id}\n value: {L[query_id]}')
    #     print("\n")
# L: { query_id : [ (docid, rankings) ] } maps to trecruns, ranked list of retrieved results
# R: { query_id : { docid : relevance } } maps to qrels,  a sortable map of relevant document to judgment values
def recall(trecrun, qrels):
    L = map_trec(trecrun)
    R = map_qrels(qrels)
    num_relevant_docs = 0
    for query_id in L:
        for (doc_id, rank) in L[query_id]:
            if R[query_id] and R[query_id][doc_id] == 1: # check if query_id exists in R first then...
                num_relevant_docs += 1
    return num_relevant_docs / len(R)

# recall (bm25, qrels)

def precision_k(trecrun,qrels,k):
    # k here is the number of top retrieved documents we need to check  for precision.   
    L = map_trec(trecrun)
    R = map_qrels(qrels)
    num_relevant_docs = 0
    for query_id in range(min(len(L), k)):
        for (doc_id, rank) in L[query_id]:
            if R[query_id] and R[query_id][doc_id] == 1: # check if query_id exists in R first then...
                num_relevant_docs += 1
    precision = num_relevant_docs/k
    return precision

# L: { query_id : [ (docid, rankings) ] } maps to trecruns, ranked list of retrieved results
# R: { query_id : { docid : relevance } } maps to qrels,  a sortable map of relevant document to judgment values
# def NCDG(trecrun, qrels, k):
#     L = map_trec(trecrun)
#     R = map_qrels(qrels)

#     ideal_vals = R.values().sort(reverse = True)
#     rankings_to_k = L[:k]
#     dcg = R.get(L[0])
#     if not dcg:
#         dcg = 0
#     idcg = ideal_vals[0]
#     for i in range(min(len(L),k)):
#         dcg += R.get(L[i], 0) / math.log((i+1), 2)
#         idcg += ideal_vals[i]/math.log((i+1), 2)
#     if idcg > 0:
#         return dcg/idcg
#     return 0

# L: { query_id : [ (docid, rankings) ] } maps to trecruns, ranked list of retrieved results
# R: { query_id : { docid : relevance } } maps to qrels,  a sortable map of relevant document to judgment values
"""
 
"""
def RR(trecrun,qrels):
    L = map_trec(trecrun)
    R = map_qrels(qrels)
    i = 0
    while i < len(L):
        if R[L[i]] != None:
            break
        i += 1
    if i < len(L):
       return (1/L[i])
    else:
       return 0