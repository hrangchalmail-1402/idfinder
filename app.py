import streamlit as st
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="Officer ID Checker", page_icon="🔍", layout="centered")

st.title("📋 ID Finder")
st.write("Enter ID below")

# Load the data source safely
CSV_FILE = "datasource.csv"

@st.cache_data
def load_data(file_path):
    try:
        # Read CSV and convert the ID column to string to avoid format mismatches
        df = pd.read_csv(file_path)
        if not df.empty:
            df.columns = df.columns.str.strip()  # Clean up whitespace from headers
        return df
    except FileNotFoundError:
        st.error(f"⚠️ Data source error: '{file_path}' not found. Please make sure the file is in the repository.")
        return None

df = load_data(CSV_FILE)

if df is not None:
    # 1. Provide an option to view all data for transparency
    with st.expander("👁️ View Full Officer Directory"):
        st.dataframe(df, use_container_width=True)
    
    # 2. Search Section
    st.subheader("🔍 Online ID Search")
    
    # We assume your ID column is named 'Officer ID' or 'ID'. Modify if different.
    id_column = [col for col in df.columns if 'id' in col.lower() or 'number' in col.lower()]
    
    if id_column:
        search_col = id_column[0]
        search_query = st.text_input("Enter Officer ID / Number to search:", placeholder="e.g., PO-102").strip()
        
        if search_query:
            # Filter the dataframe for exact or partial matches
            result = df[df[search_col].astype(str).str.lower() == search_query.lower()]
            
            if not result.empty:
                st.success("✅ Record Found!")
                # Display results nicely formatted
                for index, row in result.iterrows():
                    st.markdown("---")
                    for col in df.columns:
                        st.markdown(f"**{col}:** {row[col]}")
            else:
                st.error("❌ No officer found with that ID. Please check the spelling or number.")
    else:
        st.warning("⚠️ Could not automatically detect an 'ID' or 'Number' column in your CSV. Please ensure your CSV has an 'Officer ID' column.")