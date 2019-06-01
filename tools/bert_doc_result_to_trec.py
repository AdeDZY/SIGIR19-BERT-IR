import argparse
import json


def json_to_trec(dataset_file_path,
                 prediction_file_path,
                 output_file_path,
                 run_name="",
                 dataset_format="trec",
                 max_depth=1000):
    """

    :param dataset_file_path: json file
    :param prediction_file_path: json file of predictions
    :param run_name: run name
    :return: None
    """
    dataset = []
    with open(dataset_file_path) as dataset_file:
        for line in dataset_file:
            if dataset_format == "trec":
                line = line.strip()
                items = line.split('#')
                trec_str = items[0]
                qid, _, docid, rank, score, _ = trec_str.strip().split()
                if int(rank) > max_depth:
                    continue
                d = {"qid": qid, "docid": docid}
                dataset.append(d)
            else:
                raise NotImplementedError

    predictions = []
    with open(prediction_file_path) as prediction_file:
        for line in prediction_file:
            p = float(line.split('\t')[1])
            predictions.append(p)

    rankings = {}
    # assert len(dataset) == len(predictions)
    for d, p in zip(dataset, predictions):
        qid, docid = d['qid'], d['docid']
        score = p
        if qid not in rankings:
            rankings[qid] = []
        rankings[qid].append((float(score), docid))

    n_docs = 0
    with open(output_file_path, 'w') as out_file:
        for qid in rankings:
            my_ranking = rankings[qid][0:min(len(rankings[qid]), max_depth)]
            n_docs += len(my_ranking)
            sorted_ranking = sorted(my_ranking, reverse=True)
            for rank, item in enumerate(sorted_ranking):
                score, docid = item
                out_str = "{0}\tQ0\t{1}\t{2}\t{3}\t{4}\n".format(qid, docid, rank + 1, score, run_name)
                out_file.write(out_str)

    print("TREC file written to {0}! {1} queries, {2} docs".format(output_file_path, len(rankings), n_docs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_file', help='Dataset json file')
    parser.add_argument('prediction_file', help='Prediction json File')
    parser.add_argument('output_file', help='Output File')
    parser.add_argument("--dataset_file_format", "-d", type=str, choices=["trec"], default="trec")
    parser.add_argument('--run_name', '-n', default="", help='run name')
    parser.add_argument('--max_rerank_depth', '-M', type=int, default=100)
    args = parser.parse_args()

    json_to_trec(args.dataset_file,
                 args.prediction_file,
                 args.output_file,
                 args.run_name,
                 args.dataset_file_format,
                 args.max_rerank_depth)


