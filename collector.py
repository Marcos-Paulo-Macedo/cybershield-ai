"""
Módulo de Coleta e Ingestão de Dados de Threat Intelligence / OSINT.
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class ThreatCollector:
    """Coletor de inteligência de ameaças, notícias de cibersegurança e dados de fraudes."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberShieldAI/1.0'
        }
        self.default_rss_sources = [
            "https://www.cisa.gov/cybersecurity-advisories/all.xml",
            "https://feeds.feedburner.com/TheHackersNews"
        ]

    def fetch_rss_feeds(self, urls: List[str] = None) -> List[Dict[str, str]]:
        """Busca notícias e alertas de segurança recentes de fontes RSS."""
        sources = urls or self.default_rss_sources
        articles = []
        
        for url in sources:
            try:
                response = requests.get(url, headers=self.headers, timeout=8)
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    # Parsing básico de RSS
                    channel = root.find('channel')
                    if channel is not None:
                        for item in channel.findall('item')[:5]:
                            title = item.find('title').text if item.find('title') is not None else 'Sem título'
                            link = item.find('link').text if item.find('link') is not None else ''
                            desc = item.find('description').text if item.find('description') is not None else ''
                            articles.append({
                                'source': url,
                                'title': title,
                                'link': link,
                                'summary': BeautifulSoup(desc, 'html.parser').get_text()[:300] if desc else ''
                            })
            except Exception as e:
                # Fallback gracioso em caso de erro de rede/parsing
                continue
                
        return articles

    def scrape_fraud_database(self, query: str) -> Dict[str, Any]:
        """Simula/busca dados contextuais e relatos sobre um golpe/ameaça específica."""
        # Base de conhecimento estática / fallback contextual para alimentar o LLM
        known_tactics = {
            "phishing": "Disparo em massa de mensagens contendo links falsos para captura de credenciais ou dados bancários.",
            "vishing": "Engenharia social por telefone utilizando engenharia da fala, falsificação de caller ID e inteligência artificial.",
            "deepfake": "Sintetização avançada de voz ou áudio/vídeo por IA para simular parentes, executivos ou autoridades.",
            "pix": "Golpe do falso extorno, falso encarte Pix, ou indução à transferência emergencial sob pânico."
        }
        
        context_matches = [v for k, v in known_tactics.items() if k in query.lower()]
        
        return {
            "query": query,
            "tactics_detected": context_matches or ["Engenharia social e exploração de vulnerabilidade humana/sistêmica."],
            "status": "enriched"
        }

    def get_threat_context(self, threat_name: str) -> str:
        """Gera um pacote de contexto completo sobre uma ameaça para o analisador LLM."""
        fraud_data = self.scrape_fraud_database(threat_name)
        rss_articles = self.fetch_rss_feeds()
        
        context_str = f"Nome da Ameaça: {threat_name}\n\n"
        context_str += f"Táticas Conhecidas e Padrões: {' '.join(fraud_data['tactics_detected'])}\n\n"
        
        if rss_articles:
            context_str += "Alertas e Notícias Recentes Correlacionadas:\n"
            for art in rss_articles[:3]:
                context_str += f"- {art['title']}: {art['summary']}\n"
                
        return context_str
