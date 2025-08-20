#@title Reddit Comment Search Streamlit App (w/ Word Cloud & Sentiment)
import streamlit as st
import pandas as pd
import praw
from datetime import datetime, timezone
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

# -- Load Reddit API credentials from Streamlit secrets --
REDDIT_CLIENT_ID = st.secrets["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = st.secrets["REDDIT_CLIENT_SECRET"]
REDDIT_USER_AGENT = "reddit-search-app by u/your_username"

# -- Initialize Reddit client --
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# -- Function to search comments --
def search_reddit_comments(subreddit_name, keyword, limit=500):
    subreddit = reddit.subreddit(subreddit_name)
    comments = []
    for comment in subreddit.comments(limit=limit):
        if keyword.lower() in comment.body.lower():
            comments.append({
                "author": str(comment.author),
                "created_utc": datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                "body": comment.body,
                "permalink": f"https://reddit.com{comment.permalink}"
            })
    return pd.DataFrame(comments)

# -- Streamlit UI --
st.title("🔎 Reddit Comment Search (Live via Reddit API)")

subreddit_input = st.text_input("Subreddit", value="GooglePixel")
keyword_input = st.text_input("Keyword", value="calling")
max_comments = st.slider("Max Comments to Search", min_value=100, max_value=1000, step=100, value=500)

df = pd.DataFrame()

# Initialize df in session_state if not already present
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Search button
if st.button("Search"):
    with st.spinner("Fetching comments..."):
        df = search_reddit_comments(subreddit_input, keyword_input, max_comments)
        st.session_state.df = df  # save to session

# Retrieve from session state
df = st.session_state.df

if not df.empty:
    st.success(f"Found {len(df)} matching comments.")
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "reddit_comments.csv")


# -- Word Cloud & Sentiment --
if not df.empty:
    if st.checkbox("Show Word Cloud"):
        text = " ".join(df["body"].tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        st.subheader("Word Cloud")
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    if st.checkbox("Run Sentiment Analysis"):
        def get_sentiment(text):
            return TextBlob(text).sentiment.polarity

        df["sentiment"] = df["body"].apply(get_sentiment)
        avg_sentiment = df["sentiment"].mean()

        st.subheader("Sentiment Analysis")
        st.write(f"**Average Sentiment Polarity:** `{avg_sentiment:.3f}` (range: -1 to 1)")
        st.bar_chart(df["sentiment"])
else:
    st.info("Run a search to enable Word Cloud or Sentiment options.")
