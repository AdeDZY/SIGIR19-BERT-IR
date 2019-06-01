import argparse
import string
import json
import re
import random


def get_passages(text, plen, overlap):
    words = text.split(' ')
    s, e = 0, 0
    passages = []
    while s < len(words):
        e = s + plen
        if e >= len(words):
            e = len(words)
        p = ' '.join(words[s:e])
        passages.append(p)
        s = s + plen - overlap
    return passages


def gen_passage_from_trec_json_file(file_path, plen, overlap):
    for line in open(file_path):
        # a line:
        # qid Q0 docid doc-rank doc-score runname # {"doc":{"body": "body contents ...."}}

        items = line.split('#')
        trec_str = items[0]
        json_str = '#'.join(items[1:])
        json_dict = json.loads(json_str)
        body_text = json_dict['doc']['body']
        qid, _, docid, r, s, _ = trec_str.strip().split(' ')

        # clean body text: remove "-------" and "       "
        body_text = re.sub(r'----*', '---', body_text)
        body_text = re.sub(r'  *', ' ', body_text)

        # split the body text into passages
        passages = get_passages(body_text, plen, overlap)

        # To speed up, we use at most 30 passages from a document.
        # we always use the first passage and the last passage.
        # we random sample the rest 28 passages
        if len(passages) > 30:
            passages = [passages[0]] + random.sample(passages[1:-1], 28) + [passages[-1]]

        # we generate a new trec_json file of the passages
        # a line
        # qid Q0 docid-passageid doc-rank doc-score # {"doc":{"body": "passage contents ..."}}
        for i, passage in enumerate(passages):
            passage_id = docid + "_passage-{0}".format(i)
            json_dict['doc']['body'] = passage
            json_str = json.dumps(json_dict)
            print "{} Q0 {} {} {} passage # {}".format(qid, passage_id, r, s, json_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("trec_json_file")
    parser.add_argument("--plen", type=int, default=150, help="passage length")
    parser.add_argument("--overlap", type=int, default=75, help="overlap length")
    args = parser.parse_args()

    gen_passage_from_trec_json_file(args.trec_file, args.plen, args.overlap)