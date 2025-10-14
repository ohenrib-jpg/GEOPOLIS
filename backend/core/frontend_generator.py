"""
Générateur automatique du frontend unifié SPA
"""

from pathlib import Path

def generate_frontend():
    """Génère tous les fichiers du frontend"""
    
    frontend_dir = Path('frontend')
    frontend_dir.mkdir(exist_ok=True)
    
    # 1. Index HTML (SPA)
    index_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GEOPOLIS v3.0 - Dashboard Géopolitique</title>
    <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
    <div id="app">
        <!-- Sidebar -->
        <aside id="sidebar">
            <div class="logo">
                <h1>🌍 GEOPOLIS</h1>
                <span class="version">v3.0</span>
            </div>
            
            <nav id="nav">
                <a href="#dashboard" class="nav-item active" data-view="dashboard">
                    <span class="icon">📊</span>
                    <span>Dashboard</span>
                </a>
                <a href="#analyse" class="nav-item" data-view="analyse">
                    <span class="icon">🔍</span>
                    <span>Analyse Thématique</span>
                </a>
                <a href="#tuteur" class="nav-item" data-view="tuteur">
                    <span class="icon">🧠</span>
                    <span>Tuteur IA</span>
                </a>
                <a href="#plugins" class="nav-item" data-view="plugins">
                    <span class="icon">🔌</span>
                    <span>Plugins</span>
                </a>
                <a href="#settings" class="nav-item" data-view="settings">
                    <span class="icon">⚙️</span>
                    <span>Paramètres</span>
                </a>
            </nav>
            
            <div class="sidebar-footer">
                <div id="status" class="status"></div>
            </div>
        </aside>
        
        <!-- Main Content -->
        <main id="content">
            <div id="view-container"></div>
        </main>
    </div>
    
    <script src="/js/api.js"></script>
    <script src="/js/views/dashboard.js"></script>
    <script src="/js/views/analyse.js"></script>
    <script src="/js/views/tuteur.js"></script>
    <script src="/js/views/plugins.js"></script>
    <script src="/js/views/settings.js"></script>
    <script src="/js/app.js"></script>
