class SettingsView {
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
