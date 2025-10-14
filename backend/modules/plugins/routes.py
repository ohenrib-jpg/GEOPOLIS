"""
Module Plugins - Routes API
"""

from flask import Blueprint, request, jsonify
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

bp = Blueprint('plugins', __name__)

@bp.route('/list', methods=['GET'])
def list_plugins():
    """Liste tous les plugins disponibles"""
    try:
        from .manager import PluginManager
        
        manager = PluginManager()
        plugins = manager.list_plugins()
        
        return jsonify({
            'success': True,
            'plugins': plugins,
            'count': len(plugins)
        })
    
    except Exception as e:
        logger.error(f"Erreur listage plugins: {e}")
        return jsonify({
            'success': True,
            'plugins': [],
            'count': 0,
            'message': 'Aucun plugin disponible'
        })

@bp.route('/<plugin_id>/run', methods=['POST'])
def run_plugin(plugin_id):
    """Exécute un plugin"""
    try:
        from .manager import PluginManager
        
        data = request.get_json(force=True) if request.data else {}
        payload = data.get('payload', {})
        
        manager = PluginManager()
        result = manager.execute_plugin(plugin_id, payload)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erreur exécution plugin {plugin_id}: {e}")
        return jsonify({
            'success': False,
            'plugin': plugin_id,
            'error': str(e)
        }), 500

@bp.route('/status', methods=['GET'])
def status():
    """État du module"""
    return jsonify({
        'success': True,
        'module': 'Plugins',
        'version': '3.0.0',
        'status': 'operational'
    })
