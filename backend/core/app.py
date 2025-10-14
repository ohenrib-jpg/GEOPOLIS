# === GEOPOLIS PLUGIN MONITOR AUTOSTART ===
try:
    from plugin_monitor import start_plugin_monitor_delayed
    import threading, os, json
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    cfg_path = os.path.join(repo_root, 'services.json')
    try:
        with open(cfg_path, 'r', encoding='utf-8') as _f:
            _cfg = json.load(_f)
    except Exception:
        _cfg = {}
    max_wait = 0
    for k,v in _cfg.items():
        if isinstance(v, dict) and not k.startswith('_'):
            try:
                max_wait = max(max_wait, int(v.get('start_timeout_seconds', 300)))
            except Exception:
                pass
    if max_wait <= 0:
        max_wait = 300
    t = threading.Thread(target=lambda: start_plugin_monitor_delayed(max_wait_seconds=max_wait, poll_interval=_cfg.get('_monitor', {}).get('check_interval_seconds', 5)), daemon=True)
    t.start()
except Exception as _e:
    print('Failed to start PluginMonitor (delayed):', _e)
# === END GEOPOLIS PLUGIN MONITOR AUTOSTART ===


"""
GEOPOLIS v1.20.13 - Architecture Unifiée et Robuste
Un seul serveur Flask avec frontend Single Page Application unifié
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import sys
import logging
from pathlib import Path

# Force UTF-8 sur Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/geopolis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Création structure
for folder in ['logs', 'db', 'data', 'config', 'frontend', 'backend/modules']:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Initialisation Flask
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Permet AJAX depuis le frontend

app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'geopolis-secret-key-change-me'),
    JSON_AS_ASCII=False,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024
)

# ============================================
# ROUTE PRINCIPALE : SERVE SPA
# ============================================

@app.route('/')
def serve_spa():
    """Sert la Single Page Application"""
    index_path = Path('frontend/index.html')
    if index_path.exists():
        return send_from_directory('frontend', 'index.html')
    
    # Fallback: créer index.html minimal
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GEOPOLIS v3.0</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: system-ui; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .setup { background: white; padding: 60px; border-radius: 20px; text-align: center; max-width: 600px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
            h1 { color: #667eea; margin-bottom: 20px; font-size: 3em; }
            .status { background: #d1ecf1; color: #0c5460; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .btn { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; margin: 10px; }
            .btn:hover { background: #5568d3; }
        </style>
    </head>
    <body>
        <div class="setup">
            <h1>🌍 GEOPOLIS v3.0</h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">Configuration Initiale</p>
            
            <div class="status">
                <strong>✓ Serveur Flask opérationnel</strong><br>
                <span style="font-size: 0.9em;">Le frontend doit être configuré</span>
            </div>
            
            <button class="btn" onclick="setupFrontend()">🚀 Configurer Frontend</button>
            <button class="btn" onclick="location.href='/api/health'">🔍 Vérifier API</button>
            
            <div id="result" style="margin-top: 30px;"></div>
        </div>
        
        <script>
            async function setupFrontend() {
                document.getElementById('result').innerHTML = '<p>⏳ Configuration en cours...</p>';
                try {
                    const res = await fetch('/api/setup/frontend', { method: 'POST' });
                    const data = await res.json();
                    if (data.success) {
                        document.getElementById('result').innerHTML = '<p style="color: green;">✓ Frontend configuré ! Rechargez la page.</p>';
                        setTimeout(() => location.reload(), 2000);
                    } else {
                        throw new Error(data.error);
                    }
                } catch (e) {
                    document.getElementById('result').innerHTML = '<p style="color: red;">❌ Erreur: ' + e.message + '</p>';
                }
            }
        </script>
    </body>
    </html>
    """

# ============================================
# API CORE
# ============================================

@app.route('/api/health')
def api_health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'version': '3.0.0',
        'timestamp': Path('logs/geopolis.log').stat().st_mtime if Path('logs/geopolis.log').exists() else 0
    })

