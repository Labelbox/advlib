from advlib.client import ADVClient


class App:
    """
    The base application class for ADVLib.
    """

    def __init__(self, apikey=None):
        self.client = ADVClient(apikey)

    def create_embedding_type(self, name: str, dims: int) -> dict:
        """
        Create a new embedding type.  You must provide a name and the
        number of dimensions the embedding type has.  Once an
        embedding type has been created, you can upload the vector
        data associated with the embedding type id.

        Args:
            name: The name of the embedding type.
            dims: The number of dims

        Returns:
            A dictionary that describes the embedding type.
        """
        payload = {
            "name": name,
            "dims": dims
        }
        return self.client.post("adv/v1/embeddings", payload)

    def get_embedding_types(self) -> list:
        """
        Return a list of all embedding types for the current organization.
        """
        return self.client.get("adv/v1/embeddings")["results"]

    def import_vectors_from_file(self, id: str, path: str, callback=None) -> dict:
        """
        Import vectors into a given embedding type from an NDJSON file.  An
        NDJSON file consists of newline delimited JSON.  Each line of the file
        is valid JSON, but the entire file itself is NOT.  The format of the
        file looks like:

            {"id": DATAROW ID1, "vector": [ array of floats ]}
            {"id": DATAROW ID2, "vector": [ array of floats ]}
            {"id": DATAROW ID3, "vector": [ array of floats ]}

        The vectors are added to the system in an async manner and it may take
        up to a couple minutes before they are usable via similarity search. Note
        that you also need to upload at least 1000 vectors in order for similarity
        search to be activated.

        Args:
            id: The embedding type id.
            path: The path to the NDJSON file.
            callback: a callback function used get the status of each batch of lines uploaded.

        Returns:
            A dict with some information about the request
        """
        self.client.send_ndjson(f"adv/v1/embeddings/{id}/_import_ndjson", path, callback=callback)

    def get_imported_vector_count(self, id: str) -> int:
        """
        Return the # of vectors actually imported into Labelbox.  This will give you an accurate
        count of the number of vectors written into the vector search system.

        Args:
            id: The embedding type id.

        Returns:
            The number of imported vectors.
        """
        return self.client.get(f"adv/v1/embeddings/{id}/vectors/_count").get("count", 0)
