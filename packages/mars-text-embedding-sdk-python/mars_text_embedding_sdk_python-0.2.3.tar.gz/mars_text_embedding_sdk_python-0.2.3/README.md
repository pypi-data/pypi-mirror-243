# Example
```python
from mars_text_embedding_sdk_python import EmbeddingSDK, KeyValue, Object

## Create the caller object to end point
sdk = EmbeddingSDK("http://127.0.0.1:4000/graphql")

## Create objects consisting of KeyValues
objects = [
    Object(
        key_values=[
            KeyValue(key="hello", value="world"),
            KeyValue(key="hello", value="world"),
            KeyValue(key="you", value="are"),
        ],
    ),
    Object(
        key_values=[
            KeyValue(key="you", value="are"),
            KeyValue(key="cool", value="beans"),
            KeyValue(key="cool", value="beans"),
        ]
    )
]

# Make the call and extract data 
# If something goes wrong here, check the .error property instead. .data will be None.
emb_comp = sdk(objects, dims=300).data

# Now, use to_arrays aggregation function to, for instance, aggregate embeddings to their mean
arrs = emb_comp.to_arrays(lambda x: x.mean(axis=0))
```