"""
Module Tuteur IA - Routes API Simplifiées
"""

from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('tuteur', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_code():
    """Analyse du code Python"""
    try:
        data = request.get_json(force=True)
        code = data.get('code', '')
        provider = data.get('provider', 'local')
        
        if not code or len(code) < 10:
            return jsonify({
                'success': False,
                'error': 'Code trop court'
            }), 400
        
        # Analyse locale par défaut
        from .service import analyze_python_code
        result = analyze_python_code(code, provider)
        
        return jsonify({
            'success': True,
            'backend': result.get('backend', 'local'),
            'analysis': result.get('analysis', ''),
            'issues': result.get('issues', []),
            'suggestions': result.get('suggestions', []),
            'fixed_code': result.get('fixed_code')
        })
    
    except Exception as e:
        logger.error(f"Erreur analyse code: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/providers', methods=['GET'])
def list_providers():
    """Liste des providers IA disponibles"""
    return jsonify({
        'success': True,
        'providers': {
            'local': {'name': 'Analyse Locale', 'available': True},
            'openai': {'name': 'OpenAI', 'available': False},
            'anthropic': {'name': 'Anthropic', 'available': False}
        }
    })

@bp.route('/status', methods=['GET'])
def status():
    """État du module"""
    return jsonify({
        'success': True,
        'module': 'Tuteur IA',
        'version': '3.0.0',
        'status': 'operational'
    })
