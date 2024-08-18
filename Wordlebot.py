import streamlit as st
from utilities import calculate_frequencies, filter_words, score_words, read_words

# Initialize session state to keep track of inputs, radio button states, entered words, and remaining words count
if "inputs" not in st.session_state:
    st.session_state.inputs = [["" for _ in range(5)] for _ in range(5)]
if "radio_states" not in st.session_state:
    st.session_state.radio_states = [["❓" for _ in range(5)] for _ in range(5)]
if "entered_words" not in st.session_state:
    st.session_state.entered_words = []
if "remaining_words" not in st.session_state:
    st.session_state.remaining_words = []

# Function to handle the submission
def submit():
    # Build criteria and exclusions from inputs
    criteria = {}
    exclude_letters = set()
    exclude_positions_for_letters = {}
    entered_word = ""

    # Find the last row that contains inputs to determine the entered word
    for row in range(5):
        row_word = "".join(st.session_state.inputs[row]).strip().lower()
        if row_word:  # Check if the row has any entered characters
            entered_word = row_word

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

    # Store the current word entry and remaining words count
    if entered_word:
        st.session_state.entered_words.append(entered_word)
        st.session_state.remaining_words.append(len(sorted_filtered_words))

    # Display the results
    st.write("## Top Selected Words")
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
                if f"input_{row}_{col}" not in st.session_state:
                    st.session_state[f"input_{row}_{col}"] = ""
                if f"radio_{row}_{col}" not in st.session_state:
                    st.session_state[f"radio_{row}_{col}"] = "❓"
                st.session_state.inputs[row][col] = st.text_input(
                    f"Input ({row+1},{col+1})", key=key_input, value=st.session_state[f"input_{row}_{col}"]
                )
                st.session_state.radio_states[row][col] = st.radio(
                    "Color", ["❓", "⬜", "🟩", "🟨"], key=key_radio, horizontal=True, index=["❓", "⬜", "🟩", "🟨"].index(st.session_state[f"radio_{row}_{col}"])
                )

    # Submit button to process the inputs
    if st.button("Submit"):
        submit()

    # Sidebar to display the entered words and remaining words count
    st.sidebar.write("**Word + Remaining Words**")
    for word, count in zip(st.session_state.entered_words, st.session_state.remaining_words):
        st.sidebar.write(f"{word.upper()}: {count} ")

if __name__ == "__main__":
    main()