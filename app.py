"""Spam Email Detector — Tinashe Clifford Makandise."""
from pathlib import Path
import streamlit as st
from src.app_support import load_artifacts, classify, MAX_CHARACTERS

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Spam Email Detector', page_icon='📨', layout='centered')

@st.cache_resource
def get_artifacts():
    return load_artifacts(ROOT)

st.caption('NLP PORTFOLIO · TINASHE CLIFFORD MAKANDISE')
st.title('📨 Spam Email Detector')
st.write('Paste an email to predict whether it resembles spam or ham (non-spam).')
try:
    model, metadata = get_artifacts()
except Exception:
    st.error('The model could not be loaded. Check that both files in models/ are present and install requirements.txt. See README.md for troubleshooting.')
    st.stop()

EXAMPLES = {
    'Meeting email': 'Subject: Project meeting\nHi team, please join tomorrow at 10 AM to discuss the project report and next steps. Thanks.',
    'Prize promotion': 'Subject: Claim your free cash prize\nCongratulations! You have won a cash prize. Click now to claim your free reward. Limited offer!',
}
def fill_example(name):
    st.session_state['email_text'] = EXAMPLES[name]

def clear_email():
    st.session_state['email_text'] = ''

with st.sidebar:
    st.subheader('Try an example')
    for name in EXAMPLES:
        st.button(name, on_click=fill_example, args=(name,), use_container_width=True)
    st.caption('Invented examples demonstrate the interface; they are not additional evaluation data.')
    st.divider()
    st.caption('Model: TF-IDF + Logistic Regression')

email = st.text_area('Email text', key='email_text', height=240, max_chars=MAX_CHARACTERS,
                     placeholder='Paste the subject and message here…')
left, right = st.columns([3, 1])
check = left.button('Check email', type='primary', use_container_width=True)
right.button('Clear', on_click=clear_email, use_container_width=True)
if check:
    result = classify(email, model)
    if result['status'] != 'ok':
        st.warning(result['message'])
    else:
        if result['label'] == 'Spam':
            st.warning('Prediction: Spam')
        else:
            st.info('Prediction: Ham (non-spam)')
        st.metric('Model spam score', f"{result['spam_score']:.1%}")
        st.progress(result['spam_score'])
        st.caption('This uncalibrated model estimate is not a guarantee. A ham prediction does not establish that an email is safe.')

st.caption('The app does not write submitted email text to files or a database. Text is processed in the running app session; avoid pasting confidential information into public demos.')
with st.expander('Model evaluation and limitations'):
    m = metadata['test_metrics']
    cols = st.columns(3)
    for col, label, key in zip(cols, ['Test accuracy', 'Spam F1', 'Spam recall'], ['accuracy', 'spam_f1', 'spam_recall']):
        col.metric(label, f'{m[key]:.2%}')
    st.write(f"Evaluated on {m['test_rows']:,} held-out emails: {m['fp']} legitimate emails flagged and {m['fn']} spam messages missed.")
    st.write('Training used a historical English email corpus from MIT OpenCourseWare. Normalised message groups were separated during validation and testing. Results may differ on current inboxes and other languages.')
    st.write('This app classifies pasted text. It does not inspect attachments, verify senders or detect phishing reliably.')
    st.link_button('Dataset source: MIT OpenCourseWare', 'https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/resources/emails/')
