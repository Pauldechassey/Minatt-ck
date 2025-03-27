from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.app.models.attaque import Attaque
from backend.app.models.faille import Faille
from backend.app.models.type_attaque import Type
from backend.app.models.domaine import Domaine
from datetime import datetime

class AttaqueService:
    def __init__(self, db_session: Session):
        """
        Initialize the AttaqueService with a database session
        
        :param db_session: Database session
        """
        self.db = db_session

    def get_domaines_to_scan(self) -> List[Domaine]:
        try:
            return self.db.query(Domaine).filter(Domaine.actif == True).all()
        except Exception as e:
            print(f"Error retrieving domains: {e}")
            return []

    def add_attaques_for_domaine(self, domaine_url: str, scan_results: Dict[str, List]) -> None:
        try:
            # Get or create type attacks
            type_attacks = {
                'sqli': self._get_or_create_type_attaque('SQL Injection'),
                'xss': self._get_or_create_type_attaque('Cross-Site Scripting (XSS)'),
                'csrf': self._get_or_create_type_attaque('Cross-Site Request Forgery'),
                'headers_cookies': self._get_or_create_type_attaque('Headers and Cookies')
            }

            # Process each type of attack
            for attack_type, attacks in scan_results.items():
                if attack_type == 'url':
                    continue

                type_attack = type_attacks.get(attack_type)
                if not type_attack:
                    continue

                for attack_data in attacks:
                    # Create Attaque record
                    attaque = Attaque(
                        payload=str(attack_data.get('payload', '')),
                        date_attaque=datetime.now(),
                        resultat=attack_data.get('resultat', 0),
                        id_Type=type_attack.id_Type,
                        url=domaine_url
                    )
                    self.db.add(attaque)
                    self.db.flush()

                    # Create Faille record if vulnerability exists
                    if attack_data.get('faille'):
                        faille = Faille(
                            gravite=attack_data['faille'].get('gravite', 0),
                            description=attack_data['faille'].get('description', ''),
                            balise=attack_data['faille'].get('balise', ''),
                            id_attaque=attaque.id_attaque
                        )
                        self.db.add(faille)

            # Commit all changes
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error adding attacks for {domaine_url}: {e}")

    def _get_or_create_type_attaque(self, nom_type: str) -> Type:
        existing_type = self.db.query(Type).filter(Type.nom_type == nom_type).first()
        if existing_type:
            return existing_type

        new_type = Type(
            nom_type=nom_type,
            description_type=f"Vulnerability type for {nom_type}"
        )
        self.db.add(new_type)
        self.db.flush()
        return new_type

    def get_attaques_by_domaine(self, domaine_url: str) -> List[Attaque]:
        try:
            return self.db.query(Attaque).filter(Attaque.url == domaine_url).all()
        except Exception as e:
            print(f"Error retrieving attacks: {e}")
            return []

    def get_vulnerabilites_by_domaine(self, domaine_url: str) -> List[Faille]:
        try:
            return (
                self.db.query(Faille)
                .join(Attaque)
                .filter(Attaque.url == domaine_url)
                .all()
            )
        except Exception as e:
            print(f"Error retrieving vulnerabilities: {e}")
            return []