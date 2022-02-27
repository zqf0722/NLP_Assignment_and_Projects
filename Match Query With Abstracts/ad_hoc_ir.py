from stop_list import closed_class_stop_words
from collections import defaultdict
from scipy import spatial
import math
import os

word_set = set()
index_2_word = {}
index = 0
doc_id_ref = {}
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~+='''


def process1(file_path):
    global index
    #print(index)
    idf = defaultdict(int)
    tf = []
    words = []
    doc_id = 1
    number_of_documents = 0
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.replace('\n', '')
            line = line.split()
            if line[0] == '.I':
                cur_raw_id = line[1]
                doc_id_ref[cur_raw_id] = doc_id
                doc_id += 1
                continue
            elif line[0] == '.W':
                # read in the content
                number_of_documents += 1
                number_of_words = 0
                word_in_this_part = defaultdict(int)
                line = f.readline()
                if not line:
                    break
                line = line.replace('\n', '')
                line = line.split()
                while line[0][0] != '.':
                    number_of_words += len(line)
                    for word in line:
                        for ele in word:
                            if ele in punc:
                                word = word.replace(ele, '')
                            if ele.isdigit():
                                word = word.replace(ele, '')
                        if word not in closed_class_stop_words:
                            if word:
                                word_in_this_part[word] += 1
                                '''
                                if word not in word_2_index:
                                    word_2_index[word] = index
                                    index += 1
                                '''
                                if word not in word_set:
                                    index_2_word[index] = word
                                    index += 1
                                    word_set.add(word)
                    line = f.readline()
                    if not line:
                        break
                    line = line.replace('\n', '')
                    line = line.split()
                if not line:
                    tf.append(word_in_this_part)
                    words.append(number_of_words)
                    for word in word_in_this_part:
                        idf[word] += 1
                    break
                elif line[0] == '.I':
                    cur_raw_id = line[1]
                    doc_id_ref[cur_raw_id] = doc_id
                    doc_id += 1
                tf.append(word_in_this_part)
                words.append(number_of_words)
                for word in word_in_this_part:
                    idf[word] += 1
            else:
                continue
    # idf[word] = number of documents containing('a')
    # number_of_documents = number of documents
    # tf[id] = {'a': number of time term 'a' occurs in document id, ...}
    # words[id] = number of words in document id
    return idf, number_of_documents, tf, words


def compute_cos(vector_query, vector_abstract):
    if sum(vector_abstract) == 0:
        return 0
    value = 1-spatial.distance.cosine(vector_query, vector_abstract)
    #print(value)
    return value


def write_in(query_index, out, out_file):
    with open(out_file, 'a') as f:
        count = 0
        for similarity, abstract_index in out:
            if count == 100:
                break
            to_write = str(query_index) + ' ' + str(abstract_index) + ' ' + str(similarity) + ' \n'
            f.write(to_write)
            count += 1


if __name__ == '__main__':
    query_file = 'cran.qry'
    abstract_file = 'cran.all.1400'
    out_file = 'output.txt'
    if os.path.exists(out_file):
        os.remove(out_file)
    query_idf, number_of_queries, query_tf, query_words = process1(query_file)
    #print(number_of_queries, len(query_words), len(query_tf))
    abstract_idf, number_of_abstract, abstract_tf, abstract_words = process1(abstract_file)
    #print(abstract_words)
    #print(query_idf)
    #print(abstract_idf)
    vector_query = [[0 for _ in range(index)] for _ in range(number_of_queries)]
    vector_abstract = [[0 for _ in range(index)] for _ in range(number_of_abstract)]
    #print(index)
    #print(word_set)
    for i in range(number_of_queries):
        for pos in range(index):
            if query_words[i] == 0:
                tf = 0
            else:
                tf = math.log(query_tf[i][index_2_word[pos]]+1) if query_tf[i][index_2_word[pos]] else 0
            idf = math.log((number_of_queries + 1) / (query_idf[index_2_word[pos]] + 1))
            vector_query[i][pos] = tf * idf
    for i in range(number_of_abstract):
        for pos in range(index):
            if abstract_words[i] == 0:
                tf = 0
            else:
                tf = math.log(abstract_tf[i][index_2_word[pos]]+1) if abstract_tf[i][index_2_word[pos]] else 0
            idf = math.log((number_of_abstract + 1) / (abstract_idf[index_2_word[pos]] + 1))
            vector_abstract[i][pos] = tf * idf
    #print(vector_query[0], vector_abstract[9])
    #exit(0)
    for i in range(1, number_of_queries+1):
        out = []
        for j in range(1, number_of_abstract+1):
            # print(i, j)
            similarity = compute_cos(vector_query[i-1], vector_abstract[j-1])
            out.append((similarity, j))
        out.sort(key=lambda x: x[0], reverse=True)
        #print(out)
        write_in(i, out, out_file)

