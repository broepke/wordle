import streamlit as st
from utilities import calculate_frequencies, filter_words, score_words, read_words

# Initialize session state to keep track of inputs and radio button states
if "inputs" not in st.session_state:
    st.session_state.inputs = [["" for _ in range(5)] for _ in range(5)]
if "radio_states" not in st.session_state:
    st.session_state.radio_states = [["Select" for _ in range(5)] for _ in range(5)]


# Function to handle the submission
def submit():
    # Build criteria and exclusions from inputs
    criteria = {}
    exclude_letters = set()
    exclude_positions_for_letters = {}
    for row in range(5):
        for col in range(5):
            char = st.session_state.inputs[row][col].strip().lower()
            color = st.session_state.radio_states[row][col]
            if color == "🟩" and char:
                criteria[col] = char
            elif color == "⬜" and char:
                exclude_letters.add(char)
            elif color == "🟨" and char:
                if char not in exclude_positions_for_letters:
                    exclude_positions_for_letters[char] = []
                exclude_positions_for_letters[char].append(col)

    exclude_positions = set(criteria.keys())

    # Debugging output to verify criteria and exclusions
    # st.write("## Results")

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
    st.write("## Sorted Filtered Words")
    if sorted_filtered_words:
        for word in sorted_filtered_words[:25]:
            st.write(word)
    else:
        st.write("No words match the given criteria.")


def main():
    st.title("WordleBrian")

    # Create a 5x5 grid for input boxes and radio buttons
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            with cols[col]:
                key_input = f"input_{row}_{col}"
                key_radio = f"radio_{row}_{col}"
                st.session_state.inputs[row][col] = st.text_input(
                    f"Input ({row+1},{col+1})", key=key_input
                )
                st.session_state.radio_states[row][col] = st.radio(
                    "Color", ["❓", "⬜", "🟩", "🟨"], key=key_radio, horizontal=True
                )

    # Submit button to process the inputs
    if st.button("Submit"):
        submit()


if __name__ == "__main__":
    main()
