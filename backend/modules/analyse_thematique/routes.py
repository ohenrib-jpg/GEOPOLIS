"""
Module Analyse Thématique - Routes API
"""

from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('analyse', __name__)

# ============================================
# ANALYSE DE TEXTE
# ============================================

@bp.route('/text', methods=['POST'])
def analyze_text():
    """Analyse un texte brut"""
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        
        if not text or len(text) < 10:
            return jsonify({
                'success': False,
                'error': 'Texte trop court (minimum 10 caractères)'
            }), 400
        
        # Analyse basique (à remplacer par votre logique)
        from .service import analyze_text_content
        result = analyze_text_content(text)
        
        return jsonify({
            'success': True,
            'text': text[:200] + '...' if len(text) > 200 else text,
            'analysis': result
        })
    
    except Exception as e:
        logger.error(f"Erreur analyse texte: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# ANALYSE RSS
# ============================================

@bp.route('/rss', methods=['POST'])
def analyze_rss():
    """Parse et analyse un flux RSS"""
    try:
        data = request.get_json(force=True)
        url = data.get('url', '')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL manquante'
            }), 400
        
        # Parser RSS
        from .service import parse_rss_feed
        articles = parse_rss_feed(url)
        
        return jsonify({
            'success': True,
            'status': 'ok',
            'source': url,
            'articles': articles,
            'count': len(articles)
        })
    
    except Exception as e:
        logger.error(f"Erreur analyse RSS: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# CONFIGURATION
# ============================================

@bp.route('/keywords', methods=['GET'])
def get_keywords():
    """Retourne les mots-clés configurés"""
    keywords = {
        'geopolitique': ['conflit', 'diplomatie', 'sanction', 'alliance'],
        'economie': ['inflation', 'croissance', 'commerce', 'dette'],
        'social': ['manifestation', 'grève', 'réforme', 'social'],
        'environnement': ['climat', 'pollution', 'énergie', 'écologie'],
        'technologie': ['intelligence', 'numérique', 'cyber', 'innovation']
    }
    
    return jsonify({
        'success': True,
        'keywords': keywords
    })

@bp.route('/sources', methods=['GET'])
def get_sources():
    """Liste des sources RSS par défaut"""
    sources = [
        {
            'name': 'Le Monde - International',
            'url': 'https://www.lemonde.fr/international/rss_full.xml',
            'category': 'geopolitique'
        },
        {
            'name': 'Le Figaro - Économie',
            'url': 'https://www.lefigaro.fr/rss/figaro_economie.xml',
            'category': 'economie'
        },
        {
            'name': 'Les Échos',
            'url': 'https://www.lesechos.fr/rss.xml',
            'category': 'economie'
        }
    ]
    
    return jsonify({
        'success': True,
        'sources': sources
    })

@bp.route('/status', methods=['GET'])
def status():
    """État du module"""
    return jsonify({
        'success': True,
        'module': 'Analyse Thématique',
        'version': '3.0.0',
        'status': 'operational'
    })
