import pandas as pd
import streamlit as st
from collections import Counter
import os
import altair as alt

def main():
    st.title("Distribution of Letters")

    # Construct the path to the words.txt file
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'words.txt')
    
    # Error handling for file reading
    try:
        with open(file_path, 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) == 5]
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return

    # Count the frequency of each letter in the list of words
    letter_counts = Counter("".join(words))

    # Convert the counter to a DataFrame for better visualization
    letter_counts_df = pd.DataFrame.from_dict(letter_counts, orient='index', columns=['Count']).reset_index()
    letter_counts_df = letter_counts_df.rename(columns={'index': 'Letter'})

    # Sort the DataFrame by Count in descending order
    letter_counts_df = letter_counts_df.sort_values(by='Count', ascending=False)

    # Reset the index to have a sequential order
    letter_counts_df = letter_counts_df.reset_index(drop=True)

    # Create an Altair bar chart
    chart = alt.Chart(letter_counts_df).mark_bar().encode(
        x=alt.X('Letter', sort=None),
        y='Count',
        color=alt.value("#F63366")
    ).properties(
        width=600,
        height=400
    )

    # Display the Altair chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()