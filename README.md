# SIGIR19-BERT-IR
Repo of code and data for SIGIR-19 short paper "Deeper Text Understanding for IR with Contextual NeuralLanguage Modeling"

[Find the paper on arXiv](https://arxiv.org/abs/1905.09217v1)

Abstract: Neural networks provide new possibilities to automatically learn complex language patterns and query-document relations. Neural IR models have achieved promising results in learning query-document relevance patterns, but few explorations have been done on understanding the text content of a query or a document. This paper studies leveraging a recently-proposed contextual neural language model, BERT, to provide deeper text understanding for IR. Experimental results demonstrate that the contextual text representations from BERT are more effective than traditional word embeddings. Compared to bag-of-words retrieval models, the contextual language model can better leverage language structures, bringing large improvements on queries written in natural languages. Combining the text understanding ability with search knowledge leads to an enhanced pre-trained BERT model that can benefit related search tasks where training data are limited.

June 3, 2019: Added codes, links to Google colab, sample input files, and data download links. Will add instructions for running the scripts in this week! -Zhuyun



## Data
Data can be downloaded from our [Virtual Appendix](http://boston.lti.cs.cmu.edu/appendices/SIGIR2019-Zhuyun-Dai/).

The input to the BERT re-ranker is a list of .trec.with_json files. Each line is in the form of: 

`qid Q0 docid ranke score runname # {"doc":{"title":"...", "body":"......"}}`. 

E.g. A document:
```
80 Q0 clueweb09-en0008-49-09144 1 -5.66498569 indri # {doc": {"title": "Personal Keyboards reviews - Keyboard-Reviews.com", "body": "personal keyboards reviews accessories bass guitars , a..."}
```
A passage:
```
80 Q0 clueweb09-en0008-49-09144_passage-0 1 -5.66498569 passage # {"doc": {"title": "Personal Keyboards reviews - Keyboard-Reviews.com", "body": "personal keyboards reviews...}}
```


We release these .trec.with_json files for ClueWeb09-B. We cannot release the document contents of Robust04 documents. 
As an alternative, we provide the inital rankings for ClueWeb09/Robust04 (.trec files). Each line is the format of:

`qid Q0 docid rank score runname`

You need to get the text contents of candidate documents and append them to the trec file in json format
(`{doc":{"title":"...", "body":"......"}}`).  

Once you have generated the .trec.with_json files for documents, you can use the provided passage generation script to generate passages

## Google Colab notebooks to train BERT
You can upload the .trec.with_json files to Google cloud bucket, and directly run the notebooks:
1. [ClueWeb09-B Document Level Train/Inference (BERT-FirstP)](https://colab.research.google.com/drive/1qFGmEz5SZrsGui5HHAmiS_geppJQy8b4)
2. [ClueWeb09-B Passage Level Train/Inference (BERT-MaxP, BERT-SumP)](https://colab.research.google.com/drive/1YAj_yA7R8Sv9QaJkKfjC0sA0vpeEh3dC)
3. Robust04 notebooks Comming Soon.

The output is a file of scores for each document/passage. It need to be aligned with the document/passage ids in the original .trec.with_json file. We provide scripts for this purpose.

## Pre-trained Bing-augmented BERT Model
Some search tasks require both general text understanding (e.g. Honda is a motor company) and more-specific search knowledge (e.g. people want to see special offers about Honda). While pre-trained BERT encodes general language patterns, the search knowledge must be learned from labeled search data.  We follow the domain adaptation setting from our WSDM2018 [Conv-KNRM](http://www.cs.cmu.edu/~zhuyund/papers/WSDM_2018_Dai.pdf) work and augmented BERT with search knowledge from a sample of Bing search log. 

The Bing-augmented BERT model can be downloaded from our [Virtual Appendix](http://boston.lti.cs.cmu.edu/appendices/SIGIR2019-Zhuyun-Dai/)





