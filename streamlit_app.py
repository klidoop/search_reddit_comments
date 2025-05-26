#@title Reddit Comment Search Streamlit App
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def search_comments(subreddit, keyword, start_date, end_date, size=100):
    start_epoch = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_epoch = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    url = "https://api.pushshift.io/reddit/comment/search"
    params = {
        "subreddit": subreddit,
        "q": keyword,
        "after": start_epoch,
        "before": end_epoch,
        "size": size
    }

    res = requests.get(url, params=params)
    data = res.json().get("data", [])
    return pd.DataFrame([{
        "author": d.get("author"),
        "created_utc": datetime.utcfromtimestamp(d.get("created_utc")),
        "body": d.get("body"),
        "permalink": f"https://reddit.com{d.get('permalink')}"
    } for d in data])

# Streamlit UI
st.title("🔍 Reddit Comment Search")

subreddit = st.text_input("Subreddit", value="stocks")
keyword = st.text_input("Keyword", value="NVIDIA")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Search"):
    with st.spinner("Searching..."):
        df = search_comments(subreddit, keyword, str(start_date), str(end_date))
        if df.empty:
            st.warning("No comments found.")
        else:
            st.success(f"Found {len(df)} comments.")
            st.dataframe(df)
            st.download_button("Download CSV", df.to_csv(index=False), "results.csv")
