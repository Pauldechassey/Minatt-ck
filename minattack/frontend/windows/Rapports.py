from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QPixmap
from minattack.frontend.ui.ui_rapports import Ui_Rapports
import tempfile
import os

from minattack.frontend.utils import settings


class RapportsWindow(QWidget, Ui_Rapports):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rapports()
        self.ui.setupUi(self)
        self.main_window = main_window  # Stockez la référence à MainWindow
        self.temp_pdf_path = None

        # Initializing decorative elements
        self.ui.pushButtonDeconnexionRapports.setIcon(
            QIcon(":/images/deconnexion.png")
        )
        pixmap = QPixmap(":/images/logo.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Connecting menu buttons
        self.ui.pushButtonDeconnexionRapports.clicked.connect(
            self.main_window.logout
        )
        self.ui.pushButtonAccueilRapports.clicked.connect(
            self.main_window.goToAccueil
        )
        self.ui.pushButtonActualiteRapports.clicked.connect(
            self.main_window.goToActualite
        )
        self.ui.pushButtonDocumentationRapports.clicked.connect(
            self.main_window.goToDocumentation
        )

        # Connecter le bouton de téléchargement
        self.ui.pushButtonDownloadRapports.clicked.connect(
            self.display_rapport(settings.SELECTED_AUDIT_ID)
        )

    def display_rapport(self, audit_id: int):
        """Affiche le rapport PDF"""
        print(f"[DEBUG] Attempting to display report for audit {audit_id}")
        pdf_content = self.main_window.rapport_repo.view_rapport(audit_id)
        if pdf_content:
            # Créer un fichier temporaire pour le PDF
            if self.temp_pdf_path:
                try:
                    os.remove(self.temp_pdf_path)
                except Exception:
                    pass

            with tempfile.NamedTemporaryFile(
                suffix=".pdf", delete=False
            ) as tmp:
                tmp.write(pdf_content)
                self.temp_pdf_path = tmp.name
                print(
                    f"[DEBUG] PDF saved to temporary file: {self.temp_pdf_path}"
                )

            # Utiliser directement le QWebEngineView de l'interface
            url = QUrl.fromLocalFile(self.temp_pdf_path)
            self.ui.qWebEngineViewPdfRapports.setUrl(url)
            self.ui.pushButtonDownloadRapports.setEnabled(True)
        else:
            print("[ERROR] Failed to get PDF content")
            QMessageBox.warning(
                self, "Erreur", "Impossible de charger le rapport"
            )

    def download_rapport(self):
        """Télécharge le rapport PDF"""
        # Vérifier si un rapport est actuellement affiché
        current_url = self.ui.qWebEngineViewPdfRapports.url()
        if not current_url.isValid() or not current_url.isLocalFile():
            QMessageBox.warning(self, "Erreur", "Aucun rapport à télécharger")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le rapport",
            f"rapport_audit_{settings.SELECTED_AUDIT_ID}.pdf",
            "PDF (*.pdf)",
        )

        if file_path:
            try:
                # Copier le fichier temporaire vers la destination
                import shutil

                shutil.copy2(self.temp_pdf_path, file_path)
                QMessageBox.information(
                    self, "Succès", f"Rapport enregistré : {file_path}"
                )
            except Exception as e:
                print(f"[ERROR] Failed to save PDF: {e}")
                QMessageBox.warning(self, "Erreur", "Échec du téléchargement")
