// Client API centralisé
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
