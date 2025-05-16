#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
from typing import Dict, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
from io import BytesIO
import os.path

REPORT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "res", "rapports"
)

# Création du répertoire s'il n'existe pas
os.makedirs(REPORT_DIR, exist_ok=True)


class HorizontalLine(Flowable):
    """Classe personnalisée pour dessiner une ligne horizontale."""

    def __init__(self, width, thickness=1, color=colors.black):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def generer_rapport(data: Dict) -> bytes:
    """Génère un rapport PDF à partir des données d'audit fournies.

    Args:
        data: Dictionnaire contenant les informations d'audit

    Returns:
        bytes: Contenu du rapport PDF
    """
    try:
        # Créer un buffer pour stocker le PDF
        buffer = BytesIO()

        # Information d'audit
        audit_id = data["audit_id"]
        audit_info = data["audit_info"]
        stats = data["statistics"]
        vulnerable_urls = data["vulnerable_urls"]
        all_urls = data["all_urls"]

        # Création du nom de fichier
        date_str = audit_info["date"].strftime("%d/%m/%Y")
        domaine_name = (
            audit_info["domaine_principal"].replace(".", "_").replace("://", "_")
        )
        filename = f"rapport_audit_{audit_id}_{domaine_name}_{date_str}.pdf"
        filepath = os.path.join(REPORT_DIR, filename)

        # Créer le document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=f"Rapport d'audit - {audit_info['domaine_principal']}",
        )

        # Styles
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="Center",
                parent=styles["Heading1"],
                alignment=TA_CENTER,
                spaceAfter=24,
            )
        )
        styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=styles["Heading2"],
                fontSize=14,
                spaceBefore=12,
                spaceAfter=6,
            )
        )
        styles.add(
            ParagraphStyle(
                name="SubsectionTitle",
                parent=styles["Heading3"],
                fontSize=12,
                spaceBefore=8,
                spaceAfter=4,
            )
        )

        # Construction du document
        elements = []

        # Page de titre
        elements.append(Paragraph(f"Rapport d'audit de sécurité", styles["Center"]))
        elements.append(Spacer(1, 1 * cm))
        elements.append(
            Paragraph(f"Domaine: {audit_info['domaine_principal']}", styles["Heading2"])
        )
        if audit_info["description"]:
            elements.append(Paragraph(f"{audit_info['description']}", styles["Normal"]))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(
            Paragraph(
                f"Date d'audit: {audit_info['date'].strftime('%d/%m/%Y')}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 2 * cm))
        elements.append(Paragraph("Confidentiel", styles["Center"]))
        elements.append(PageBreak())

        # Sommaire
        elements.append(Paragraph("Sommaire", styles["Heading1"]))
        elements.append(Paragraph("1. Résumé exécutif", styles["Normal"]))
        elements.append(Paragraph("2. Statistiques globales", styles["Normal"]))
        elements.append(Paragraph("3. Liste des URL testées", styles["Normal"]))
        elements.append(Paragraph("4. Vulnérabilités détectées", styles["Normal"]))
        elements.append(PageBreak())

        # Résumé exécutif
        elements.append(Paragraph("1. Résumé exécutif", styles["Heading1"]))
        elements.append(
            Paragraph(
                f"Ce rapport présente les résultats de l'audit de sécurité réalisé sur le domaine "
                f"{audit_info['domaine_principal']} et ses sous-domaines associés. "
                f"L'audit a été effectué le {audit_info['date'].strftime('%d/%m/%Y')}.",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 0.5 * cm))

        # Synthèse des résultats
        vulnerable_count = sum(1 for url in all_urls if url["is_vulnerable"])
        elements.append(Paragraph("Synthèse des résultats:", styles["SectionTitle"]))
        elements.append(
            Paragraph(
                f"• {stats['total_sous_domaines']} sous-domaines analysés<br/>"
                f"• {vulnerable_count} sous-domaines vulnérables ({round(vulnerable_count/stats['total_sous_domaines']*100) if stats['total_sous_domaines'] > 0 else 0}%)<br/>"
                f"• {stats['total_attaques']} attaques tentées<br/>"
                f"• {stats['total_failles']} failles de sécurité identifiées",
                styles["Normal"],
            )
        )

        elements.append(PageBreak())

        # Statistiques globales
        elements.append(Paragraph("2. Statistiques globales", styles["Heading1"]))

        stats_data = [
            ["Nombre de sous-domaines analysés", stats["total_sous_domaines"]],
            ["Nombre d'attaques tentées", stats["total_attaques"]],
            ["Nombre de failles identifiées", stats["total_failles"]],
        ]

        stats_table = Table(stats_data, colWidths=[doc.width * 2 / 3, doc.width / 3])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        elements.append(stats_table)
        elements.append(Spacer(1, 1 * cm))
        elements.append(PageBreak())

        # Liste des URL testées
        elements.append(Paragraph("3. Liste des URL testées", styles["Heading1"]))

        if all_urls:
            # Entêtes du tableau
            url_data = [["URL", "Description", "Attaques", "Failles", "Statut"]]

            # Données du tableau
            for url in all_urls:
                status = "Vulnérable" if url["is_vulnerable"] else "Sécurisé"
                status_color = colors.red if url["is_vulnerable"] else colors.green

                url_data.append(
                    [
                        url["url"],
                        url["description"] or "",
                        url["nb_attaques"],
                        url["nb_failles"],
                        status,
                    ]
                )

            # Création du tableau
            url_table = Table(
                url_data,
                colWidths=[
                    doc.width * 0.35,
                    doc.width * 0.3,
                    doc.width * 0.1,
                    doc.width * 0.1,
                    doc.width * 0.15,
                ],
            )

            # Style du tableau
            table_style = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),  # Aligner à gauche les URLs
                ("ALIGN", (1, 1), (1, -1), "LEFT"),  # Aligner à gauche les descriptions
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]

            # Colorer les statuts
            for i in range(1, len(url_data)):
                if url_data[i][4] == "Vulnérable":
                    table_style.append(("TEXTCOLOR", (4, i), (4, i), colors.red))
                    table_style.append(("FONTNAME", (4, i), (4, i), "Helvetica-Bold"))
                else:
                    table_style.append(("TEXTCOLOR", (4, i), (4, i), colors.green))

            url_table.setStyle(TableStyle(table_style))
            elements.append(url_table)
        else:
            elements.append(
                Paragraph(
                    "Aucune URL n'a été testée durant cet audit.", styles["Normal"]
                )
            )

        elements.append(PageBreak())

        # Vulnérabilités détectées
        elements.append(Paragraph("4. Vulnérabilités détectées", styles["Heading1"]))

        if vulnerable_urls:
            # Regrouper les vulnérabilités par URL
            vulns_by_url = {}
            for vuln in vulnerable_urls:
                url = vuln["url"]
                if url not in vulns_by_url:
                    vulns_by_url[url] = []
                vulns_by_url[url].append(vuln)

            # Afficher les vulnérabilités par URL
            for url, vulns in vulns_by_url.items():
                elements.append(Paragraph(f"URL: {url}", styles["SectionTitle"]))

                # Description de l'URL si disponible
                if vulns[0]["description"]:
                    elements.append(
                        Paragraph(
                            f"Description: {vulns[0]['description']}", styles["Normal"]
                        )
                    )

                elements.append(Spacer(1, 0.3 * cm))

                # Pour chaque vulnérabilité de cette URL
                for i, vuln in enumerate(vulns):
                    elements.append(
                        Paragraph(
                            f"Vulnérabilité #{i+1}: {vuln['type_attaque']}",
                            styles["SubsectionTitle"],
                        )
                    )

                    vuln_data = [
                        ["Balise affectée", vuln["balise"] or "N/A"],
                        ["Description", vuln["description_faille"]],
                        ["Gravité", vuln["gravite"]],
                        ["Payload utilisé", vuln["payload"]],
                        [
                            "Date de détection",
                            vuln["date_attaque"].strftime("%d/%m/%Y %H:%M:%S"),
                        ],
                    ]

                    vuln_table = Table(
                        vuln_data, colWidths=[doc.width * 0.25, doc.width * 0.75]
                    )

                    # Style du tableau de vulnérabilité
                    vuln_style = [
                        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                        ("ALIGN", (1, 0), (1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]

                    vuln_table.setStyle(TableStyle(vuln_style))
                    elements.append(vuln_table)
                    elements.append(Spacer(1, 0.5 * cm))

                elements.append(HorizontalLine(doc.width))
                elements.append(Spacer(1, 0.5 * cm))

        else:
            elements.append(
                Paragraph(
                    "Aucune vulnérabilité n'a été détectée durant cet audit.",
                    styles["Normal"],
                )
            )

        elements.append(PageBreak())

        # Construire le PDF
        doc.build(elements)

        # Récupérer le contenu du buffer
        pdf_content = buffer.getvalue()
        buffer.close()

        # Sauvegarder une copie du PDF dans le répertoire des rapports
        with open(filepath, "wb") as f:
            f.write(pdf_content)

        return pdf_content
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du rapport: {str(e)}")

def get_rapport_dir() -> str:
    """Retourne le chemin du répertoire des rapports."""
    return REPORT_DIR