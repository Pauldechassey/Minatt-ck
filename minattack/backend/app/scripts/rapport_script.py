from datetime import datetime
from io import BytesIO
from typing import Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generer_rapport(data: Dict) -> Dict:
    """Génère un rapport PDF à partir des données d'audit"""
    
    # Création du buffer PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Création des styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    story = []
    
    # En-tête
    story.append(Paragraph("Rapport d'Audit de Sécurité", title_style))
    story.append(Paragraph(f"Date: {data['audit_info']['date']}", styles["Normal"]))
    story.append(Paragraph(f"Domaine: {data['audit_info']['domaine_principal']}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Statistiques globales
    story.append(Paragraph("Résumé des résultats", styles["Heading2"]))
    stats_data = [
        ["Sous-domaines analysés", str(data['statistics']['total_sous_domaines'])],
        ["Attaques effectuées", str(data['statistics']['total_attaques'])],
        ["Vulnérabilités trouvées", str(data['statistics']['total_failles'])]
    ]
    stats_table = Table(stats_data, colWidths=[4*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 20))

    # Vulnérabilités détectées
    if data['vulnerable_urls']:
        story.append(Paragraph("Vulnérabilités Détectées", styles["Heading2"]))
        for vuln in data['vulnerable_urls']:
            # En-tête de vulnérabilité
            story.append(Paragraph(f"URL: {vuln['url']}", styles["Heading3"]))
            
            vuln_data = [
                ["Type d'attaque", vuln['type_attaque']],
                ["Balise ciblée", vuln['balise']],
                ["Payload utilisé", vuln['payload']],
                ["Date de détection", vuln['date_attaque'].strftime('%Y-%m-%d %H:%M')],
                ["Gravité", vuln['gravite']],
                ["Description", vuln['description_faille']]
            ]
            
            vuln_table = Table(vuln_data, colWidths=[2*inch, 4*inch])
            vuln_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(vuln_table)
            story.append(Spacer(1, 15))

    # Liste des URLs testées
    story.append(Paragraph("URLs Analysées", styles["Heading2"]))
    story.append(Spacer(1, 10))
    
    for url in data['all_urls']:
        color = colors.red if url['is_vulnerable'] else colors.black
        url_style = ParagraphStyle(
            'URL',
            parent=styles['Normal'],
            textColor=color
        )
        story.append(Paragraph(
            f"• {url['url']} ({url['nb_attaques']} attaques, {url['nb_failles']} failles)", 
            url_style
        ))
        if url['description']:
            story.append(Paragraph(f"  Description: {url['description']}", styles['Normal']))
        story.append(Spacer(1, 5))

    # Génération du PDF
    doc.build(story)
    
    return {
        "filename": f"rapport_audit_{data['audit_info']['id']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        "content": buffer.getvalue()
    }