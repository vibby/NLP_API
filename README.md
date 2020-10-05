# nalapi

aka NAtural Language API

A simple http api to get results from the excellent NLTK Python Naural Language Processor Toolkit.

Originally forked from https://github.com/William-Lake/NLP-API

# Install

```
pip3 install nltk bottle action vaderSentiment
pip3 install git+https://github.com/vibby/nalapi.git@stable#egg=nalapi
```
Set up NLTK data
```
mkdir -p ~/nltk_data/{chunkers,corpora,taggers,tokenizers}
python3 -c "import nltk; nltk.download(['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words'])"
```

# Usage 

## Launch Server

```python3 nalapi localhost 2330```

## Make a test call

```curl --request GET --header "Content-Type: application/json" --data '{"text":"Once I was alone. Then other words came."}' http://localhost:2330/snt```

Expected Response : 

```JSON
{
    "action": "SentenceExtraction",
    "result": [
        "Once I was alone.",
        "Then other words came."
    ],
    "history": [
        [
            "snt",
            "success"
        ]
    ],
    "original": "Once I was alone. Then they came."
}
```

# Doc

Look at possible actions here : https://github.com/vibby/nalapi/tree/develop/nalapi/action

Nothing more for the moment :P

# Participate

PR are welcome :)
