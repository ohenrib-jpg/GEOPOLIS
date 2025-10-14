GEOPOLIS/
│
├── app.py                          # ★ Serveur Flask UNIQUE
├── start_geopolis_v3.bat          # Script démarrage Windows
├── requirements.txt                # Dépendances Python
│
├── frontend/                       # ★ Frontend SPA Unifié
│   ├── index.html                 # Page unique
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js                 # Client API centralisé
│       ├── app.js                 # Router SPA
│       └── views/
│           ├── dashboard.js       # Vue Dashboard
│           ├── analyse.js         # Vue Analyse
│           ├── tuteur.js          # Vue Tuteur IA
│           ├── plugins.js         # Vue Plugins
│           └── settings.js        # Vue Paramètres
│
├── backend/                        # ★ Backend Modulaire
│   ├── core/
│   │   └── frontend_generator.py # Générateur auto frontend
│   │
│   └── modules/
│       ├── analyse_thematique/
│       │   ├── routes.py          # API Blueprint
│       │   └── service.py         # Logique métier
│       │
│       ├── tuteur_ia/
│       │   ├── routes.py
│       │   └── service.py
│       │
│       └── plugins/
│           ├── routes.py
│           └── manager.py
│
├── plugins/                        # Plugins utilisateur
│   ├── gov_open_data/
│   └── finance/
    └── etc...
├── config/
│   └── geopolis.json              # Configuration centralisée
│
└── logs/
    └── geopolis.log               # Logs unifiés
```
