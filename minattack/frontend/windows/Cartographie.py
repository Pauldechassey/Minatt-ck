from PySide6.QtWidgets import QWidget, QMessageBox
import logging

from minattack.frontend.ui.ui_cartographie import Ui_Cartographie

from PySide6.QtGui import QIcon, QPixmap

import minattack.frontend.utils.settings as settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CartographieWindow(QWidget, Ui_Cartographie):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Cartographie()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow

        # Initializing decorative element
        self.ui.pushButtonDeconnexionCartographie.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionCartographie.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilCartographie.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteCartographie.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationCartographie.clicked.connect(
            self.main_window.goToDocumentation
        )

        # Connecting page elemets
        self.ui.pushButtonLancerCartographie.clicked.connect(self.manageCarto)
        self.ui.checkBoxFuzzingCartographie.clicked.connect(
            self.checkFuzzSelect
        )

    def checkFuzzSelect(self):
        if self.ui.checkBoxFuzzingCartographie.isChecked():
            self.ui.lineEditWordlistPathCartographie.setEnabled(True)
        else:
            self.ui.lineEditWordlistPathCartographie.clear()
            self.ui.lineEditWordlistPathCartographie.setEnabled(False)

    def checkAuditStateCartographie(self) -> bool:
        if settings.SELECTED_AUDIT_STATE > 0:
            QMessageBox.warning(
                self,
                "Attention",
                "La cartographie a déjà été effectuée pour cet audit",
            )
            return False
        elif settings.SELECTED_AUDIT_STATE < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Etat de l'audit invalide",
            )
            return False
        else:
            return True

    def updateAuditStateCartographie(self):
        settings.SELECTED_AUDIT_STATE = settings.SELECTED_AUDIT_STATE + 1
        if self.main_window.auditRepo.updateAuditState(
            settings.SELECTED_AUDIT_ID, settings.SELECTED_AUDIT_STATE
        ):
            QMessageBox.information(
                self,
                "Succès",
                "Cartographie réalisée avec succès",
                QMessageBox.StandardButton.Cancel,
            )
            self.main_window.auditsSelectPage.populateComboBox()
            self.main_window.mainStackedWidget.setCurrentIndex(
                self.main_window.mainStackedWidget.indexOf(
                    self.main_window.attaquesPage
                )
            )
        else:
            QMessageBox.warning(
                self,
                "Attention",
                "Cartographie réussie mais erreur lors de la mise à jour de l'état",
            )

    def launchCarto(self, fuzzing: bool, wordlist_path: str):
        if self.main_window.cartoRepo.runCarto(
            settings.SELECTED_AUDIT_ID, fuzzing, wordlist_path
        ):
            self.updateAuditStateCartographie()
        else:
            settings.SELECTED_AUDIT_STATE = settings.SELECTED_AUDIT_STATE - 1
            QMessageBox.critical(self, "Erreur", "La cartographie a échoué")

    def manageCarto(self):
        check = self.checkAuditStateCartographie()
        fuzzing = self.ui.checkBoxFuzzingCartographie.isChecked()
        wordlist_path = self.ui.lineEditWordlistPathCartographie.text()
        if check and fuzzing is False:
            self.launchCarto(fuzzing, "")
        elif check and fuzzing is True:
            self.launchCarto(fuzzing, wordlist_path)


from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math
import random

