from fastapi import logger
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import umap  #visuelisation des vecteurs


def classification_DBSCAN(embedded_vectors, minPts=3, eps=0.5):
    """
    Classifie les vecteurs embarqués avec DBSCAN.
    Retourne les labels de clusters.
    """
    X = np.array(embedded_vectors)
    dbscan = DBSCAN(eps=eps, min_samples=minPts)
    labels = dbscan.fit_predict(X)
    
    plot_clusters(embedded_vectors, labels)  # Affiche les clusters
    logger.info((f"Nombre de clusters trouvés : {len(set(labels)) - (1 if -1 in labels else 0)}"))
    
    return labels


def plot_clusters(embedded_vectors, labels):  # visuellement moins précis car on ne garde que 2 dimensions pour la visualisation
    """
    Affiche un graphique 2D (UMAP) des vecteurs embarqués, colorés par cluster.
    """
    embedded_vectors = np.array(embedded_vectors)
    labels = np.array(labels)

    # Réduction à 2D uniquement pour visualisation
    reducer = umap.UMAP(n_components=2, random_state=42)
    vectors_2d = reducer.fit_transform(embedded_vectors)

    plt.figure(figsize=(10, 6))
    palette = sns.color_palette('husl', len(set(labels)) - (1 if -1 in labels else 0))
    colors = [palette[label] if label != -1 else (0, 0, 0) for label in labels]

    plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], c=colors, s=50, edgecolor='k')
    plt.title("Clusters UMAP (2D) + DBSCAN")
    plt.xlabel("UMAP Dimension 1")
    plt.ylabel("UMAP Dimension 2")
    plt.grid(True)
    plt.show()
