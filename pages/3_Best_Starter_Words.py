import streamlit as st
from utilities import calculate_frequencies, filter_words, score_words, read_words


def main():
    st.title("Best Starter Words")

    # Build criteria and exclusions from inputs
    criteria = {}
    exclude_letters = set()
    exclude_positions_for_letters = {}

    exclude_positions = set(criteria.keys())

    # Read the words from the file
    words = read_words("words.txt")

    # Calculate frequencies based on the full list of words
    frequencies = calculate_frequencies(words)

    # Filter the words based on criteria and exclusions
    filtered_words = filter_words(
        words, criteria, exclude_letters, exclude_positions_for_letters
    )

    # Score the filtered words based on the new frequencies
    sorted_filtered_words = score_words(filtered_words, frequencies, exclude_positions)

    # Display the results
    st.write("## Top Slected Words")
    if sorted_filtered_words:
        for word in sorted_filtered_words[:25]:
            st.write(word)
    else:
        st.write("No words match the given criteria.")


if __name__ == "__main__":
    main()
