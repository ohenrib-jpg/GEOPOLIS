"""
Plugin: Threat Intelligence
Description: Veille cyber et menaces hybrides via AlienVault OTX et CVE databases
"""

import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Plugin:
    """Classe principale du plugin"""
    
    def __init__(self, settings):
        """Initialisation"""
        self.name = "threat-intelligence"
        self.settings = settings
    
    def run(self, payload=None):
        """Point d'entrée principal"""
        if payload is None:
            payload = {}
        
        try:
            # VOTRE LOGIQUE ICI
            results = self._analyze_threats(payload)
            
            return {
                'status': 'success',
                'plugin': self.name,
                'timestamp': self._get_timestamp(),
                'data': results['data'],
                'metrics': results['metrics'],
                'message': 'Analyse des menaces cyber terminée'
            }
            
        except Exception as e:
            return {
                'status': 'error', 'plugin': self.name,
                'timestamp': self._get_timestamp(),
                'data': [],
                'metrics': {},
                'message': f'Erreur: {str(e)}'
            }
    
    def _analyze_threats(self, payload):
        """Logique d'analyse des menaces"""
        threat_type = payload.get('threat_type', 'all')
        
        # Données AlienVault OTX
        otx_data = self._fetch_otx_pulses(threat_type)
        
        # Données CVE récentes
        cve_data = self._fetch_recent_cves()
        
        # Analyse des campagnes de menace
        campaigns = self._analyze_campaigns(otx_data)
        
        data = []
        for threat in otx_data[:10]:
            data.append({
                'menace': threat['name'],
                'type': threat['type'],
                'severite': threat['severity'],
                'acteurs': ', '.join(threat['actors']),
                'cibles': threat['targets'],
                'iocs': len(threat['indicators']),
                'premiere_observation': threat['first_seen'],
                'derniere_activite': threat['last_seen']
            })
        
        # Ajouter les CVE critiques
        for cve in cve_data[:5]:
            data.append({
                'menace': cve['cve_id'],
                'type': 'Vulnerabilité',
                'severite': cve['cvss_score'],
                'acteurs': 'N/A',
                'cibles': cve['affected_products'],
                'iocs': 0,
                'premiere_observation': cve['published_date'],
                'derniere_activite': cve['last_modified']
            })
        
        metrics = {
            'menaces_actives': len(otx_data),
            'vulnerabilites_critiques': len([c for c in cve_data if c['cvss_score'] >= 9]),
            'campagnes_identifiees': len(campaigns),
            'pays_cibles': len(set([t['targets'] for t in otx_data])),
            'tendance_globale': self._calculate_threat_trend(otx_data)
        }
        
        return {'data': data, 'metrics': metrics}
    
    def _fetch_otx_pulses(self, threat_type):
        """Récupère les pulses AlienVault OTX"""
        try:
            # API AlienVault OTX (version démo)
            # url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
            # headers = {'X-OTX-API-KEY': self.settings.get('api_keys', {}).get('alienvault', '')}
            # response = requests.get(url, headers=headers)
            
            # Données de démonstration réalistes
            return [
                {
                    'name': 'APT29 Campaign',
                    'type': 'APT',
                    'severity': 'High',
                    'actors': ['APT29', 'Cozy Bear'],
                    'targets': 'Gouvernements UE',
                    'indicators': ['ip1', 'domain1', 'hash1'],
                    'first_seen': '2024-01-10',
                    'last_seen': '2024-01-15'
                },
                {
                    'name': 'Phishing Finance Sector',
                    'type': 'Phishing',
                    'severity': 'Medium',
                    'actors': ['FIN7'],
                    'targets': 'Banques internationales',
                    'indicators': ['ip2', 'domain2', 'hash2'],
                    'first_seen': '2024-01-12',
                    'last_seen': '2024-01-16'
                }
            ]
        except Exception as e:
            logger.warning(f"OTX API error: {e}")
            return []
    
    def _fetch_recent_cves(self):
        """Récupère les CVE récentes"""
        try:
            # NVD API pour CVE récentes
            # url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
            # params = {'resultsPerPage': 20, 'orderBy': 'PUBLISHED_DATE'}
            
            return [
                {
                    'cve_id': 'CVE-2024-1234',
                    'cvss_score': 9.8,
                    'affected_products': ['Windows', 'Linux'],
                    'published_date': '2024-01-15',
                    'last_modified': '2024-01-16'
                },
                {
                    'cve_id': 'CVE-2024-1235',
                    'cvss_score': 7.5,
                    'affected_products': ['Cisco IOS'],
                    'published_date': '2024-01-14',
                    'last_modified': '2024-01-15'
                }
            ]
        except Exception as e:
            logger.warning(f"CVE API error: {e}")
            return []
    
    def _analyze_campaigns(self, threats):
        """Analyse les campagnes de menace coordonnées"""
        campaigns = []
        
        # Regroupement par acteurs similaires
        actor_groups = {}
        for threat in threats:
            for actor in threat['actors']:
                if actor not in actor_groups:
                    actor_groups[actor] = []
                actor_groups[actor].append(threat)
        
        # Identification des campagnes
        for actor, threats_list in actor_groups.items():
            if len(threats_list) > 1:
                campaigns.append({
                    'nom_campagne': f"Campagne {actor}",
                    'acteur_principal': actor,
                    'menaces_liees': len(threats_list),
                    'periode_activite': f"{min(t['first_seen'] for t in threats_list)} to {max(t['last_seen'] for t in threats_list)}"
                })
        
        return campaigns
    
    def _calculate_threat_trend(self, threats):
        """Calcule la tendance des menaces"""
        if not threats:
            return 'Stable'
        
        high_severity = len([t for t in threats if t['severity'] == 'High'])
        if high_severity > len(threats) * 0.5:
            return 'Escalade'
        else:
            return 'Stable'
    
    def _get_timestamp(self):
        """Retourne timestamp ISO"""
        return datetime.now().isoformat()
    
    def get_info(self):
        """Informations du plugin"""
        return {
            'name': self.name,
            'capabilities': ['veille_cyber', 'analyse_ioc', 'detection_campagnes'],
            'required_keys': ['alienvault']  # Optionnel
        }