from PySide6.QtWidgets import (
    QWidget,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from minattack.frontend.ui.ui_rapports import Ui_Rapports
import tempfile
import os

from minattack.frontend.utils import settings
from minattack.frontend.repository.RapportRepo import RapportRepo


class RapportsWindow(QWidget, Ui_Rapports):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rapports()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.rapport_repo = RapportRepo()  
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

        self.ui.pushButtonDownloadRapports.clicked.connect(
            lambda: self.download_rapport()  
        )

    def showEvent(self, event):
        """Appelé quand la fenêtre devient visible"""
        super().showEvent(event)
        if settings.SELECTED_AUDIT_ID:
            print(f"[DEBUG] Loading report for audit {settings.SELECTED_AUDIT_ID}")
            self.display_rapport(settings.SELECTED_AUDIT_ID)
        else:
            print("[DEBUG] No audit selected")

    def display_rapport(self, audit_id: int):
        """Affiche le rapport PDF"""
        print(f"[DEBUG] Attempting to display report for audit {audit_id}")
        # Utiliser self.rapport_repo au lieu de self.main_window.rapportRepo
        pdf_content = self.rapport_repo.view_rapport(audit_id)
        if pdf_content:
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
                import shutil
                shutil.copy2(self.temp_pdf_path, file_path)
                QMessageBox.information(
                    self, "Succès", f"Rapport enregistré : {file_path}"
                )
            except Exception as e:
                print(f"[ERROR] Failed to save PDF: {e}")
                QMessageBox.warning(self, "Erreur", "Échec du téléchargement")