@app.route('/api/info')
def api_info():
    """Informations système"""
    blueprints_loaded = [bp for bp in app.blueprints.keys() if bp != 'static']
    
    return jsonify({
        'name': 'GEOPOLIS',
        'version': '3.0.0',
        'architecture': 'Unified Flask + SPA',
        'modules_loaded': blueprints_loaded,
        'status': 'operational'
    })

@app.route('/api/setup/frontend', methods=['POST'])
def api_setup_frontend():
    """Génère le frontend unifié automatiquement"""
    try:
        from backend.core.frontend_generator import generate_frontend
        generate_frontend()
        return jsonify({'success': True, 'message': 'Frontend généré'})
    except Exception as e:
        logger.error(f"Erreur génération frontend: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# CHARGEMENT DES MODULES
# ============================================

def load_modules():
    """Charge tous les modules (Blueprints)"""
    modules_loaded = []
    
    # 1. Analyse Thématique
    try:
        from backend.modules.analyse_thematique.routes import bp as analyse_bp
        app.register_blueprint(analyse_bp, url_prefix='/api/analyse')
        modules_loaded.append('analyse_thematique')
        logger.info("[OK] Module Analyse Thematique charge")
    except ImportError as e:
        logger.warning(f"[SKIP] Analyse Thematique: {e}")
    except Exception as e:
        logger.error(f"[ERREUR] Analyse Thematique: {e}")
    
    # 2. Tuteur IA
    try:
        from backend.modules.tuteur_ia.routes import bp as tuteur_bp
        app.register_blueprint(tuteur_bp, url_prefix='/api/tuteur')
        modules_loaded.append('tuteur_ia')
        logger.info("[OK] Module Tuteur IA charge")
    except ImportError as e:
        logger.warning(f"[SKIP] Tuteur IA: {e}")
    except Exception as e:
        logger.error(f"[ERREUR] Tuteur IA: {e}")
    
    # 3. Plugins
    try:
        from backend.modules.plugins.routes import bp as plugins_bp
        app.register_blueprint(plugins_bp, url_prefix='/api/plugins')
        modules_loaded.append('plugins')
        logger.info("[OK] Module Plugins charge")
    except ImportError as e:
        logger.warning(f"[SKIP] Plugins: {e}")
    except Exception as e:
        logger.error(f"[ERREUR] Plugins: {e}")
    
    return modules_loaded

# ============================================
# GESTION ERREURS
# ============================================

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint non trouve', 'path': request.path}), 404
    # Rediriger vers SPA pour le routing côté client
    return serve_spa()

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Erreur 500: {e}", exc_info=True)
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Erreur serveur', 'details': str(e)}), 500
    return jsonify({'error': str(e)}), 500

# ============================================
# INITIALISATION
# ============================================

def initialize():
    """Initialise l'application"""
    logger.info("=" * 60)
    logger.info("GEOPOLIS v3.0 - Architecture Unifiee")
    logger.info("=" * 60)
    
    # Charger les modules
    modules = load_modules()
    logger.info(f"[+] Modules charges: {len(modules)}")
    
    # Vérifier le frontend
    if not Path('frontend/index.html').exists():
        logger.warning("[!] Frontend non configure - Utilisez /api/setup/frontend")
    else:
        logger.info("[OK] Frontend detecte")
    
    logger.info("=" * 60)
    logger.info("[OK] Initialisation terminee")
    logger.info("=" * 60)

# ============================================
# POINT D'ENTRÉE
# ============================================

if __name__ == '__main__':
    initialize()
    
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"[+] Serveur demarre sur http://{host}:{port}")
    logger.info("=" * 60)
    
    app.run(host=host, port=port, debug=debug, use_reloader=False)

# === Added by integration for GEOPOLIS unified service ===
from flask import jsonify

@app.route('/api/status')
def api_status():
    return jsonify({"status": "ok"}), 200
# === End integration ===

