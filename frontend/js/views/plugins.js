class PluginsView {
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
            alert(`✓ Plugin exécuté

${JSON.stringify(data.result, null, 2)}`);
        } catch (e) {
            alert(`❌ Erreur: ${e.message}`);
        }
    }
}
