import umap
import numpy as np

class Embedder:
    """
    Class to embed vectors using UMAP. -> 90D to 10D
    """
    def __init__(self, all_vectors):
        self.umap_model = umap.UMAP(n_components=10, random_state=42)
        self.umap_model.fit(all_vectors)

    def embed(self, vector):
        vector = np.array(vector).reshape(1, -1)
        return self.umap_model.transform(vector)[0]
