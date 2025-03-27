from flask import Blueprint, jsonify, request
from backend.app.database.database import SessionLocal
from backend.app.services.attaque_service import AttaqueService
from backend.app.scripts.attaque_script import AttaqueScript

attaque_bp = Blueprint('attaque', __name__)

@attaque_bp.route('/scan_domaines', methods=['POST'])
def scan_domaines():
    """
    Endpoint to scan all active domains
    """
    db_session = SessionLocal()
    attaque_service = AttaqueService(db_session)
    attaque_script = AttaqueScript()

    try:
        # Get domains to scan
        domaines = attaque_service.get_domaines_to_scan()
        
        # Results container
        scan_results = []

        # Scan each domain
        for domaine in domaines:
            url = domaine.url  # Assuming domaine model has a url attribute
            
            # Run attacks on the URL
            results = attaque_script.run_attack(url)
            
            # Save attacks and vulnerabilities
            attaque_service.add_attaques_for_domaine(url, results)
            
            # Collect results
            scan_results.append({
                'url': url,
                'results': results
            })

        return jsonify({
            'status': 'success',
            'scan_results': scan_results
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        db_session.close()

@attaque_bp.route('/get_domaine_attacks/<path:url>', methods=['GET'])
def get_domaine_attacks(url):
    """
    Retrieve attacks for a specific domain
    """
    db_session = SessionLocal()
    attaque_service = AttaqueService(db_session)

    try:
        # Get attacks
        attacks = attaque_service.get_attaques_by_domaine(url)
        
        # Get vulnerabilities
        vulnerabilities = attaque_service.get_vulnerabilites_by_domaine(url)

        return jsonify({
            'status': 'success',
            'attacks': [
                {
                    'id': attack.id_attaque,
                    'payload': attack.payload,
                    'date': attack.date_attaque,
                    'result': attack.resultat,
                    'type': attack.type.nom_type if attack.type else 'Unknown'
                } for attack in attacks
            ],
            'vulnerabilities': [
                {
                    'id': vuln.id_faille,
                    'severity': vuln.gravite,
                    'description': vuln.description,
                    'tag': vuln.balise
                } for vuln in vulnerabilities
            ]
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        db_session.close()