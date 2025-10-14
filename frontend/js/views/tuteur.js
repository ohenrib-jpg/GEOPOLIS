class TuteurView {
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
