import streamlit as st
import pandas as pd


st.title("Past Answers")
st.write("Below is a list of past Wordle answers from [Beebom.com](https://beebom.com/past-wordle-answers/).")

url = "https://beebom.com/past-wordle-answers/"
tables = pd.read_html(url)

# Combine all HTML Tables into One
combined_df = pd.concat(tables, ignore_index=True)

# Only keep the colunmsn we need
combined_df = combined_df[["Date", "Wordle Answer"]].copy()

# Convert Date to datetime
combined_df['Date'] = pd.to_datetime(combined_df['Date'], format='mixed', errors='coerce')

# Drop the index from the Dataframe
combined_df.reset_index(drop=True, inplace=True)

# Display the Dataframe
st.dataframe(combined_df, use_container_width=True)