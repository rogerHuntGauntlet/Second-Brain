Upsert data
This page shows you how to upsert records into a namespace in an index. Namespaces let you partition records within an index and are essential for implementing multitenancy when you need to isolate the data of each customer/user.

If a record ID already exists, upserting overwrites the entire record. To update only part of a record, use the update operation instead.

Pinecone is eventually consistent, so there can be a slight delay before new or changed records are visible to queries. See Understanding data freshness to learn about data freshness in Pinecone and how to check the freshness of your data.

​
Upsert limits
Metric	Limit
Max upsert size	2MB or 1000 records
Max metadata size per record	40 KB
Max length for a record ID	512 characters
Max dimensionality for dense vectors	20,000
Max non-zero values for sparse vectors	1000
Max dimensionality for sparse vectors	4.2 billion
When upserting larger amounts of data, it is recommended to upsert records in large batches. A batch of upserts should be as large as possible (up to 1000 records) without exceeding the maximum request size of 2MB.

To understand the number of records you can fit into one batch based on the vector dimensions and metadata size, see the following table:

Dimension	Metadata (bytes)	Max batch size
386	0	1000
768	500	559
1536	2000	245
​
Upsert records
​
External embedding
When upserting into an index for vectors created with an external embedding model, you use the upsert operation and send vectors directly.

Format the request body as records, each with the following:

An id field with a unique record identifier for the index namespace.
A values field with the dense vector values.
Optionally, a metadata field with key-value pairs to store additional information or context. When you query the index, you can then filter by metadata to ensure only relevant records are scanned. This can reduce latency and improve the accuracy of results. For more information, see Metadata Filtering.
Optionally, a sparse_values field with sparse vector values. This allows you to perform hybrid search](/guides/data/understanding-hybrid-search), or semantic and keyword search, in one query for more relevant results. For more information, see Upsert sparse-dense vectors.
Also specify the namespace to upsert into. If the specified namespace doesn’t exist, it is created. To use the default namespace, set the namespace to an empty string ("").


Python

JavaScript

Java

Go

C#

curl

from pinecone.grpc import PineconeGRPC as Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

index.upsert(
  vectors=[
    {
      "id": "A", 
      "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
      "metadata": {"genre": "comedy", "year": 2020}
    },
    {
      "id": "B", 
      "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
      "metadata": {"genre": "documentary", "year": 2019}
    },
    {
      "id": "C", 
      "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
      "metadata": {"genre": "comedy", "year": 2019}
    },
    {
      "id": "D", 
      "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
      "metadata": {"genre": "drama"}
    }
  ],
  namespace="example-namespace"
)
​
Integrated embedding
When upserting into index with integrated embedding, you use the upsert_records operation and send source text, which Pinecone converts to vectors automatically using the hosted embedding model associated with the index.

Format the request body as records, each with the following:

An _id field with a unique record identifier for the index namespace. id can be used as an alias for _id.
A field with the text for embedding. This field must match the field_map specified in the index.
Additional fields will be stored as record metadata and can be returned in search results or used to filter search results.
For example, the following code converts the sentences in the source_text fields to sparse vectors and then upserts them into example-namespace in example-index. The additional category field is stored as metadata.


Python

curl

# pip install --upgrade "pinecone[grpc]" "pinecone-plugin-records"
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

# Upsert records into a namespace
# `source_text` fields will be converted to vectors
# `category` fields will be stored as metadata
index.upsert_records(
    "example-namespace",
    [
        {
            "_id": "rec1",
            "source_text": "Apples are a great source of dietary fiber, which supports digestion and helps maintain a healthy gut.",
            "category": "digestive system", 
        },
        {
            "_id": "rec2",
            "source_text": "Apples originated in Central Asia and have been cultivated for thousands of years, with over 7,500 varieties available today.",
            "category": "cultivation",
        },
        {
            "_id": "rec3",
            "source_text": "Rich in vitamin C and other antioxidants, apples contribute to immune health and may reduce the risk of chronic diseases.",
            "category": "immune system",
        },
        {
            "_id": "rec4",
            "source_text": "The high fiber content in apples can also help regulate blood sugar levels, making them a favorable snack for people with diabetes.",
            "category": "endocrine system",
        },
    ]
) 
​
Upsert in batches
When upserting larger amounts of data, it is recommended to upsert records in large batches. This should be as large as possible (up to 1000 records) without exceeding the maximum request size of 2MB. To understand the number of records you can fit into one batch, see the Upsert limits section.