class GraphWindow(QWidget):
    def __init__(self, graph_data, parent=None):
        super().__init__(parent)
        logger.warning("GraphWindow [START]: Début de l'initialisation")
        
        self.graph_data = graph_data
        logger.warning(f"GraphWindow [DATA]: Données reçues: {type(graph_data)}, contenu: {graph_data}")
        
        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.node_positions = {}
        self.animation_timer = QTimer()
        self.zoom_factor = 1.0
        self.is_3d_mode = False
        self.dragging = False
        self.drag_start_pos = None
        logger.warning("GraphWindow [VARS]: Variables initialisées")
        
        try:
            logger.warning("GraphWindow [UI]: Début setupUI")
            self.setupUI()
            logger.warning("GraphWindow [UI]: setupUI terminé")
        except Exception as e:
            logger.error(f"GraphWindow [UI ERROR]: {e}")
            raise
        
        try:
            logger.warning("GraphWindow [PARSE]: Début parseGraphData")
            self.parseGraphData()
            logger.warning("GraphWindow [PARSE]: parseGraphData terminé")
        except Exception as e:
            logger.error(f"GraphWindow [PARSE ERROR]: {e}")
            raise
        
        try:
            logger.warning("GraphWindow [ANIM]: Début setupAnimation")
            self.setupAnimation()
            logger.warning("GraphWindow [ANIM]: setupAnimation terminé")
        except Exception as e:
            logger.error(f"GraphWindow [ANIM ERROR]: {e}")
            raise
        
        logger.warning("GraphWindow [END]: Initialisation terminée avec succès")
        
    def setupUI(self):
        logger.warning("GraphWindow [UI]: setWindowTitle")
        self.setWindowTitle("Cartographie - Visualisation Dynamique")
        
        logger.warning("GraphWindow [UI]: setGeometry")
        self.setGeometry(100, 100, 1200, 800)
        
        # Style cohérent avec le reste de l'application
        logger.warning("GraphWindow [UI]: setStyleSheet")
        self.setStyleSheet("""
            QWidget {
                background-color: #2c2c2c;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                color: white;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#toggle3D {
                background-color: #2196F3;
            }
            QPushButton#toggle3D:hover {
                background-color: #1976D2;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
                padding: 5px;
            }
            QLabel#infoLabel {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        logger.warning("GraphWindow [UI]: Création layout principal")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # En-tête avec titre
        header_layout = QHBoxLayout()
        title_label = QLabel("Cartographie Réseau - Visualisation Interactive")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50; padding: 10px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Zone de contrôles
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        logger.warning("GraphWindow [UI]: Création boutons")
        controls_label = QLabel("Contrôles :")
        controls_label.setStyleSheet("font-weight: bold; margin-right: 10px;")
        
        self.zoom_in_btn = QPushButton("Zoom +")
        self.zoom_out_btn = QPushButton("Zoom -")
        self.reset_btn = QPushButton("Réinitialiser")
        self.toggle_3d_btn = QPushButton("Vue 3D")
        self.toggle_3d_btn.setObjectName("toggle3D")
        
        logger.warning("GraphWindow [UI]: Connexion boutons")
        self.zoom_in_btn.clicked.connect(self.zoomIn)
        self.zoom_out_btn.clicked.connect(self.zoomOut)
        self.reset_btn.clicked.connect(self.resetView)
        self.toggle_3d_btn.clicked.connect(self.toggle3DView)
        
        logger.warning("GraphWindow [UI]: Ajout widgets controls")
        controls_layout.addWidget(controls_label)
        controls_layout.addWidget(self.zoom_in_btn)
        controls_layout.addWidget(self.zoom_out_btn)
        controls_layout.addWidget(self.reset_btn)
        controls_layout.addWidget(self.toggle_3d_btn)
        controls_layout.addStretch()
        
        # Zone de dessin (canvas)
        logger.warning("GraphWindow [UI]: Création canvas")
        self.canvas = QWidget()
        self.canvas.setMinimumSize(800, 500)
        self.canvas.setStyleSheet("background-color: #1e1e1e; border: 2px solid #555555; border-radius: 8px;")
        self.canvas.paintEvent = self.paintEvent
        self.canvas.mousePressEvent = self.mousePressEvent
        self.canvas.mouseMoveEvent = self.mouseMoveEvent
        self.canvas.mouseReleaseEvent = self.mouseReleaseEvent
        
        # Zone d'informations
        logger.warning("GraphWindow [UI]: Création info_label")
        self.info_label = QLabel("Cliquez sur un nœud pour afficher ses détails")
        self.info_label.setObjectName("infoLabel")
        self.info_label.setWordWrap(True)
        self.info_label.setMinimumHeight(100)
        
        logger.warning("GraphWindow [UI]: Configuration layout final")
        main_layout.addLayout(header_layout)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.canvas, 1)  # Étendre le canvas
        main_layout.addWidget(self.info_label)
        
        logger.warning("GraphWindow [UI]: setLayout")
        self.setLayout(main_layout)
        logger.warning("GraphWindow [UI]: setupUI terminé avec succès")
        
    def parseGraphData(self):
        logger.warning("GraphWindow [PARSE]: Début parseGraphData")
        if not self.graph_data:
            logger.warning("GraphWindow [PARSE]: Aucune donnée graphique - création de données d'exemple")
            # Créer des données d'exemple si aucune donnée n'est fournie
            self.createSampleData()
            return
            
        logger.warning(f"GraphWindow [PARSE]: Vérification clés: {list(self.graph_data.keys())}")
        
        # Données JSON pour extraire nodes et edges
        if 'nodes' in self.graph_data:
            self.nodes = self.graph_data['nodes']
            logger.warning(f"GraphWindow [PARSE]: {len(self.nodes)} nœuds trouvés")
        else:
            logger.warning("GraphWindow [PARSE]: Pas de clé 'nodes'")
            
        if 'edges' in self.graph_data:
            self.edges = self.graph_data['edges']
            logger.warning(f"GraphWindow [PARSE]: {len(self.edges)} arêtes trouvées")
        else:
            logger.warning("GraphWindow [PARSE]: Pas de clé 'edges'")
            
        # Si pas de données valides, créer des exemples
        if not self.nodes:
            logger.warning("GraphWindow [PARSE]: Pas de nœuds - création de données d'exemple")
            self.createSampleData()
        else:
            # Utiliser les positions calculées par le backend
            logger.warning("GraphWindow [PARSE]: Début loadNodePositions")
            self.loadNodePositions()
        
        logger.warning("GraphWindow [PARSE]: parseGraphData terminé")
        
    def createSampleData(self):
        """Crée des données d'exemple pour les tests"""
        self.nodes = [
            {'id': 'domain1', 'label': 'example.com', 'type': 'domaine', 'level': 0},
            {'id': 'subdomain1', 'label': 'www.example.com', 'type': 'sous_domaine', 'level': 1, 'parent_id': 'domain1'},
            {'id': 'subdomain2', 'label': 'api.example.com', 'type': 'sous_domaine', 'level': 1, 'parent_id': 'domain1'},
            {'id': 'subdomain3', 'label': 'mail.example.com', 'type': 'sous_domaine', 'level': 1, 'parent_id': 'domain1'},
            {'id': 'port1', 'label': 'Port 80', 'type': 'port', 'level': 2, 'parent_id': 'subdomain1'},
            {'id': 'port2', 'label': 'Port 443', 'type': 'port', 'level': 2, 'parent_id': 'subdomain1'},
        ]
        
        self.edges = [
            {'source': 'domain1', 'target': 'subdomain1'},
            {'source': 'domain1', 'target': 'subdomain2'},
            {'source': 'domain1', 'target': 'subdomain3'},
            {'source': 'subdomain1', 'target': 'port1'},
            {'source': 'subdomain1', 'target': 'port2'},
        ]
        
        self.generateNodePositions()
    
    def toggle3DView(self):
        """Bascule entre vue 2D et 3D"""
        self.is_3d_mode = not self.is_3d_mode
        if self.is_3d_mode:
            self.toggle_3d_btn.setText("Vue 2D")
        else:
            self.toggle_3d_btn.setText("Vue 3D")
        self.update()
        
    def mousePressEvent(self, event):
        """Gestion des clics souris"""
        if event.button() == Qt.LeftButton:
            # Vérifier si on clique sur un nœud
            clicked_node = self.getNodeAtPosition(event.pos())
            if clicked_node:
                self.selected_node = clicked_node['id']
                self.showNodeInfo(clicked_node)
            else:
                self.selected_node = None
                self.info_label.setText("Cliquez sur un nœud pour afficher ses détails")
            
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.update()
            
    def mouseMoveEvent(self, event):
        """Gestion du drag"""
        if self.dragging and self.drag_start_pos:
            # TODO déplacement de la vue
            pass
        
    def mouseReleaseEvent(self, event):
        """Fin du drag"""
        self.dragging = False
        self.drag_start_pos = None
        
    def getNodeAtPosition(self, pos):
        """Trouve le nœud à la position donnée"""
        for node in self.nodes:
            node_id = node.get('id')
            if node_id not in self.node_positions:
                continue
                
            node_pos = self.node_positions[node_id]
            node_x, node_y = int(node_pos['x'] * self.zoom_factor), int(node_pos['y'] * self.zoom_factor)
            
            # Calculer la taille du nœud
            if node.get('type') == 'domaine':
                size = 30
            else:
                level = node.get('level', 1)
                size = max(15, 25 - level * 2)
            
            size *= self.zoom_factor
            
            # Vérifier si le clic est dans le cercle du nœud
            distance = math.sqrt((pos.x() - node_x)**2 + (pos.y() - node_y)**2)
            if distance <= size:
                return node
        
        return None
    
    def loadNodePositions(self):
        logger.warning("GraphWindow [LOAD]: Début loadNodePositions")
        center_x, center_y = self.width() // 2, self.height() // 2
        logger.warning(f"GraphWindow [LOAD]: Centre: {center_x}, {center_y}")
        
        for i, node in enumerate(self.nodes):
            node_id = node.get('id')
            x = center_x + node.get('x', 0)
            y = center_y + node.get('y', 0)
            
            self.node_positions[node_id] = {
                'x': x,
                'y': y,
                'target_x': x,
                'target_y': y,
                'velocity_x': 0,
                'velocity_y': 0,
                'level': node.get('level', 0)
            }
            logger.warning(f"GraphWindow [LOAD]: Nœud {i+1}/{len(self.nodes)} positionné: {node_id}")
            
        logger.warning("GraphWindow [LOAD]: loadNodePositions terminé")
        
    def zoomIn(self):
        logger.warning("GraphWindow [ZOOM IN]: Zoom avant")
        self.zoom_factor *= 1.2
        self.update()
        
    def zoomOut(self):
        logger.warning("GraphWindow [ZOOM OUT]: Zoom arrière")
        self.zoom_factor /= 1.2
        self.update()
        
    def resetView(self):
        self.zoom_factor = 1.0
        self.generateNodePositions()
        self.update()
        
    def toggleAnimation(self):
        if self.animation_timer.isActive():
            self.animation_timer.stop()
            self.animate_btn.setText("Animation")
        else:
            self.animation_timer.start(16)
            self.animate_btn.setText("Pause")
    
    def setupAnimation(self):
        logger.warning("GraphWindow [ANIM]: Connexion timer")
        self.animation_timer.timeout.connect(self.updateAnimation)
        logger.warning("GraphWindow [ANIM]: Démarrage timer")
        self.animation_timer.start(16)  # 60 FPS
        logger.warning("GraphWindow [ANIM]: setupAnimation terminé")
    
    def getNodeColor(self, node_type):
        colors = {
            'domaine': QColor(255, 100, 100),      # Rouge pour le domaine principal
            'sous_domaine': QColor(100, 255, 100), # Vert pour les sous-domaines
            'server': QColor(255, 100, 100),
            'service': QColor(100, 255, 100),
            'vulnerability': QColor(255, 100, 255),
            'port': QColor(100, 100, 255),
            'default': QColor(150, 150, 150)
        }
        return colors.get(node_type, colors['default'])
    
    def updateAnimation(self):
        for node_id, pos in self.node_positions.items():
            # force de répulsion entre nœuds
            for other_id, other_pos in self.node_positions.items():
                if node_id != other_id:
                    dx = pos['x'] - other_pos['x']
                    dy = pos['y'] - other_pos['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance > 0 and distance < 100:
                        force = 1000 / (distance * distance)
                        pos['velocity_x'] += force * dx / distance
                        pos['velocity_y'] += force * dy / distance
            
            # Attraction vers le centre
            center_x, center_y = self.width() // 2, self.height() // 2
            dx = center_x - pos['x']
            dy = center_y - pos['y']
            pos['velocity_x'] += dx * 0.001
            pos['velocity_y'] += dy * 0.001
            
            # Amortissement
            pos['velocity_x'] *= 0.95
            pos['velocity_y'] *= 0.95
            
            # Mise à jour position
            pos['x'] += pos['velocity_x']
            pos['y'] += pos['velocity_y']
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self.canvas if hasattr(self, 'canvas') else self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arrière-plan
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # Appliquer le zoom
        painter.scale(self.zoom_factor, self.zoom_factor)
        
        # Dessiner les arêtes en premier
        self.drawEdges(painter)
        
        # Dessiner les nœuds
        self.drawNodes(painter)
        
        # Afficher les informations de zoom
        painter.resetTransform()
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(10, 20, f"Zoom: {self.zoom_factor:.1f}x")
        if self.is_3d_mode:
            painter.drawText(10, 40, "Mode: 3D (Simulation)")
            
    def drawNodes(self, painter):
        for node in self.nodes:
            node_id = node.get('id')
            if node_id not in self.node_positions:
                continue
                
            pos = self.node_positions[node_id]
            x, y = int(pos['x']), int(pos['y'])
            
            # Effet 3D (simulation)
            if self.is_3d_mode:
                # Ajouter une ombre pour l'effet 3D
                shadow_offset = 5
                painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
                painter.setPen(Qt.NoPen)
                size = self.getNodeSize(node)
                painter.drawEllipse(x-size+shadow_offset, y-size+shadow_offset, size*2, size*2)
            
            # Couleur selon le type de nœud
            node_type = node.get('type', 'default')
            color = self.getNodeColor(node_type)
            
            # Taille selon le niveau
            size = self.getNodeSize(node)
            
            # Dessiner le nœud sélectionné avec un halo
            if node_id == self.selected_node:
                painter.setBrush(QBrush(QColor(255, 215, 0, 100)))
                painter.setPen(QPen(QColor(255, 215, 0), 4))
                painter.drawEllipse(x-size-8, y-size-8, (size+8)*2, (size+8)*2)
            
            # Dessiner le nœud principal
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawEllipse(x-size, y-size, size*2, size*2)
            
            # Dessiner le texte
            self.drawNodeLabel(painter, node, x, y, size)
            
    def getNodeSize(self, node):
        """Calcule la taille d'un nœud selon son type et niveau"""
        if node.get('type') == 'domaine':
            return 25
        else:
            level = node.get('level', 1)
            return max(12, 20 - level * 2)
    
    def drawNodeLabel(self, painter, node, x, y, size):
        """Dessine le label d'un nœud"""
        painter.setPen(QPen(QColor(255, 255, 255)))
        font_size = 9 if node.get('type') == 'domaine' else 8
        painter.setFont(QFont("Arial", font_size, QFont.Bold))
        
        text = node.get('label', str(node.get('id')))
        
        # Limiter la longueur du texte
        if len(text) > 15:
            text = text[:12] + "..."
        
        text_width = painter.fontMetrics().horizontalAdvance(text)
        painter.drawText(x - text_width//2, y + size + 20, text)
    
    
        
    def drawEdges(self, painter):
        pen = QPen(QColor(100, 100, 100), 2)
        painter.setPen(pen)
        
        for edge in self.edges:
            source_id = edge.get('source')
            target_id = edge.get('target')
            
            if source_id in self.node_positions and target_id in self.node_positions:
                source_pos = self.node_positions[source_id]
                target_pos = self.node_positions[target_id]
                
                painter.drawLine(
                    int(source_pos['x']), int(source_pos['y']),
                    int(target_pos['x']), int(target_pos['y'])
                )
    
    def drawNodes(self, painter):
        for node in self.nodes:
            node_id = node.get('id')
            if node_id not in self.node_positions:
                continue
                
            pos = self.node_positions[node_id]
            x, y = int(pos['x']), int(pos['y'])
            
            # Couleur selon le type de nœud
            node_type = node.get('type', 'default')
            color = self.getNodeColor(node_type)
            
            # Taille selon le niveau (domaine principal plus gros)
            if node_type == 'domaine':
                size = 30
            else:
                level = node.get('level', 1)
                size = max(15, 25 - level * 2)  # Plus petit pour les niveaux profonds
            
            # Dessiner le nœud sélectionné
            if node_id == self.selected_node:
                painter.setBrush(QBrush(QColor(255, 255, 0, 100)))
                painter.setPen(QPen(QColor(255, 255, 0), 3))
                painter.drawEllipse(x-size-5, y-size-5, (size+5)*2, (size+5)*2)
            
            # Dessiner le nœud
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawEllipse(x-size, y-size, size*2, size*2)
            
            # Dessiner le texte (URL du domaine/sous-domaine)
            painter.setPen(QPen(QColor(255, 255, 255)))
            font_size = 10 if node_type == 'domaine' else 8
            painter.setFont(QFont("Arial", font_size))
            text = node.get('label', str(node_id))
            
            # Limiter la longueur du texte affiché
            if len(text) > 20:
                text = text[:17] + "..."
            
            text_width = painter.fontMetrics().horizontalAdvance(text)
            painter.drawText(x - text_width//2, y + size + 15, text)
    
    def showNodeInfo(self, node):
        """Affiche les informations spécifiques aux domaines/sous-domaines"""
        node_type = node.get('type', 'Inconnu')
        info = f"Type: {node_type.capitalize()}\n"
        info += f"URL: {node.get('label', 'Inconnu')}\n"
        info += f"Niveau: {node.get('level', 'N/A')}\n"
        info += f"Description: {node.get('description', 'Aucune description')}\n"
        
        if node.get('parent_id'):
            parent_label = self.getParentLabel(node.get('parent_id'))
            info += f"Parent: {parent_label}"
        else:
            info += "Parent: Racine"
        
        self.info_label.setText(info)
    
    def getParentLabel(self, parent_id):
        """Récupère le label du nœud parent"""
        for node in self.nodes:
            if node.get('id') == parent_id:
                return node.get('label', 'Inconnu')
        return 'Inconnu'
    
    def generateNodePositions(self):
        """Génère des positions en cercles concentriques selon les niveaux"""
        center_x, center_y = self.width() // 2, self.height() // 2
        
        # Grouper les nœuds par niveau
        levels = {}
        for node in self.nodes:
            level = node.get('level', 0)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        for level, level_nodes in levels.items():
            if level == 0:
                for node in level_nodes:
                    node_id = node.get('id')
                    self.node_positions[node_id] = {
                        'x': center_x,
                        'y': center_y,
                        'target_x': center_x,
                        'target_y': center_y,
                        'velocity_x': 0,
                        'velocity_y': 0,
                        'level': level
                    }
            else:
                radius = level * 120
                angle_step = 2 * math.pi / len(level_nodes) if len(level_nodes) > 0 else 0
                
                for i, node in enumerate(level_nodes):
                    angle = i * angle_step
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                    node_id = node.get('id')
                    self.node_positions[node_id] = {
                        'x': x,
                        'y': y,
                        'target_x': x,
                        'target_y': y,
                        'velocity_x': 0,
                        'velocity_y': 0,
                        'level': level
                    }