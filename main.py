# main.py (updated with required field highlights)
import streamlit as st
import pandas as pd
import hashlib
import os
import logging
import plotly.express as px
from constants import STATUS_ALIVE, STATUS_DEAD
from ocr_utils import extract_text_from_image, clean_post_content
from parser import parse_details_from_text
from config import ensure_config, load_config

# Setup
DATA_FILE = 'turtle_release_records.csv'
LOG_FILE = 'logs/app.log'
EXPECTED_COLUMNS = [
    'Date', 'Time', 'Account Name (Manual)', 'Account Name (Detected)',
    'Post Date (Detected)', 'Post Content', 'Location', 'Turtle Count',
    'Province', 'District', 'Species', 'Interaction', 'Status', 'Content Hash'
]

os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ensure_config()
CONFIG = load_config()

st.set_page_config(page_title="Marine Turtle Release Monitor", layout="wide")

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(DATA_FILE, index=False)

def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
        missing = set(EXPECTED_COLUMNS) - set(data.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        return data
    except Exception as e:
        logging.warning(f"Malformed CSV, recreating. Error: {e}")
        pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(DATA_FILE, index=False)
        return pd.read_csv(DATA_FILE)

def hash_post_content(text):
    try:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    except Exception as e:
        logging.error(f"Hashing failed: {e}")
        return ""

data = load_data()

st.title("🐢 Marine Turtle Release Monitoring Tool")
st.markdown("""
Automatically extract turtle release or stranding info from social media posts and screenshots.
Supports Green, Olive Ridley, Leatherback, Loggerhead, and Hawksbill turtles.
""")

post_content = ""
show_preview = False

with st.expander("➕ Add New Turtle Release Record", expanded=True):
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date of Entry", value=pd.to_datetime("today"))
            time = st.time_input("Time of Entry")
            account_manual = st.text_input("Account Name (Manual) [Optional]")
            override_status = st.selectbox("Override Status *", ["", "Alive", "Dead", "Released Alive", "Released Dead", "Unknown"])
            override_species = st.selectbox("Species (Override)", ["", "Green Turtle", "Olive Ridley", "Leatherback", "Loggerhead", "Hawksbill"])
        with col2:
            location_manual = st.text_input("Location (Optional)")
            screenshot = st.file_uploader("Upload Screenshot (Preferred)", type=["png", "jpg", "jpeg"])
            override_interaction = st.selectbox("Interaction (Override)", ["", "Stranded", "Sighted", "Bycatch"])

        post_content_input = st.text_area("Post Text (Optional)")
        override_count = st.number_input("Turtle Count (Override) *", min_value=0, value=0)
        override_province = st.text_input("Province (Override) *")
        override_district = st.text_input("District (Override)")

        submit = st.form_submit_button("Save Record")

        if submit:
            with st.spinner("🔍 Processing..."):
                if screenshot:
                    if screenshot.size > 5 * 1024 * 1024:
                        st.toast("File too large. Please upload files < 5MB.", icon="❗")
                        st.stop()
                    post_content = clean_post_content(extract_text_from_image(screenshot))
                else:
                    post_content = clean_post_content(post_content_input.strip())

                details = parse_details_from_text(post_content)
                detected_account = details.get('account_name') or account_manual
                detected_post_date = details.get('post_date') or date

                turtle_count = override_count or details.get('turtle_count')

                status_map = {
                    "Released Alive": "Alive",
                    "Released Dead": "Dead",
                    "Alive": "Alive",
                    "Dead": "Dead",
                    "Unknown": "Unknown"
                }
                raw_status = (override_status or details.get('status') or '').strip().title()
                status = status_map.get(raw_status, "Unknown")

                species_map = {
                    "Green Turtle": "Green Turtle",
                    "Olive Ridley": "Olive Ridley",
                    "Leatherback": "Leatherback",
                    "Loggerhead": "Loggerhead",
                    "Hawksbill": "Hawksbill"
                }
                raw_species = (override_species or details.get('species') or '').strip().title()
                species = species_map.get(raw_species, "Unknown")

                interaction_map = {
                    "Stranded": "Stranded",
                    "Sighted": "Sighted",
                    "Bycatch": "Bycatch"
                }
                raw_interaction = (override_interaction or details.get('interaction') or '').strip().title()
                interaction = interaction_map.get(raw_interaction, "Unknown")

                detected_location = (location_manual or details.get('area') or '').strip().title()
                province = (override_province or details.get('province') or '').strip().title()
                district = (override_district or details.get('district') or '').strip().title()

                missing_fields = []
                if not post_content:
                    st.toast("⚠️ No post content found.", icon="⚠️")
                if turtle_count is None or turtle_count <= 0:
                    missing_fields.append("Turtle Count")
                if not province:
                    missing_fields.append("Province")
                if not status:
                    missing_fields.append("Status")

                if missing_fields:
                    st.warning(f"⚠️ Missing crucial fields: {', '.join(missing_fields)}. Please complete manually.")
                else:
                    content_hash = hash_post_content(post_content)
                    if not data.empty and content_hash in data['Content Hash'].values:
                        st.info("ℹ️ Duplicate post detected. Not added.")
                    else:
                        new_entry = pd.DataFrame([{
                            'Date': date,
                            'Time': time,
                            'Account Name (Manual)': account_manual,
                            'Account Name (Detected)': detected_account,
                            'Post Date (Detected)': detected_post_date,
                            'Post Content': post_content,
                            'Location': detected_location,
                            'Turtle Count': turtle_count,
                            'Province': province,
                            'District': district,
                            'Species': species,
                            'Interaction': interaction,
                            'Status': status,
                            'Content Hash': content_hash
                        }])
                        new_entry.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
                        st.success("✅ Record saved.")
                        data = load_data()
                        show_preview = True



if show_preview:
    st.markdown("### 📝 OCR Text Preview")
    st.code(post_content[:500] + "...", language="markdown")

with st.expander("📊 Dashboard & Analysis"):
    if not data.empty:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data['Post Date (Detected)'] = pd.to_datetime(data['Post Date (Detected)'], errors='coerce')
        data = data.dropna(subset=['Post Date (Detected)'])

        st.subheader("Turtle Status")
        status_df = data['Status'].value_counts().reset_index()
        status_df.columns = ['Status', 'Count']
        st.plotly_chart(px.bar(status_df, x='Status', y='Count'))

        st.subheader("Location × Status")
        loc_stat = data.groupby(['Location', 'Status']).size().reset_index(name='Count')
        st.plotly_chart(px.bar(loc_stat, x='Location', y='Count', color='Status', barmode='group'))

        st.subheader("Releases by District")
        district_df = data['District'].value_counts().reset_index()
        district_df.columns = ['District', 'Count']
        st.plotly_chart(px.bar(district_df, x='District', y='Count'))

        st.subheader("Monthly Trends")
        trend = data.groupby(data['Post Date (Detected)'].dt.to_period('M')).size().reset_index(name='Count')
        trend['Post Date (Detected)'] = trend['Post Date (Detected)'].astype(str)
        st.plotly_chart(px.line(trend, x='Post Date (Detected)', y='Count'))

        st.subheader("Posts per Account")
        account_df = data['Account Name (Detected)'].value_counts().reset_index()
        account_df.columns = ['Account', 'Count']
        st.plotly_chart(px.bar(account_df, x='Account', y='Count'))

        st.subheader("Species Distribution")
        species_df = data['Species'].value_counts().reset_index()
        species_df.columns = ['Species', 'Count']
        st.plotly_chart(px.pie(species_df, names='Species', values='Count'))

        st.subheader("Interaction Types")
        interaction_df = data['Interaction'].value_counts().reset_index()
        interaction_df.columns = ['Interaction', 'Count']
        st.plotly_chart(px.bar(interaction_df, x='Interaction', y='Count'))


with st.expander("📄 View & Download Records"):
    keyword = st.text_input("Search keyword")
    filtered = data[data.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)] if keyword else data
    st.dataframe(filtered, use_container_width=True)
    st.download_button("Download CSV", data=filtered.to_csv(index=False), file_name="turtle_release_log.csv")

with st.expander("🧹 Admin: Clear Records"):
    if st.checkbox("I confirm I want to permanently delete all records."):
        if st.button("❌ Clear All Data"):
            pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(DATA_FILE, index=False)
            st.success("✅ All records cleared.")

with st.expander("🛠️ Admin: App Logs"):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            st.code(f.read(), language="log")
    else:
        st.info("No logs found.")
