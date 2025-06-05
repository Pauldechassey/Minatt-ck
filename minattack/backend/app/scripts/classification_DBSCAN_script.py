import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend - MUST be before other matplotlib imports

import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import umap
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def classification_DBSCAN(embedded_vectors, minPts=3, eps=0.3, save_plot=True):
    """
    Classifie les vecteurs embarqués avec DBSCAN.
    Retourne les labels de clusters.
    
    Args:
        embedded_vectors: Vecteurs à classifier
        minPts: Nombre minimum de points pour former un cluster
        eps: Distance maximum entre deux échantillons pour qu'ils soient considérés comme voisins
        save_plot: Si True, sauvegarde le graphique au lieu de l'afficher
        output_dir: Répertoire où sauvegarder les graphiques
    """
    output_dir="static/cluster_plots"
    try:
        X = np.array(embedded_vectors)
        logger.info(f"Classification DBSCAN avec {len(X)} vecteurs (dim: {X.shape[1]})")
        
        dbscan = DBSCAN(eps=eps, min_samples=minPts)
        labels = dbscan.fit_predict(X)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        logger.info(f"Nombre de clusters trouvés : {n_clusters}")
        logger.info(f"Nombre de points de bruit : {n_noise}")
        
        if save_plot:
            plot_path = plot_clusters_save(embedded_vectors, labels, output_dir=output_dir)
            if plot_path:
                logger.info(f"Graphique sauvegardé : {plot_path}")
        else:
            logger.info("Visualisation désactivée (mode non-interactif)")
        
        # Convertir en liste Python pour éviter les problèmes avec numpy arrays
        return labels.tolist()
        
    except Exception as e:
        logger.error(f"Erreur lors de la classification DBSCAN: {e}")
        raise

def plot_clusters_save(embedded_vectors, labels, output_dir="cluster_plots"):
    """
    Sauvegarde un graphique 2D (UMAP) des vecteurs embarqués, colorés par cluster.
    Retourne le chemin du fichier sauvegardé.
    """
    try:
        embedded_vectors = np.array(embedded_vectors)
        labels = np.array(labels)
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Réduction à 2D uniquement pour visualisation
        logger.info("Réduction UMAP en cours...")
        reducer = umap.UMAP(n_components=2, random_state=42)
        vectors_2d = reducer.fit_transform(embedded_vectors)
        
        # Configuration du graphique
        plt.figure(figsize=(12, 8))
        
        # Palette de couleurs
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters > 0:
            palette = sns.color_palette('husl', n_clusters)
            # Mapper les labels aux couleurs
            unique_labels = sorted(list(set(labels)))
            color_map = {}
            color_idx = 0
            for label in unique_labels:
                if label == -1:
                    color_map[label] = (0.5, 0.5, 0.5)  # Gris pour le bruit
                else:
                    color_map[label] = palette[color_idx]
                    color_idx += 1
        else:
            color_map = {-1: (0.5, 0.5, 0.5)}
        
        colors = [color_map[label] for label in labels]
        
        # Créer le scatter plot
        scatter = plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], 
                            c=colors, s=50, edgecolor='k', alpha=0.7)
        
        # Configuration du graphique
        plt.title(f"Clusters UMAP (2D) + DBSCAN\n{n_clusters} clusters, {list(labels).count(-1)} points de bruit", 
                 fontsize=14, fontweight='bold')
        plt.xlabel("UMAP Dimension 1", fontsize=12)
        plt.ylabel("UMAP Dimension 2", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Ajouter une légende
        if n_clusters > 0:
            legend_elements = []
            for label in sorted(set(labels)):
                if label == -1:
                    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                                    markerfacecolor=(0.5, 0.5, 0.5), 
                                                    markersize=8, label='Bruit'))
                else:
                    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                                    markerfacecolor=color_map[label], 
                                                    markersize=8, label=f'Cluster {label}'))
            
            plt.legend(handles=legend_elements, loc='best', framealpha=0.9)
        
        # Sauvegarde avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dbscan_clusters_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close() 
        
        logger.info(f"Graphique sauvegardé avec succès: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du graphique: {e}")
        plt.close()  # S'assurer que la figure est fermée même en cas d'erreur
        return None
