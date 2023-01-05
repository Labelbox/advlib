from advlib.client import ADVClient


class App:

    def __init__(self, apikey=None):
        self.client = ADVClient(apikey)

    def create_embedding_type(self, name: str, dims: int) -> dict:
        payload = {
            "name": name,
            "dims": dims
        }
        return self.client.post("adv/v1/embeddings", payload)

    def get_embedding_types(self) -> list:
        return self.client.get("adv/v1/embeddings")["results"]

    def import_vectors_from_file(self, id: str, path: str, callback=None) -> dict:
        self.client.send_ndjson(f"adv/v1/embeddings/{id}/_import_ndjson", path, callback=callback)

    def get_imported_vector_count(self, id: str) -> int:
        return self.client.get(f"adv/v1/embeddings/{id}/vectors/_count").get("count", 0)
