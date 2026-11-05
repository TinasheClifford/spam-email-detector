# Spam Email Detector with NLP
## Live Demo

[Try the Spam Email Detector](https://spam-email-detector-2jiq4vl823c77pgw28d2te.streamlit.app/)

Author: **Tinashe Clifford Makandise**

An educational Python project that classifies pasted English email text with TF-IDF and Logistic Regression. Includes the evaluated model, five executed notebooks, performance reports and a Streamlit interface.

## Open on Windows

1. Extract the ZIP using **Extract All**. A short location such as `Documents\spam-detector` is convenient.
2. Open the extracted `spam-email-detector` folder containing `app.py`.
3. Double-click **setup_windows.bat** once. It creates `%USERPROFILE%\spam-env` and installs the app dependencies. Internet is needed for setup; let it finish.
4. Double-click **start_windows.bat**. Keep its command window open. If the browser does not open, visit http://localhost:8501.
5. Paste text and click **Check email**. Use **Clear** to remove it or try the invented sidebar examples.

After restarting your computer, double-click **start_windows.bat** again. Stop the server with Ctrl+C or close its command window. Do not open the ZIP with Python or Streamlit. The launchers assume `python` points to an installed supported Python interpreter; Python 3.12 or 3.13 is recommended. The exported model was trained on Python 3.12.14 with scikit-learn 1.8.0. Keep the pinned inference versions.

The environment is deliberately placed outside the long project path to reduce Windows path-length problems. No administrator access or virtual-environment activation is required. If setup fails due to connectivity, reconnect and rerun setup; cached downloads can be reused. If the environment was created using an incompatible Python version, create a fresh environment with Python 3.12/3.13 and use its interpreter instead.

## Run manually

Run each command separately from the extracted project folder:

```bat
python -m venv "%USERPROFILE%\spam-env"
```
```bat
"%USERPROFILE%\spam-env\Scripts\python.exe" -m pip install --timeout 120 --retries 10 -r requirements.txt
```
```bat
"%USERPROFILE%\spam-env\Scripts\python.exe" -m streamlit run app.py
```

On Linux/macOS: create a virtual environment, install `requirements.txt`, then run `python -m streamlit run app.py` with that environment's Python.

## Dataset and reproducibility

Source: [MIT OpenCourseWare, The Analytics Edge — emails dataset](https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/resources/emails/).

[Direct CSV download](https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/67f7be241f1b459d7fdb8e9031384338_emails.csv).

The original data has 5,728 rows and columns `text` and `spam` (0=ham, 1=spam). Thirty-three exact duplicates were removed. Unicode/case/whitespace-normalised message groups were kept together when splitting. The resulting training partition has 4,547 rows and the reserved test partition has 1,148. Grouping does not eliminate all related campaigns or near-duplicates.

The ZIP omits raw and processed email CSVs; the app does not need them. To reproduce, download the original CSV to `data/raw/emails.csv`, install `requirements-dev.txt`, and run the notebooks in numerical order in the same project. Notebook 1 creates the split and reports. Use the same environment throughout. Notebook 3's NLTK stemming demo is optional; the deployed pipeline does not require NLTK or corpus downloads.

1. `01_spam_email_project_overview_and_data_inspection.ipynb`
2. `02_spam_email_exploratory_text_analysis.ipynb`
3. `03_text_preprocessing_and_feature_engineering.ipynb`
4. `04_model_training_and_comparison.ipynb`
5. `05_final_evaluation_and_model_export.ipynb`

Two fixed TF-IDF representations were compared with Multinomial Naive Bayes and Logistic Regression using five-fold StratifiedGroupKFold. A majority-class baseline was included. Selection used mean spam F1; the winning representation removed built-in English stopwords. Vocabulary and IDF were fitted within each fold. The selected pipeline was fitted on training data only, evaluated on the reserved test partition and exported unchanged. The default classification decision rule was retained, without test threshold tuning.

## Final held-out results

| Metric | Result |
|---|---:|
| Accuracy | 98.52% |
| Spam precision | 98.86% |
| Spam recall | 94.89% |
| Spam F1 | 96.83% |
| Average precision | 99.79% |

Counts: 871 true ham, 260 true spam, 3 false positives and 14 false negatives. These are results on this historical dataset and split, not a guarantee for current inboxes. See `reports/final_test_metrics.json` and `reports/figures/`.

## Application files

- `app.py`: Streamlit interface.
- `src/app_support.py`: artifact validation and input classification.
- `models/spam_pipeline.joblib`: fitted TF-IDF plus classifier.
- `models/model_metadata.json`: versions, checksums and evaluation provenance.
- `requirements.txt`: pinned app dependencies.
- `setup_windows.bat`, `start_windows.bat`: Windows setup and reopening.
- `notebooks/`: complete learning and modelling workflow.
- `reports/`: aggregate analyses, settings and charts.

The app verifies the model checksum and scikit-learn version before loading. Only load trusted joblib files. Preserve the accompanying metadata. The model and notebooks include no custom serialized preprocessing functions.

## Limitations and privacy

A predicted ham label does not establish that an email is safe. The score is an uncalibrated model estimate, not verified confidence. The app does not validate senders, attachments, links or phishing. Short messages and unfamiliar vocabulary may be poorly represented; blank and zero-feature inputs are rejected. Other languages and modern spam campaigns need separate evaluation.

The app code does not write submitted email text to disk or a database, nor call a third-party prediction service. Streamlit processes text within the running session; do not paste confidential information into a public demo. There is no saved email-history feature.

## Later deployment

Upload the extracted project contents, including `src/`, `models/`, `requirements.txt` and `.streamlit/config.toml`, to a GitHub repository. Do not upload the ZIP as the app entry point. Deploy `app.py` and select Python 3.12 to match training. Public deployment has not been performed for this package.
