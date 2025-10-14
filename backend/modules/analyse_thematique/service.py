"""
Module Analyse Thématique - Logique métier
"""

import re
import logging

logger = logging.getLogger(__name__)

# ============================================
# ANALYSE DE TEXTE
# ============================================

def analyze_text_content(text):
    """
    Analyse le contenu d'un texte
    Retourne thème, sentiment, mots-clés, etc.
    """
    
    # Mots-clés par thème
    themes = {
        'geopolitique': ['guerre', 'conflit', 'diplomatie', 'sanction', 'alliance', 'tension'],
        'economie': ['inflation', 'croissance', 'commerce', 'dette', 'marché', 'économie'],
        'social': ['manifestation', 'grève', 'réforme', 'social', 'protestation'],
        'environnement': ['climat', 'pollution', 'énergie', 'écologie', 'carbone'],
        'technologie': ['intelligence', 'numérique', 'cyber', 'innovation', 'tech']
    }
    
    # Détection du thème principal
    text_lower = text.lower()
    theme_scores = {}
    
    for theme, keywords in themes.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            theme_scores[theme] = score
    
    main_theme = max(theme_scores, key=theme_scores.get) if theme_scores else 'general'
    
    # Analyse de sentiment
    positive_words = ['succès', 'accord', 'paix', 'coopération', 'progrès', 'victoire']
    negative_words = ['crise', 'conflit', 'guerre', 'tension', 'échec', 'problème']
    
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if pos_count > neg_count:
        sentiment = {'label': 'positif', 'score': min(50 + pos_count * 10, 90)}
    elif neg_count > pos_count:
        sentiment = {'label': 'négatif', 'score': max(50 - neg_count * 10, 10)}
    else:
        sentiment = {'label': 'neutre', 'score': 50}
    
    # Niveau de risque
    risk_keywords = ['crise', 'conflit', 'guerre', 'sanction', 'tension']
    risk_count = sum(1 for kw in risk_keywords if kw in text_lower)
    
    if risk_count >= 3:
        risk_level = 'high'
    elif risk_count >= 1:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    # Extraction mots-clés
    keywords_found = []
    for theme_keywords in themes.values():
        keywords_found.extend([kw for kw in theme_keywords if kw in text_lower])
    
    return {
        'theme': main_theme,
        'sentiment': sentiment,
        'risk_level': risk_level,
        'keywords': list(set(keywords_found))[:10],  # Top 10 uniques
        'word_count': len(text.split()),
        'character_count': len(text)
    }

# ============================================
# PARSING RSS
# ============================================

def parse_rss_feed(url):
    """
    Parse un flux RSS et retourne les articles
    """
    try:
        import feedparser
        
        logger.info(f"Parsing RSS: {url}")
        feed = feedparser.parse(url)
        
        articles = []
        for entry in feed.entries[:20]:  # Limiter à 20 articles
            article = {
                'title': entry.get('title', 'Sans titre'),
                'link': entry.get('link', ''),
                'description': entry.get('summary', entry.get('description', '')),
                'published': entry.get('published', ''),
                'source': feed.feed.get('title', 'Source inconnue')
            }
            articles.append(article)
        
        logger.info(f"✓ {len(articles)} articles récupérés")
        return articles
    
    except ImportError:
        logger.error("feedparser non installé")
        return parse_rss_fallback(url)
    
    except Exception as e:
        logger.error(f"Erreur parsing RSS: {e}")
        return []

def parse_rss_fallback(url):
    """
    Fallback si feedparser n'est pas disponible
    Utilise requests + regex basique
    """
    try:
        import requests
        
        logger.warning("Utilisation du fallback RSS (feedparser non disponible)")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        xml_content = response.text
        
        # Extraction basique par regex
        titles = re.findall(r'<title>(.*?)</title>', xml_content, re.DOTALL)
        links = re.findall(r'<link>(.*?)</link>', xml_content, re.DOTALL)
        
        articles = []
        for i in range(min(len(titles), len(links), 20)):
            if i > 0:  # Skip le premier (titre du feed)
                articles.append({
                    'title': titles[i].strip(),
                    'link': links[i].strip(),
                    'description': '',
                    'published': '',
                    'source': titles[0].strip() if titles else 'Source inconnue'
                })
        
        logger.info(f"✓ {len(articles)} articles récupérés (fallback)")
        return articles
    
    except Exception as e:
        logger.error(f"Erreur fallback RSS: {e}")
        return []

# ============================================
# ANALYSE AVANCÉE (avec IA si disponible)
# ============================================

def analyze_with_ai(text, ai_manager=None):
    """
    Analyse avec IA si disponible, sinon fallback heuristique
    """
    if ai_manager:
        try:
            result = ai_manager.analyze_text(text)
            return result
        except Exception as e:
            logger.warning(f"IA non disponible: {e}, utilisation heuristique")
    
    return analyze_text_content(text)
