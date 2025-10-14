class AnalyseView {
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
