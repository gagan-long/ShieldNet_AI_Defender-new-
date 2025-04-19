from transformers import pipeline
from pymisp import ExpandedPyMISP
from core.phishing_detection.nlp_analyzer import PhishingAnalyzer
from config import ConfigLoader
import re
import os

class PhishingAnalyzer:
    def __init__(self, misp_url, misp_key):
        self.nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.misp = ExpandedPyMISP(misp_url, misp_key)
        self.phishing_keywords = self._load_keywords()
        
    
        self.config = ConfigLoader().load_model_config()
        self.threshold = self.config['phishing']['min_confidence']

    def _load_keywords(self):
        """Load from threat feeds using environment variable"""
        threat_feed_path = os.getenv(
            'THREAT_FEED_PATH', 
            'core/phishing_detection/threat_feeds'
        )
        with open(f'{threat_feed_path}/malicious_keywords.txt') as f:
            return [line.strip() for line in f if not line.startswith('#')]

    def update_threat_feeds(self):
        """Auto-update from MISP"""
        domains = self.misp.search(type_attribute="domain")
        with open('core/phishing_detection/threat_feeds/known_phishing_domains.txt', 'a') as f:
            f.write('\n'.join(d['value'] for d in domains))

    def analyze_text(self, text):
        # Existing analysis logic
        # ... (keep previous implementation)

        # Add domain check
        domains = re.findall(r'https?://([\w\.-]+)', text)
        with open('core/phishing_detection/threat_feeds/known_phishing_domains.txt') as f:
            blacklist = [line.strip() for line in f if not line.startswith('#')]
        
        malicious_domains = [d for d in domains if d in blacklist]
        
        return {
            **previous_result,
            "malicious_domains": malicious_domains
        }

analyzer = PhishingAnalyzer(
    misp_url="https://your-misp-instance.com",
    misp_key="your_api_key"
)

# Auto-update threat feeds
analyzer.update_threat_feeds()

result = analyzer.analyze_text("URGENT: Reset your password now!")





    