</body>
</html>'''
    
    # 2. CSS Principal
    styles_css = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: #f5f7fa;
    overflow: hidden;
}

#app {
    display: flex;
    height: 100vh;
}

/* Sidebar */
#sidebar {
    width: 260px;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.logo {
    padding: 30px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.2);
}

.logo h1 {
    font-size: 1.8em;
    margin-bottom: 5px;
}

.version {
    font-size: 0.85em;
    opacity: 0.8;
}

#nav {
    flex: 1;
    padding: 20px 0;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 15px 20px;
    color: white;
    text-decoration: none;
    transition: all 0.3s;
    border-left: 4px solid transparent;
}

.nav-item:hover {
    background: rgba(255,255,255,0.1);
    border-left-color: rgba(255,255,255,0.5);
}

.nav-item.active {
    background: rgba(255,255,255,0.2);
    border-left-color: white;
    font-weight: 600;
}

.nav-item .icon {
    margin-right: 15px;
    font-size: 1.3em;
}

.sidebar-footer {
    padding: 20px;
    border-top: 1px solid rgba(255,255,255,0.2);
}

.status {
    font-size: 0.85em;
    opacity: 0.9;
}

/* Main Content */
#content {
    flex: 1;
    overflow-y: auto;
    background: #f5f7fa;
}

#view-container {
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
}

/* Cards */
.card {
    background: white;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.card h2 {
    color: #333;
    margin-bottom: 20px;
    font-size: 1.6em;
}

/* Buttons */
.btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.3s;
}

.btn:hover {
    background: #5568d3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Inputs */
input, textarea, select {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-family: inherit;
    font-size: 1em;
    margin: 10px 0;
    transition: border 0.3s;
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: #667eea;
}

/* Alerts */
.alert {
    padding: 15px 20px;
    border-radius: 8px;
    margin: 15px 0;
    border-left: 4px solid;
}

.alert-info {
    background: #d1ecf1;
    color: #0c5460;
    border-left-color: #17a2b8;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border-left-color: #28a745;
}

.alert-warning {
    background: #fff3cd;
    color: #856404;
    border-left-color: #ffc107;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
    border-left-color: #dc3545;
}

/* Loading */
.loading {
    text-align: center;
    padding: 40px;
    color: #666;
}

.spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Result Box */
.result-box {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 20px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
    margin-top: 15px;
}
'''
    
    # 3. API Client
    api_js = '''// Client API centralisé
class API {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }
    
    // GET
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    // POST
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    // Endpoints spécifiques
    health() {
        return this.get('/health');
    }
    
    info() {
        return this.get('/info');
    }
    
    // Analyse
    analyseText(text) {
        return this.post('/analyse/text', { text });
    }
    
    analyseRSS(url) {
        return this.post('/analyse/rss', { url });
    }
    
    // Tuteur
    analyzeCode(code, provider = 'local') {
        return this.post('/tuteur/analyze', { code, provider });
    }
    
    // Plugins
    listPlugins() {
        return this.get('/plugins/list');
    }
    
    runPlugin(id, payload = {}) {
        return this.post(`/plugins/${id}/run`, { payload });
    }
}

const api = new API();
'''
    
    # 4. Router App Principal
    app_js = '''// Router et gestion des vues
class App {
    constructor() {
        this.currentView = null;
        this.views = {
            dashboard: new DashboardView(),
            analyse: new AnalyseView(),
            tuteur: new TuteurView(),
            plugins: new PluginsView(),
            settings: new SettingsView()
        };
        
        this.init();
    }
    
    init() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const view = item.dataset.view;
                this.navigateTo(view);
            });
        });
        
        // Hash routing
        window.addEventListener('hashchange', () => {
            const hash = window.location.hash.substring(1) || 'dashboard';
            this.navigateTo(hash);
        });
        
        // Status check
        this.checkStatus();
        setInterval(() => this.checkStatus(), 30000);
        
        // Load initial view
        const initialView = window.location.hash.substring(1) || 'dashboard';
        this.navigateTo(initialView);
    }
    
    navigateTo(viewName) {
        const view = this.views[viewName];
        if (!view) {
            console.error(`View not found: ${viewName}`);
            return;
        }
        
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === viewName);
        });
        
        // Render view
        const container = document.getElementById('view-container');
        container.innerHTML = view.render();
        
        // Mount view logic
        if (view.mount) {
            view.mount();
        }
        
        this.currentView = viewName;
        window.location.hash = viewName;
    }
    
    async checkStatus() {
        try {
            const data = await api.health();
            document.getElementById('status').innerHTML = 
                `<div style="color: rgba(255,255,255,0.9);">✓ Connecté v${data.version}</div>`;
        } catch (error) {
            document.getElementById('status').innerHTML = 
                `<div style="color: #ff6b6b;">✗ Déconnecté</div>`;
        }
    }
}

// Start app
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
'''
    
    # Écrire les fichiers
    (frontend_dir / 'index.html').write_text(index_html, encoding='utf-8')
    
    css_dir = frontend_dir / 'css'
    css_dir.mkdir(exist_ok=True)
    (css_dir / 'styles.css').write_text(styles_css, encoding='utf-8')
    
    js_dir = frontend_dir / 'js'
    js_dir.mkdir(exist_ok=True)
    (js_dir / 'api.js').write_text(api_js, encoding='utf-8')
    (js_dir / 'app.js').write_text(app_js, encoding='utf-8')
    
    # Créer les vues
    views_dir = js_dir / 'views'
    views_dir.mkdir(exist_ok=True)
    
    generate_views(views_dir)
    
    print("[OK] Frontend généré avec succès")

