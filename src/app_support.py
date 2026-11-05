"""Load trusted local artifacts and classify text without saving submissions."""
from pathlib import Path
import hashlib
import json
import joblib
import sklearn

MAX_CHARACTERS = 50000

def load_artifacts(root):
    root = Path(root)
    metadata = json.loads((root / 'models/model_metadata.json').read_text(encoding='utf-8'))
    model_path = root / 'models/spam_pipeline.joblib'
    if hashlib.sha256(model_path.read_bytes()).hexdigest() != metadata['model_sha256']:
        raise ValueError('Model checksum does not match its metadata. Restore both model files from the package.')
    if sklearn.__version__ != metadata['versions']['scikit-learn']:
        raise ValueError('The scikit-learn version differs from training. Install requirements.txt in the app environment.')
    model = joblib.load(model_path)
    if list(model.classes_) != [0, 1]:
        raise ValueError('Unexpected class mapping.')
    return model, metadata

def classify(text, model):
    if not isinstance(text, str) or not text.strip():
        return {'status': 'invalid', 'message': 'Paste an email before checking.'}
    if len(text) > MAX_CHARACTERS:
        return {'status': 'invalid', 'message': 'Use no more than 50,000 characters per email.'}
    features = model.named_steps['tfidf'].transform([text])
    if features.nnz == 0:
        return {'status': 'unsupported', 'message': 'No recognised text features. Try a fuller email in English.'}
    classifier = model.named_steps['classifier']
    label = int(classifier.predict(features)[0])
    score = float(classifier.predict_proba(features)[0, list(classifier.classes_).index(1)])
    return {'status': 'ok', 'label': 'Spam' if label else 'Ham', 'spam_score': score}
