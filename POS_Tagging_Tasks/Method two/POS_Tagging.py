import sys
from collections import defaultdict

# prior_prop['DT'] = {'the':1500, 'a':200', ...}
prior_prop = defaultdict(dict)
# transition['DT'] = {'NN':500, 'NNP': 200, ...}
transition = defaultdict(dict)
END_STATE = 'End_Sent'
START_STATE = 'Begin_Sent'
pos_list = [START_STATE]
unknown = set()
known = set()
known_pos = set()
LIKELIHOOD_UNKNOWN = 0.001


def preprocess(file_path):
    with open(file_path, 'r', encoding= 'UTF-8') as f:
        cur_state = START_STATE
        while True:
            line = f.readline()
            if not line:
                break
            line = line.replace('\n', '')
            line = line.split()
            if len(line) == 0:
                freq = transition[cur_state]
                if END_STATE in freq:
                    freq[END_STATE] += 1
                else:
                    freq[END_STATE] = 1
                cur_state = START_STATE
                continue
            token, pos = line
            #token = token
            if token in unknown:
                unknown.remove(token)
            else:
                if token not in known:
                    unknown.add(token)
                    known.add(token)
            freq = prior_prop[pos]
            if token in freq:
                freq[token] += 1
            else:
                freq[token] = 1
            freq = transition[cur_state]
            if pos in freq:
                freq[pos] += 1
            else:
                freq[pos] = 1
            cur_state = pos
            if pos not in known_pos:
                known_pos.add(pos)
                pos_list.append(pos)
        pos_list.append(END_STATE)


def convert_to_prop(dict_name):
    for key, value in dict_name.items():
        total = sum(value.values())
        for sub_key in value.keys():
            value[sub_key] /= total


def make_prediction(f, words):
    # make prediction according to the words and write it to f file
    n = len(words)  #
    m = len(pos_list)   # number of POS
    backpointer = [[0 for _ in range(n)] for _ in range(m)]
    viterbi = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        if i == 0:
            viterbi[0][0] = 1
        elif i == n-1:
            cur_max = 0
            cur_pos = 0
            for j in range(1, m-1):
                if END_STATE not in transition[pos_list[j]]:
                    prop = 0
                else:
                    prop = viterbi[j][i-1]*transition[pos_list[j]][END_STATE]
                if prop > cur_max:
                    cur_max = prop
                    cur_pos = j
            viterbi[m-1][i] = cur_max
            backpointer[m-1][i] = cur_pos
        elif i == 1:
            for j in range(1, m-1):
                #print(pos_list[j], words[i])
                if pos_list[j] not in transition[START_STATE]:
                    viterbi[j][1] = 0
                else:
                    if words[i] not in known:
                        viterbi[j][1] = transition[START_STATE][pos_list[j]]\
                                            * LIKELIHOOD_UNKNOWN
                    else:
                        if words[i] not in prior_prop[pos_list[j]]:
                            viterbi[j][1] = 0
                        else:
                            viterbi[j][1] = transition[START_STATE][pos_list[j]]\
                                            * prior_prop[pos_list[j]][words[i]]
        else:
            for j in range(1, m-1):
                cur_max = 0
                cur_pos = 0
                for p in range(1, m-1):
                    if pos_list[j] not in transition[pos_list[p]]:
                        prop = 0
                    else:
                        if words[i] not in known:
                            prop = viterbi[p][i-1]*transition[pos_list[p]][pos_list[j]]*LIKELIHOOD_UNKNOWN
                        else:
                            if words[i] not in prior_prop[pos_list[j]]:
                                prop = 0
                            else:
                                prop = viterbi[p][i-1]*transition[pos_list[p]][pos_list[j]]\
                                       * prior_prop[pos_list[j]][words[i]]
                    if prop > cur_max:
                        cur_max = prop
                        cur_pos = p
                viterbi[j][i] = cur_max
                backpointer[j][i] = cur_pos
    cur_pos = m-1
    pos_out = [0 for _ in range(n-2)]
    for t in range(n-1, 1, -1):
        pos = backpointer[cur_pos][t]
        cur_pos = pos
        pos_out[t-2] = pos_list[pos]
    for t in range(1, n-1):
        f.write(words[t]+'\t'+pos_out[t-1]+'\n')
    f.write('\n')


def predict(test_file):
    out_file = 'submission.pos'
    f_out = open(out_file, 'w')
    with open(test_file, 'r') as f:
        words = [START_STATE]
        while True:
            line = f.readline()
            if not line:
                break
            line = line.replace('\n', '')
            if len(line) == 0:
                # Finished a whole sentence
                words.append(END_STATE)
                make_prediction(f_out, words)
                words = [START_STATE]
                continue
            words.append(line)
    f_out.close()


if __name__ == '__main__':
    n = len(sys.argv)
    if n < 3:
        print("invalid input file structure")
        exit(0)
    input_file_list = []
    for i in range(1, n-1):
        input_file_list.append(sys.argv[i])
    for file_path in input_file_list:
        preprocess(file_path)
    convert_to_prop(prior_prop)
    convert_to_prop(transition)
    test_file = sys.argv[-1]
    predict(test_file)

