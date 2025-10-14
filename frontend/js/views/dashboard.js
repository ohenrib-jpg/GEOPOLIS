class DashboardView {
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
