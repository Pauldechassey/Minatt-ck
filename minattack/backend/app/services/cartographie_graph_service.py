# backend/domain_graph_service.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from dataclasses import dataclass
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.domaine import Domaine 

@dataclass
class GraphNode:
    id: str
    type: str  # 'domaine' ou 'sous_domaine'
    label: str
    description: str
    level: int
    parent_id: str = None
    x: float = 0.0
    y: float = 0.0

@dataclass
class GraphEdge:
    source: str
    target: str
    type: str = "contains"

class DomainGraphService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_graph_data(self, id_domaine: int) -> Dict[str, Any]:
        """
        Récupère toutes les données nécessaires pour construire le graphe
        """
        domaine = self.session.query(Domaine).filter(Domaine.id_domaine == id_domaine).first()
        
        sous_domaines = self.session.query(SousDomaine).filter(
            SousDomaine.id_domaine == id_domaine
        ).order_by(SousDomaine.degre, SousDomaine.id_SD).all()
        
        nodes = []
        edges = []
        
        # Node principal (domaine)
        domaine_node = GraphNode(
            id=f"domaine_{id_domaine}",
            type="domaine",
            label=f"Domaine {domaine.url_domaine}",
            description="Domaine principal",
            level=0,
            x=0.0,  # Position centrale
            y=0.0
        )
        nodes.append(domaine_node)
        
        # nodes des sous-domaines
        for sd in sous_domaines:
            node = GraphNode(
                id=f"sd_{sd.id_SD}",
                type="sous_domaine",
                label=sd.url_SD,
                description=sd.description_SD,
                level=sd.degre,
                parent_id=f"domaine_{id_domaine}" if sd.id_SD_Sous_domaine == 0 else f"sd_{sd.id_SD_Sous_domaine}"
            )
            nodes.append(node)
            
            # Créer les edges
            if sd.id_SD_Sous_domaine == 0:
                # Lien direct avec le domaine
                edge = GraphEdge(
                    source=f"domaine_{id_domaine}",
                    target=f"sd_{sd.id_SD}",
                    type="contains"
                )
            else:
                # lien avec un autre sous-domaine parent
                edge = GraphEdge(
                    source=f"sd_{sd.id_SD_Sous_domaine}",
                    target=f"sd_{sd.id_SD}",
                    type="contains"
                )
            edges.append(edge)
        
        # calcul des positions
        self._calculate_positions(nodes, edges)
        
        return {
            "domaine_id": id_domaine,
            "nodes": [self._node_to_dict(node) for node in nodes],
            "edges": [self._edge_to_dict(edge) for edge in edges]
        }
    
    def _calculate_positions(self, nodes: List[GraphNode], edges: List[GraphEdge]):
        """
        Calcule les positions des nodes pour un affichage radial
        """
        import math
        
        # grouper les nodes par niveau
        levels = {}
        for node in nodes:
            if node.level not in levels:
                levels[node.level] = []
            levels[node.level].append(node)
        
        # domaine au centre
        for node in levels.get(0, []):
            node.x = 0
            node.y = 0
        
        # niveaux en cercles concentriques
        for level, level_nodes in levels.items():
            if level == 0:
                continue
                
            radius = level * 150  # Distance du centre
            angle_step = 2 * math.pi / len(level_nodes) if len(level_nodes) > 1 else 0
            
            for i, node in enumerate(level_nodes):
                angle = i * angle_step
                node.x = radius * math.cos(angle)
                node.y = radius * math.sin(angle)
    
    def _node_to_dict(self, node: GraphNode) -> Dict:
        return {
            "id": node.id,
            "type": node.type,
            "label": node.label,
            "description": node.description,
            "level": node.level,
            "parent_id": node.parent_id,
            "x": node.x,
            "y": node.y
        }
    
    def _edge_to_dict(self, edge: GraphEdge) -> Dict:
        return {
            "source": edge.source,
            "target": edge.target,
            "type": edge.type
        }