Python

JavaScript

Java

Go

import random
import itertools
from pinecone.grpc import PineconeGRPC as Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

def chunks(iterable, batch_size=200):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

vector_dim = 128
vector_count = 10000

# Example generator that generates many (id, vector) pairs
example_data_generator = map(lambda i: (f'id-{i}', [random.random() for _ in range(vector_dim)]), range(vector_count))

# Upsert data with 200 vectors per upsert request
for ids_vectors_chunk in chunks(example_data_generator, batch_size=200):
    index.upsert(vectors=ids_vectors_chunk) 
​
Upsert in parallel
Send multiple upserts in parallel to help increase throughput. Vector operations block until the response has been received. However, they can be made asynchronously as follows:


Python

JavaScript

Java

Go

import random
import itertools
from pinecone import Pinecone

# Initialize the client with pool_threads=30. This limits simultaneous requests to 30.
pc = Pinecone(api_key="YOUR_API_KEY", pool_threads=30)

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

def chunks(iterable, batch_size=200):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

vector_dim = 128
vector_count = 10000

example_data_generator = map(lambda i: (f'id-{i}', [random.random() for _ in range(vector_dim)]), range(vector_count))

# Upsert data with 200 vectors per upsert request asynchronously
# - Pass async_req=True to index.upsert()
with pc.Index(host="INDEX_HOST", pool_threads=30) as index:
    # Send requests in parallel
    async_results = [
        index.upsert(vectors=ids_vectors_chunk, async_req=True)
        for ids_vectors_chunk in chunks(example_data_generator, batch_size=200)
    ]
    # Wait for and retrieve responses (this raises in case of error)
    [async_result.get() for async_result in async_results]
​
Python SDK with gRPC
Using the Python SDK with gRPC extras can provide higher upsert speeds. Through multiplexing, gRPC is able to handle large amounts of requests in parallel without slowing down the rest of the system (HoL blocking), unlike REST. Moreover, you can pass various retry strategies to the gRPC SDK, including exponential backoffs.

To install the gRPC version of the SDK:

Shell

pip install "pinecone[grpc]"
To use the gRPC SDK, import the pinecone.grpc subpackage and target an index as usual:

Python

from pinecone.grpc import PineconeGRPC as Pinecone

# This is gRPC client aliased as "Pinecone"
pc = Pinecone(api_key='YOUR_API_KEY')  

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")
To launch multiple read and write requests in parallel, pass async_req to the upsert operation:

Python

def chunker(seq, batch_size):
  return (seq[pos:pos + batch_size] for pos in range(0, len(seq), batch_size))

async_results = [
  index.upsert(vectors=chunk, async_req=True)
  for chunk in chunker(data, batch_size=200)
]

# Wait for and retrieve responses (in case of error)
[async_result.result() for async_result in async_results]
It is possible to get write-throttled faster when upserting using the gRPC SDK. If you see this often, we recommend you use a backoff algorithm(e.g., exponential backoffs)
while upserting.

The syntax for upsert, query, fetch, and delete with the gRPC SDK remain the same as the standard SDK.

​
Upsert a dataset as a dataframe
To quickly ingest data when using the Python SDK, use the upsert_from_dataframe method. The method includes retry logic andbatch_size, and is performant especially with Parquet file data sets.

The following example upserts the uora_all-MiniLM-L6-bm25 dataset as a dataframe.

Python

from pinecone import Pinecone, ServerlessSpec
from pinecone_datasets import list_datasets, load_dataset

pc = Pinecone(api_key="API_KEY")

dataset = load_dataset("quora_all-MiniLM-L6-bm25")

pc.create_index(
  name="example-index",
  dimension=384,
  metric="cosine",
  spec=ServerlessSpec(
    cloud="aws",
    region="us-east-1"
  )
)

# To get the unique host for an index, 
# see https://docs.pinecone.io/guides/data/target-an-index
index = pc.Index(host="INDEX_HOST")

index.upsert_from_dataframe(dataset.drop(columns=["blob"]))