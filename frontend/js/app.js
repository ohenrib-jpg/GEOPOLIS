// Router et gestion des vues
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
