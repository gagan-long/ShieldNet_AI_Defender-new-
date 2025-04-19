from art.estimators.classification import SklearnClassifier
from art.attacks.evasion import FastGradientMethod
import numpy as np

class AdversarialDetector:
    def __init__(self, model):
        self.classifier = SklearnClassifier(model=model)
        self.attack = FastGradientMethod(estimator=self.classifier, eps=0.1)

    def detect(self, input_data):
        # Generate adversarial example
        adversarial_sample = self.attack.generate(x=np.array([input_data]))
        
        # Compare predictions
        original_pred = self.classifier.predict(np.array([input_data]))[0]
        adversarial_pred = self.classifier.predict(adversarial_sample)[0]
        
        return {
            "is_adversarial": not np.argmax(original_pred) == np.argmax(adversarial_pred),
            "confidence_diff": float(np.max(adversarial_pred) - np.max(original_pred))
        }

# Usage: detector = AdversarialDetector(your_scikit_model)
from core.adversarial_detection.detector import AdversarialDetector
import numpy as np

# Load test case
with open('core/adversarial_detection/test_cases/fgsm_attack.txt') as f:
    line = next(l for l in f if l.startswith('Normalized pixel values'))
    attack_sample = np.array(
        [float(x) for x in line.split(':')[1].strip(' []\n').split(',')]
    )

# Example model (replace with actual trained model)
from sklearn.linear_model import LogisticRegression
model = LogisticRegression().fit(X_train, y_train)  # Dummy training

detector = AdversarialDetector(model)
result = detector.detect(attack_sample)

# Train a sample model first
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

iris = load_iris()
X, y = iris.data, iris.target
model = LogisticRegression().fit(X, y)

detector = AdversarialDetector(model)
result = detector.detect(X[0])  # Use actual sample

