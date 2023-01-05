# ADV Library

ADVLib is a basic library and command line tool for importing custom embeddings into Labelbox.

## Building

The build a distributable whl file:
```poetry build```


## Installation

If you have a whl file, installing is easy:

```pip install advtool-0.1.0-py3-none-any.whl```

## Setup

In order to use this script you must have a Labelbox API key stored in the environment 
one of two ways

   * LABELBOX_API_KEY - The API key itself
   * LABELBOX_API_KEY_FILE - The path to a file containing the Labelbox API key.

## Usage

Before we begin with usage, it's important to note that you must upload at least 1000
feature vectors for similarity search to function in Catalog.

To create a custom embedding type:

```advtool embeddings create test1 1024```

This will output the ID.

Now use the ID to import an NDJson file in the format of
{"id": <drid>, "vector": [some floats]}

```advtool embeddings import 98875a54-4ab8-4172-875a-544ab881726c  /Users/mrc/src/intelligence/packages/datavault/adv/benchmark/output2.ndjson```

You can get a count of the number of feature vectors imported.

```advtool embeddings count 98875a54-4ab8-4172-875a-544ab881726c```

You also get a list of all available Embedding types.

```advtool embeddings list```


