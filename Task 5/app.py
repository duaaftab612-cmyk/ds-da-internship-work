!pip install -q streamlit pyngrok pandas plotly
from google.colab import files
files.upload()

app_code = """
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Superstore Dashboard', layout='wide')

st.title(' Global Superstore Interactive Dashboard')

@st.cache_data
def load_data():
    df = pd.read_csv('Global superstore.csv', encoding='latin1')
    df.columns = df.columns.str.strip()
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False, errors='coerce')
    df = df.dropna(subset=['Order Date'])
    return df

df = load_data()

# SIDEBAR FILTERS
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Region", df['Region'].unique(), df['Region'].unique())
category = st.sidebar.multiselect("Category", df['Category'].unique(), df['Category'].unique())
segment = st.sidebar.multiselect("Segment", df['Segment'].unique(), df['Segment'].unique())

filtered = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Segment'].isin(segment))
]

# KPIs
st.metric(" Sales", f"${filtered['Sales'].sum():,.2f}")
st.metric(" Profit", f"${filtered['Profit'].sum():,.2f}")
st.metric(" Orders", filtered.shape[0])

# REGION SALES
fig1 = px.bar(
    filtered.groupby('Region')['Sales'].sum().reset_index(),
    x='Region',
    y='Sales',
    color='Region'
)

st.plotly_chart(fig1, use_container_width=True)

# CATEGORY SALES
fig2 = px.pie(
    filtered.groupby('Category')['Sales'].sum().reset_index(),
    names='Category',
    values='Sales'
)

st.plotly_chart(fig2, use_container_width=True)

# TOP CUSTOMERS
top_customers = (
    filtered.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig3 = px.bar(top_customers, x='Customer Name', y='Sales', color='Sales')

st.plotly_chart(fig3, use_container_width=True)
"""

with open("app.py", "w") as f:
    f.write(app_code)

print("app.py created ")
!streamlit run app.py &>/content/logs.txt &
print("Streamlit started ")
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared-linux-amd64

!./cloudflared-linux-amd64 tunnel --url http://localhost:8501
