from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QApplication,
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphWindow(QWidget):



    def __init__(self, graph_data, parent=None):
        super().__init__(parent)
        logger.warning("GraphWindow [START]: Initialisation")

        self.graph_data = graph_data
        self.parent_window = parent

        # Rendre la fenêtre modale
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Fenêtre sans bordure pour un effet plus moderne
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Variables pour le déplacement de la fenêtre
        self.window_dragging = False
        self.window_drag_start = None

        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.node_positions = {}
        self.zoom_factor = 1.0
        self.dragging = False
        self.drag_start_pos = None
        self.pan_offset_x = 0
        self.pan_offset_y = 0

        self.initial_animation_timer = QTimer()
        self.initial_animation_step = 0

        try:
            self._setup_ui()
            self._parse_graph_data()
        except Exception as e:
            logger.exception(
                "GraphWindow [ERROR]: Erreur durant l'initialisation"
            )
            raise

        logger.warning("GraphWindow [END]: Initialisation réussie")

    def _setup_ui(self):
        self.setWindowTitle("Cartographie - Visualisation Dynamique")

        # Obtenir la taille de l'écran
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Définir une taille raisonnable (80% de l'écran)
        window_width = int(screen_geometry.width() * 0.8)
        window_height = int(screen_geometry.height() * 0.8)

        # Centrer la fenêtre
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2

        # Appliquer la géométrie
        self.setGeometry(x, y, window_width, window_height)

        # Style avec effet d'overlay sombre
        self.setStyleSheet(self._stylesheet())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Barre de titre personnalisée (pour la fenêtre sans bordure)
        title_bar = QWidget()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet(
            """
            QWidget {
                background-color: rgba(26, 26, 26, 240);
                border-bottom: 2px solid #4CAF50;
            }
        """
        )

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)

        # Titre avec icône de déplacement
        title = QLabel("Cartographie - Visualisation")
        title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #4CAF50; padding: 10px;"
        )
        title.setCursor(Qt.OpenHandCursor)

        # Boutons de contrôle de fenêtre
        minimize_btn = QPushButton("−", objectName="windowButton")
        maximize_btn = QPushButton("□", objectName="windowButton")
        close_btn = QPushButton("✕", objectName="windowButton")

        minimize_btn.clicked.connect(self.showMinimized)
        maximize_btn.clicked.connect(self.toggleMaximize)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)

        # Contrôles du graphique
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(20, 10, 20, 10)

        controls_label = QLabel("Contrôles :")
        controls_label.setStyleSheet(
            "font-weight: bold; margin-right: 10px; color: #fff;"
        )

        zoom_in_btn = QPushButton("Zoom +")
        zoom_out_btn = QPushButton("Zoom -")
        reset_btn = QPushButton("Réinitialiser")

        zoom_in_btn.clicked.connect(self.zoomIn)
        zoom_out_btn.clicked.connect(self.zoomOut)
        reset_btn.clicked.connect(self.resetView)

        for btn in (controls_label, zoom_in_btn, zoom_out_btn, reset_btn):
            controls_layout.addWidget(btn)
        controls_layout.addStretch()

        # Canvas principal
        self.canvas = QWidget()
        self.canvas.setMinimumSize(800, 500)
        self.canvas.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 230); 
            border: 2px solid #333; 
            border-radius: 8px;
            margin: 10px;
        """
        )

        main_layout.addWidget(title_bar)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.canvas, 1)

        # Zone d'information en overlay (après avoir ajouté le canvas)
        self.info_label = QLabel(
            "Cliquez sur un nœud pour afficher ses détails", self
        )
        self.info_label.setObjectName("infoLabel")
        self.info_label.setWordWrap(True)
        self.info_label.setFixedHeight(170)  # Hauteur fixe
        self.info_label.setMinimumWidth(250)  # Largeur minimale
        self.info_label.setMaximumWidth(500)  # Largeur maximale
        self.info_label.raise_()  # Mettre au premier plan

        # Connecter les événements
        self.canvas.paintEvent = self.paintCanvas
        self.canvas.mousePressEvent = self.canvasMousePress
        self.canvas.mouseMoveEvent = self.canvasMouseMove
        self.canvas.mouseReleaseEvent = self.canvasMouseRelease
        self.canvas.wheelEvent = self.canvasMouseWheel

        # Événements pour déplacer la fenêtre
        title.mousePressEvent = self.titleMousePress
        title.mouseMoveEvent = self.titleMouseMove
        title.mouseReleaseEvent = self.titleMouseRelease

    def _stylesheet(self):
        return """
        QWidget { background-color: #000; color: #fff; font-family: 'Segoe UI', Arial; }
        QPushButton {
            background-color: #4CAF50; border: none; border-radius: 8px; padding: 10px 20px;
            color: white; font-weight: bold; font-size: 12px; min-width: 80px;
        }
        QPushButton:hover { background-color: #45a049; }
        QPushButton:pressed { background-color: #3d8b40; }
        QPushButton#closeButton { background-color: #f44336; min-width: 100px; }
        QPushButton#closeButton:hover { background-color: #da190b; }
        QPushButton#closeButton:pressed { background-color: #b71c1c; }
        QLabel { color: #fff; font-size: 13px; padding: 5px; }
        QLabel#infoLabel {
            background-color: #1a1a1a; border: 1px solid #555; border-radius: 8px;
            padding: 15px; margin: 10px;
        }
        """

    def toggleMaximize(self):
        """Basculer entre taille normale et maximisée (limitée à l'écran)"""
        if self.isMaximized():
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()

            window_width = int(screen_geometry.width() * 0.7)
            window_height = int(screen_geometry.height() * 0.7)

            x = (screen_geometry.width() - window_width) // 2
            y = (screen_geometry.height() - window_height) // 2

            self.setGeometry(x, y, window_width, window_height)
        else:
            # Maximiser à la taille de l'écran disponible
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            self.setGeometry(screen_geometry)

    def titleMousePress(self, event):
        """Début du déplacement de fenêtre"""
        if event.button() == Qt.LeftButton:
            self.window_dragging = True
            self.window_drag_start = event.globalPos()

    def titleMouseMove(self, event):
        """Déplacement de la fenêtre"""
        if self.window_dragging and self.window_drag_start:
            delta = event.globalPos() - self.window_drag_start
            self.move(self.pos() + delta)
            self.window_drag_start = event.globalPos()

    def titleMouseRelease(self, event):
        """Fin du déplacement de fenêtre"""
        self.window_dragging = False
        self.window_drag_start = None

    def resizeEvent(self, event):
        """Repositionner l'info label lors du redimensionnement"""
        super().resizeEvent(event)
        if hasattr(self, "info_label"):
            # Repositionner en bas à gauche avec une marge
            margin = 20
            self.info_label.move(
                margin, self.height() - self.info_label.height() - margin
            )

    def closeEvent(self, event):
        """Événement de fermeture personnalisé"""
        logger.warning(
            "GraphWindow [CLOSE]: Fermeture de la fenêtre graphique"
        )
        event.accept()

    def _parse_graph_data(self):
        if not self.graph_data:
            logger.warning("GraphWindow [PARSE]: Aucune donnée")
            return
        self.nodes = self.graph_data.get("nodes", [])
        self.edges = self.graph_data.get("edges", [])
        self.loadNodePositions()
        logger.warning(
            f"GraphWindow [PARSE]: {len(self.nodes)} nœuds, {len(self.edges)} arêtes chargés"
        )

    def drawNodeLabel(self, painter, node, x, y, size):
        """Dessine le label d'un nœud avec seulement la partie ajoutée de l'URL"""
        painter.setPen(QPen(QColor(255, 255, 255)))
        level = node.get("level", 0)

        # Taille de police selon le niveau
        font_size = 10 if level == 0 else 9
        painter.setFont(
            QFont(
                "Arial", font_size, QFont.Bold if level == 0 else QFont.Normal
            )
        )

        # Extraire seulement la partie ajoutée de l'URL
        full_url = node.get("label", str(node.get("id")))
        text = self.extractPathSegment(full_url, level)

        # Limiter la longueur du texte pour l'affichage
        if len(text) > 20:
            text = text[:17] + "..."

        # Calculer la position du texte (en dessous du nœud)
        text_width = painter.fontMetrics().horizontalAdvance(text)
        text_x = x - text_width // 2
        text_y = y + size + 15

        # Dessiner un fond semi-transparent pour le texte
        text_rect = painter.fontMetrics().boundingRect(text)
        bg_rect = text_rect.adjusted(-3, -2, 3, 2)

        # Correction : utiliser QPoint pour moveTopLeft
        from PySide6.QtCore import QPoint

        bg_rect.moveTopLeft(
            QPoint(text_x - 3, text_y - text_rect.height() + 2)
        )

        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.drawRoundedRect(bg_rect, 3, 3)

        # Dessiner le texte
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(text_x, text_y, text)

    def paintCanvas(self, event):
        """Événement de peinture pour le canvas"""
        painter = QPainter(self.canvas)

        try:
            painter.setRenderHint(QPainter.Antialiasing)

            # Arrière-plan noir
            painter.fillRect(self.canvas.rect(), QColor(0, 0, 0))

            # Vérifier qu'on a des données à dessiner
            if not self.nodes:
                painter.setPen(QPen(QColor(255, 255, 255)))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(
                    self.canvas.rect().center(), "Aucune donnée à afficher"
                )
                return

            # Sauvegarder l'état du painter
            painter.save()

            # Appliquer les transformations (pan et zoom depuis le centre)
            center_x = self.canvas.width() / 2
            center_y = self.canvas.height() / 2

            painter.translate(
                center_x + self.pan_offset_x, center_y + self.pan_offset_y
            )
            painter.scale(self.zoom_factor, self.zoom_factor)

            # Dessiner les arêtes en premier
            if self.edges:
                self.drawEdges(painter)

            # Dessiner les nœuds
            if self.nodes:
                self.drawNodes(painter)

            # Restaurer l'état du painter
            painter.restore()

            # Afficher les informations de zoom (sans transformation)
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(10, 20, f"Zoom: {self.zoom_factor:.1f}x")
            painter.drawText(10, 40, f"Nœuds: {len(self.nodes)}")
            painter.drawText(10, 60, f"Arêtes: {len(self.edges)}")

        except Exception as e:
            logger.error(f"GraphWindow [PAINT ERROR]: {e}")
        finally:
            # S'assurer que le painter est correctement fermé
            if painter.isActive():
                painter.end()

    def drawNodes(self, painter):
        """Dessine tous les nœuds"""
        for node in self.nodes:
            node_id = node.get("id")
            if node_id not in self.node_positions:
                continue

            pos = self.node_positions[node_id]
            x, y = int(pos["x"]), int(pos["y"])

            # Couleur selon le type de nœud
            node_type = node.get("type", "default")
            color = self.getNodeColor(node_type)

            # Taille selon le niveau
            size = self.getNodeSize(node)

            # Dessiner le nœud sélectionné avec un halo
            if node_id == self.selected_node:
                painter.setBrush(QBrush(QColor(255, 215, 0, 100)))
                painter.setPen(QPen(QColor(255, 215, 0), 4))
                painter.drawEllipse(
                    x - size - 5, y - size - 5, (size + 5) * 2, (size + 5) * 2
                )

            # Dessiner le nœud principal
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawEllipse(x - size, y - size, size * 2, size * 2)

            # Dessiner le texte
            self.drawNodeLabel(painter, node, x, y, size)

    def drawEdges(self, painter):
        """Dessine toutes les arêtes"""
        pen = QPen(QColor(100, 100, 100), 2)
        painter.setPen(pen)

        for edge in self.edges:
            source_id = edge.get("source")
            target_id = edge.get("target")

            if (
                source_id in self.node_positions
                and target_id in self.node_positions
            ):
                source_pos = self.node_positions[source_id]
                target_pos = self.node_positions[target_id]

                painter.drawLine(
                    int(source_pos["x"]),
                    int(source_pos["y"]),
                    int(target_pos["x"]),
                    int(target_pos["y"]),
                )

    def getNodeColor(self, node_type):
        colors = {
            "domaine": QColor(
                255, 100, 100
            ),  # Rouge pour le domaine principal
            "sous_domaine": QColor(
                100, 255, 100
            ),  # Vert pour les sous-domaines
            "server": QColor(255, 100, 100),
            "service": QColor(100, 255, 100),
            "vulnerability": QColor(255, 100, 255),
            "port": QColor(100, 100, 255),
            "default": QColor(150, 150, 150),
        }
        return colors.get(node_type, colors["default"])

    def getNodeSize(self, node):
        """Calcule la taille d'un nœud selon son type et niveau"""
        if node.get("type") == "domaine":
            return 25
        else:
            level = node.get("level", 1)
            return max(12, 20 - level * 2)

    def extractPathSegment(self, full_url, level):
        """Extrait seulement la partie de l'URL ajoutée à ce niveau"""
        try:
            if level == 0:
                # Pour le domaine principal, extraire seulement le hostname
                if "://" in full_url:
                    # Protocole présent
                    url_parts = full_url.split("://", 1)[1]
                else:
                    url_parts = full_url

                # Extraire seulement le hostname (avant le premier /)
                hostname = url_parts.split("/")[0]
                return hostname
            else:
                # Pour les autres niveaux, extraire le chemin
                if "://" in full_url:
                    path_part = full_url.split("://", 1)[1]
                    if "/" in path_part:
                        path = "/" + "/".join(path_part.split("/")[1:])
                    else:
                        path = "/"
                else:
                    if full_url.startswith("/"):
                        path = full_url
                    else:
                        path = "/" + full_url

                # Diviser le chemin en segments
                path_segments = [seg for seg in path.split("/") if seg]

                if level <= len(path_segments):
                    # Retourner seulement le segment de ce niveau
                    return "/" + path_segments[level - 1]
                else:
                    return path  # Fallback si le niveau est incorrect
        except Exception as e:
            logger.error(
                f"GraphWindow [ERROR]: Erreur lors de l'extraction du segment de chemin: {e}"
            )
            return full_url

    def drawNodeLabel(self, painter, node, x, y, size):
        """Dessine le label d'un nœud avec seulement la partie ajoutée de l'URL"""
        painter.setPen(QPen(QColor(255, 255, 255)))
        level = node.get("level", 0)

        # Taille de police selon le niveau
        font_size = 10 if level == 0 else 9
        painter.setFont(
            QFont(
                "Arial", font_size, QFont.Bold if level == 0 else QFont.Normal
            )
        )

        # Extraire seulement la partie ajoutée de l'URL
        full_url = node.get("label", str(node.get("id")))
        text = self.extractPathSegment(full_url, level)

        # Limiter la longueur du texte pour l'affichage
        if len(text) > 20:
            text = text[:17] + "..."

        # Calculer la position du texte (en dessous du nœud)
        text_width = painter.fontMetrics().horizontalAdvance(text)
        text_x = x - text_width // 2
        text_y = y + size + 15

        # Dessiner un fond semi-transparent pour le texte
        text_rect = painter.fontMetrics().boundingRect(text)
        bg_rect = text_rect.adjusted(-3, -2, 3, 2)

        # Correction : utiliser QPoint pour moveTopLeft
        from PySide6.QtCore import QPoint

        bg_rect.moveTopLeft(
            QPoint(text_x - 3, text_y - text_rect.height() + 2)
        )

        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.drawRoundedRect(bg_rect, 3, 3)

        # Dessiner le texte
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(text_x, text_y, text)

    def canvasMousePress(self, event):
        """Gestion des clics souris sur le canvas"""
        if event.button() == Qt.LeftButton:
            # Vérifier si on clique sur un nœud d'abord
            clicked_node = self.getNodeAtPosition(event.pos())
            if clicked_node:
                self.selected_node = clicked_node["id"]
                self.showNodeInfo(clicked_node)
                logger.warning(
                    f"GraphWindow [CLICK]: Nœud sélectionné: {clicked_node['id']}"
                )
                self.dragging = False
                self.drag_start_pos = None
            else:
                self.selected_node = None
                self.info_label.setText(
                    "Cliquez sur un nœud pour afficher ses détails"
                )
                self.dragging = True
                self.drag_start_pos = event.pos()
                logger.warning("GraphWindow [DRAG]: Début du drag")

            self.canvas.update()

    def canvasMouseMove(self, event):
        """Gestion du drag pour déplacer la vue"""
        if self.dragging and self.drag_start_pos:
            # Calculer le déplacement
            dx = event.pos().x() - self.drag_start_pos.x()
            dy = event.pos().y() - self.drag_start_pos.y()

            # Appliquer le déplacement
            self.pan_offset_x += dx
            self.pan_offset_y += dy

            # Mettre à jour la position de départ
            self.drag_start_pos = event.pos()

            # Redessiner uniquement le canvas
            self.canvas.update()

    def canvasMouseRelease(self, event):
        """Fin du drag"""
        if self.dragging:
            logger.warning("GraphWindow [DRAG]: Fin du drag")
        self.dragging = False
        self.drag_start_pos = None

    def canvasMouseWheel(self, event):
        """Gestion de la molette pour le zoom centré"""
        # Calculer le facteur de zoom
        zoom_in = event.angleDelta().y() > 0
        zoom_factor_change = 1.1 if zoom_in else 1 / 1.1

        # Position de la souris dans le canvas
        mouse_pos = event.position()

        # Position relative au centre du canvas
        center_x = self.canvas.width() / 2
        center_y = self.canvas.height() / 2

        # Calculer la position avant zoom
        before_x = (
            mouse_pos.x() - center_x - self.pan_offset_x
        ) / self.zoom_factor
        before_y = (
            mouse_pos.y() - center_y - self.pan_offset_y
        ) / self.zoom_factor

        # Appliquer le zoom
        self.zoom_factor *= zoom_factor_change
        self.zoom_factor = max(0.1, min(5.0, self.zoom_factor))

        # Calculer la position après zoom
        after_x = before_x * self.zoom_factor
        after_y = before_y * self.zoom_factor

        # Ajuster le pan pour garder le point sous la souris
        self.pan_offset_x += (mouse_pos.x() - center_x) - after_x
        self.pan_offset_y += (mouse_pos.y() - center_y) - after_y

        self.canvas.update()

    def getNodeAtPosition(self, canvas_pos):
        """Trouve le nœud à la position donnée dans le canvas"""
        for node in self.nodes:
            node_id = node.get("id")
            if node_id not in self.node_positions:
                continue

            node_pos = self.node_positions[node_id]
            # Appliquer les transformations (zoom et pan)
            center_x = self.canvas.width() / 2
            center_y = self.canvas.height() / 2

            node_x = (
                center_x
                + (node_pos["x"] * self.zoom_factor)
                + self.pan_offset_x
            )
            node_y = (
                center_y
                + (node_pos["y"] * self.zoom_factor)
                + self.pan_offset_y
            )

            size = self.getNodeSize(node) * self.zoom_factor

            # Vérifier si le clic est dans le cercle du nœud
            distance = math.sqrt(
                (canvas_pos.x() - node_x) ** 2 + (canvas_pos.y() - node_y) ** 2
            )
            if distance <= size:
                return node

        return None

    def loadNodePositions(self):
        """Charge les positions des nœuds et centre le graphique"""
        if not self.nodes:
            return

        # Vérifier si les nœuds ont des positions définies
        has_positions = False
        for node in self.nodes:
            x = node.get("x", 0)
            y = node.get("y", 0)
            if x != 0 or y != 0:
                has_positions = True
                break

        if has_positions:
            # Charger les positions depuis les données
            for node in self.nodes:
                node_id = node.get("id")
                x = node.get("x", 0)
                y = node.get("y", 0)

                self.node_positions[node_id] = {
                    "x": x,
                    "y": y,
                    "level": node.get("level", 0),
                }
        else:
            # Générer des positions si elles n'existent pas
            logger.warning(
                "GraphWindow [POSITIONS]: Génération des positions automatique"
            )
            self.generateNodePositions()

        # Centrer le graphique automatiquement
        self.centerGraph()

    def centerGraph(self):
        """Centre le graphique dans la vue"""
        if not self.node_positions:
            return

        # Calculer les bornes du graphique
        x_coords = [pos["x"] for pos in self.node_positions.values()]
        y_coords = [pos["y"] for pos in self.node_positions.values()]

        if x_coords and y_coords:
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)

            # Centre du graphique
            graph_center_x = (min_x + max_x) / 2
            graph_center_y = (min_y + max_y) / 2

            # Déplacer tous les nœuds pour centrer le graphique sur (0,0)
            for node_id in self.node_positions:
                self.node_positions[node_id]["x"] -= graph_center_x
                self.node_positions[node_id]["y"] -= graph_center_y

            # Calculer un zoom approprié
            graph_width = max_x - min_x
            graph_height = max_y - min_y

            if graph_width > 0 and graph_height > 0:
                # Ajuster le zoom pour que le graphique tienne dans 80% de la vue
                canvas_width = 800  # Taille minimale du canvas
                canvas_height = 500

                zoom_x = (
                    (canvas_width * 0.4) / graph_width
                    if graph_width > 0
                    else 1.0
                )
                zoom_y = (
                    (canvas_height * 0.4) / graph_height
                    if graph_height > 0
                    else 1.0
                )

                self.zoom_factor = min(
                    zoom_x, zoom_y, 2.0
                )  # Limiter le zoom max à 2.0
                self.zoom_factor = max(
                    0.3, self.zoom_factor
                )  # Limiter le zoom min à 0.3

    def zoomIn(self):
        logger.warning("GraphWindow [ZOOM IN]: Zoom avant")
        self.zoom_factor *= 1.2
        self.zoom_factor = min(5.0, self.zoom_factor)
        self.canvas.update()

    def zoomOut(self):
        logger.warning("GraphWindow [ZOOM OUT]: Zoom arrière")
        self.zoom_factor /= 1.2
        self.zoom_factor = max(0.1, self.zoom_factor)
        self.canvas.update()

    def resetView(self):
        """Remet la vue à zéro"""
        self.zoom_factor = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.canvas.update()

    def showNodeInfo(self, node):
        """Affiche les informations du nœud avec URL complète"""
        node_type = node.get("type", "Inconnu")
        level = node.get("level", 0)
        full_url = node.get("label", "Inconnu")
        displayed_part = self.extractPathSegment(full_url, level)

        info = f"Type: {node_type.capitalize()}\n"
        info += f"Niveau: {level}\n"
        info += f"Partie affichée: {displayed_part}\n"
        info += f"URL complète: {full_url}\n"

        if node.get("parent_id"):
            parent_label = self.getParentLabel(node.get("parent_id"))
            info += f"Parent: {parent_label}"
        else:
            info += "Parent: Racine"

        self.info_label.setText(info)

        # Calculer la largeur nécessaire pour le texte
        font_metrics = self.info_label.fontMetrics()
        text_width = 0
        for line in info.split("\n"):
            line_width = font_metrics.horizontalAdvance(line)
            text_width = max(text_width, line_width)

        # Ajouter une marge et respecter les limites
        desired_width = text_width + 30  # 30px de marge
        desired_width = max(250, min(500, desired_width))  # Entre 250 et 500px

        self.info_label.setFixedWidth(desired_width)

    def getParentLabel(self, parent_id):
        """Récupère le label du nœud parent"""
        for node in self.nodes:
            if node.get("id") == parent_id:
                return node.get("label", "Inconnu")
        return "Inconnu"

    def generateNodePositions(self):
        """Génère des positions en cercles concentriques selon les niveaux"""
        # Grouper les nœuds par niveau
        levels = {}
        for node in self.nodes:
            level = node.get("level", 0)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)

        for level, level_nodes in levels.items():
            if level == 0:
                # Domaine principal au centre
                for node in level_nodes:
                    node_id = node.get("id")
                    self.node_positions[node_id] = {
                        "x": 0,  # Centre (0,0)
                        "y": 0,
                        "level": level,
                    }
            else:
                # Autres niveaux en cercles
                radius = level * 120
                angle_step = (
                    2 * math.pi / len(level_nodes)
                    if len(level_nodes) > 0
                    else 0
                )

                for i, node in enumerate(level_nodes):
                    angle = i * angle_step
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)

                    node_id = node.get("id")
                    self.node_positions[node_id] = {
                        "x": x,
                        "y": y,
                        "level": level,
                    }
