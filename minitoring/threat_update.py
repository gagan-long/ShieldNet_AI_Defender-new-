# monitoring/threat_update.py
def rotate_feeds():
    s3.download_file('threat-feeds', 'latest-domains.txt', 'data/feeds/domains.txt')
    reload_phishing_analyzer()