def generate_views(views_dir):
    """Génère tous les fichiers de vues"""
    
    # Dashboard
    dashboard_js = '''class DashboardView {
    render() {
        return `
            <div class="card">
                <h2>📊 Dashboard</h2>
                <p>Bienvenue sur GEOPOLIS v3.0</p>
                
                <div class="alert alert-info">
                    <strong>✓ Système opérationnel</strong><br>
                    Architecture unifiée avec frontend SPA
                </div>
            </div>
            
            <div class="card">
                <h2>Modules Disponibles</h2>
                <div id="modules-list">Chargement...</div>
            </div>
        `;
    }
    
    async mount() {
        try {
            const data = await api.info();
            const html = `
                <ul style="line-height: 2;">
                    ${data.modules_loaded.map(m => `<li>✓ ${m}</li>`).join('')}
                </ul>
            `;
            document.getElementById('modules-list').innerHTML = html;
        } catch (e) {
            document.getElementById('modules-list').innerHTML = 
                `<div class="alert alert-error">Erreur: ${e.message}</div>`;
        }
    }
}
'''
    
    # Analyse
    analyse_js = '''class AnalyseView {
    render() {
        return `
            <div class="card">
                <h2>🔍 Analyse de Texte</h2>
                <textarea id="analyseText" rows="6" placeholder="Collez un texte à analyser..."></textarea>
                <button class="btn" onclick="this.analyzeText()">Analyser</button>
                <div id="analyseResult"></div>
            </div>
            
            <div class="card">
                <h2>📡 Analyse RSS</h2>
                <input type="text" id="rssUrl" placeholder="URL du flux RSS" value="https://www.lemonde.fr/rss">
                <button class="btn" onclick="this.analyzeRSS()">Analyser</button>
                <div id="rssResult"></div>
            </div>
        `;
    }
    
    mount() {
        window.analyzeText = () => this.handleAnalyzeText();
        window.analyzeRSS = () => this.handleAnalyzeRSS();
    }
    
    async handleAnalyzeText() {
        const text = document.getElementById('analyseText').value.trim();
        const resultDiv = document.getElementById('analyseResult');
        
        if (!text) {
            resultDiv.innerHTML = '<div class="alert alert-warning">Veuillez entrer du texte</div>';
            return;
        }
        
        resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Analyse en cours...</div>';
        
        try {
            const data = await api.analyseText(text);
            resultDiv.innerHTML = `
                <div class="alert alert-success">✓ Analyse terminée</div>
                <div class="result-box">${JSON.stringify(data, null, 2)}</div>
            `;
        } catch (e) {
            resultDiv.innerHTML = `<div class="alert alert-error">❌ Erreur: ${e.message}</div>`;
        }
    }
    
    async handleAnalyzeRSS() {
        const url = document.getElementById('rssUrl').value.trim();
        const resultDiv = document.getElementById('rssResult');
        
        if (!url) {
            resultDiv.innerHTML = '<div class="alert alert-warning">Veuillez entrer une URL</div>';
            return;
        }
        
        resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Récupération du flux...</div>';
        
        try {
            const data = await api.analyseRSS(url);
            const articles = data.articles || [];
            let html = `<div class="alert alert-success">✓ ${articles.length} articles trouvés</div>`;
            
            if (articles.length > 0) {
                html += '<ul style="line-height: 2;">';
                articles.forEach(article => {
                    html += `<li><strong>${article.title || 'Sans titre'}</strong></li>`;
                });
                html += '</ul>';
            }
            
            resultDiv.innerHTML = html;
        } catch (e) {
            resultDiv.innerHTML = `<div class="alert alert-error">❌ Erreur: ${e.message}</div>`;
        }
    }
}
'''
    
    # Tuteur IA
    tuteur_js = '''class TuteurView {
    render() {
        return `
            <div class="card">
                <h2>🧠 Tuteur IA - Analyse de Code</h2>
                
                <label>Code Python à analyser :</label>
                <textarea id="codeInput" rows="12" placeholder="Collez votre code Python ici..."></textarea>
                
                <label>Provider IA :</label>
                <select id="aiProvider">
                    <option value="local">Local (Heuristique)</option>
                    <option value="openai">OpenAI (nécessite clé API)</option>
                    <option value="anthropic">Anthropic (nécessite clé API)</option>
                </select>
                
                <button class="btn" onclick="this.analyzeCode()">🔍 Analyser le code</button>
                
                <div id="codeResult"></div>
            </div>
        `;
    }
    
    mount() {
        window.analyzeCode = () => this.handleAnalyzeCode();
    }
    
    async handleAnalyzeCode() {
        const code = document.getElementById('codeInput').value.trim();
        const provider = document.getElementById('aiProvider').value;
        const resultDiv = document.getElementById('codeResult');
        
        if (!code) {
            resultDiv.innerHTML = '<div class="alert alert-warning">Veuillez entrer du code</div>';
            return;
        }
        
        resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Analyse en cours...</div>';
        
        try {
            const data = await api.analyzeCode(code, provider);
            
            let html = `<div class="alert alert-success">✓ Analyse terminée (Backend: ${data.backend})</div>`;
            
            if (data.analysis) {
                html += `<div class="result-box">${data.analysis}</div>`;
            }
            
            if (data.fixed_code) {
                html += `
                    <h3 style="margin-top: 20px;">Code corrigé :</h3>
                    <div class="result-box">${data.fixed_code}</div>
                `;
            }
            
            resultDiv.innerHTML = html;
        } catch (e) {
            resultDiv.innerHTML = `<div class="alert alert-error">❌ Erreur: ${e.message}</div>`;
        }
    }
}
'''
    
    # Plugins
    plugins_js = '''class PluginsView {
    render() {
        return `
            <div class="card">
                <h2>🔌 Gestionnaire de Plugins</h2>
                <button class="btn" onclick="this.loadPlugins()">🔄 Actualiser</button>
                <div id="pluginsList"></div>
            </div>
        `;
    }
    
    mount() {
        window.loadPlugins = () => this.handleLoadPlugins();
        this.handleLoadPlugins();
    }
    
    async handleLoadPlugins() {
        const listDiv = document.getElementById('pluginsList');
        listDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Chargement...</div>';
        
        try {
            const data = await api.listPlugins();
            const plugins = data.plugins || [];
            
            if (plugins.length === 0) {
                listDiv.innerHTML = `
                    <div class="alert alert-info">
                        Aucun plugin disponible<br>
                        <small>Placez vos plugins dans le dossier plugins/</small>
                    </div>
                `;
                return;
            }
            
            let html = '<div style="margin-top: 20px;">';
            plugins.forEach(plugin => {
                html += `
                    <div class="card" style="margin: 15px 0; background: #f8f9fa;">
                        <h3>${plugin.name || plugin.id}</h3>
                        <p>${plugin.metadata?.description || 'Aucune description'}</p>
                        <button class="btn" onclick="window.runPlugin('${plugin.id}')">▶ Exécuter</button>
                    </div>
                `;
            });
            html += '</div>';
            
            listDiv.innerHTML = html;
            
            window.runPlugin = (id) => this.handleRunPlugin(id);
        } catch (e) {
            listDiv.innerHTML = `<div class="alert alert-error">❌ Erreur: ${e.message}</div>`;
        }
    }
    
    async handleRunPlugin(pluginId) {
        if (!confirm(`Exécuter le plugin ${pluginId} ?`)) return;
        
        try {
            const data = await api.runPlugin(pluginId);
            alert(`✓ Plugin exécuté\n\n${JSON.stringify(data.result, null, 2)}`);
        } catch (e) {
            alert(`❌ Erreur: ${e.message}`);
        }
    }
}
'''
    
    # Settings
    settings_js = '''class SettingsView {
    render() {
        return `
            <div class="card">
                <h2>⚙️ Paramètres</h2>
                
                <h3>Clés API</h3>
                
                <label>OpenAI API Key :</label>
                <input type="password" id="openaiKey" placeholder="sk-...">
                
                <label>Anthropic API Key :</label>
                <input type="password" id="anthropicKey" placeholder="sk-ant-...">
                
                <label>HuggingFace API Key :</label>
                <input type="password" id="hfKey" placeholder="hf_...">
                
                <h3 style="margin-top: 30px;">Paramètres IA</h3>
                
                <label>Provider par défaut :</label>
                <select id="defaultProvider">
                    <option value="local">Local (gratuit)</option>
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic</option>
                    <option value="huggingface">HuggingFace</option>
                </select>
                
                <label>Modèle OpenAI :</label>
                <select id="openaiModel">
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    <option value="gpt-4">GPT-4</option>
                </select>
                
                <button class="btn" onclick="this.saveSettings()" style="margin-top: 20px;">💾 Sauvegarder</button>
                
                <div id="settingsResult"></div>
            </div>
        `;
    }
    
    mount() {
        window.saveSettings = () => this.handleSaveSettings();
        this.loadSettings();
    }
    
    async loadSettings() {
        try {
            const data = await api.get('/config');
            if (data.config) {
                // Remplir les champs (sans afficher les clés)
                document.getElementById('defaultProvider').value = data.config.ai_settings?.provider || 'local';
                document.getElementById('openaiModel').value = data.config.ai_settings?.model || 'gpt-3.5-turbo';
            }
        } catch (e) {
            console.error('Erreur chargement config:', e);
        }
    }
    
    async handleSaveSettings() {
        const resultDiv = document.getElementById('settingsResult');
        resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Sauvegarde...</div>';
        
        const config = {
            api_keys: {
                openai: document.getElementById('openaiKey').value,
                anthropic: document.getElementById('anthropicKey').value,
                huggingface: document.getElementById('hfKey').value
            },
            ai_settings: {
                provider: document.getElementById('defaultProvider').value,
                model: document.getElementById('openaiModel').value
            }
        };
        
        try {
            await api.post('/config', config);
            resultDiv.innerHTML = '<div class="alert alert-success">✓ Configuration sauvegardée</div>';
            
            // Effacer les champs de clés
            document.getElementById('openaiKey').value = '';
            document.getElementById('anthropicKey').value = '';
            document.getElementById('hfKey').value = '';
        } catch (e) {
            resultDiv.innerHTML = `<div class="alert alert-error">❌ Erreur: ${e.message}</div>`;
        }
    }
}
'''
    
    # Écrire tous les fichiers de vues
    (views_dir / 'dashboard.js').write_text(dashboard_js, encoding='utf-8')
    (views_dir / 'analyse.js').write_text(analyse_js, encoding='utf-8')
    (views_dir / 'tuteur.js').write_text(tuteur_js, encoding='utf-8')
    (views_dir / 'plugins.js').write_text(plugins_js, encoding='utf-8')
    (views_dir / 'settings.js').write_text(settings_js, encoding='utf-8')

if __name__ == '__main__':
    generate_frontend()
    print("Frontend généré avec succès !")
