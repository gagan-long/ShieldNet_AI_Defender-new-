from sklearn.ensemble import IsolationForest
import numpy as np

class QueryAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01)
        self.query_logs = []
        
    def log_query(self, query):
        features = [
            len(query),
            len(query.split()),
            sum(c.isdigit() for c in query)
        ]
        self.query_logs.append(features)
        
    def detect_anomalies(self):
        X = np.array(self.query_logs[-1000:] or [[0,0,0]])  # Use last 1000 queries
        self.model.fit(X)
        preds = self.model.predict(X)
        return {
            "anomaly_count": int(sum(preds == -1)),
            "recent_queries": X[-10:].tolist()
        }
