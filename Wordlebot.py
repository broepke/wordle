import streamlit as st
from collections import Counter

# Initialize session state to keep track of inputs and radio button states
if 'inputs' not in st.session_state:
    st.session_state.inputs = [["" for _ in range(5)] for _ in range(5)]
if 'radio_states' not in st.session_state:
    st.session_state.radio_states = [["Select" for _ in range(5)] for _ in range(5)]

# Function to read words from a file
def read_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file if len(line.strip()) == 5]

# Function to filter words based on specific criteria, exclusion list, and exclude positions for certain letters
def filter_words(words, criteria, exclude_letters, exclude_positions_for_letters):
    exclude_letters_set = set(exclude_letters)

    # Remove letters from exclude list if they are in criteria or exclude_positions_for_letters
    letters_to_keep = set(criteria.values()).union(exclude_positions_for_letters.keys())
    exclude_letters_set.difference_update(letters_to_keep)

    # Filter words based on green letter criteria
    green_filtered_words = []
    for word in words:
        match = True
        for position, char in criteria.items():
            if word[position] != char:
                match = False
                break
        if match:
            green_filtered_words.append(word)

    st.write("Words matching green letter criteria:")
    st.write(len(green_filtered_words))

    # Filter words based on yellow letter criteria
    yellow_filtered_words = []
    for word in green_filtered_words:
        match = True
        for letter, positions in exclude_positions_for_letters.items():
            if letter not in word:
                match = False
                break
            if any(word[pos] == letter for pos in positions):
                match = False
                break
        if match:
            yellow_filtered_words.append(word)

    st.write("Words matching yellow letter criteria:")
    st.write(len(yellow_filtered_words))

    # Exclude words containing grey letters
    final_filtered_words = []
    for word in yellow_filtered_words:
        if not any(char in exclude_letters_set for char in word):
            final_filtered_words.append(word)

    st.write("Words matching all criteria (excluding grey letters):")
    st.write(len(final_filtered_words))
    st.write(final_filtered_words)

    return final_filtered_words

# Function to calculate letter frequencies for specific positions based on filtered words
def calculate_frequencies(words, exclude_positions):
    letter_counts = Counter()
    for word in words:
        for i, char in enumerate(word):
            if i not in exclude_positions:
                letter_counts[char] += 1
    return letter_counts

# Improved function to score words with more nuanced criteria, using frequencies from remaining valid words
def score_words(words, frequencies, exclude_positions):
    def word_score(word):
        # Base score from letter frequencies
        score = sum(frequencies[char] for i, char in enumerate(word) if i not in exclude_positions)
        
        # Calculate the number of duplicate letters and apply a heavy penalty
        duplicate_count = len(word) - len(set(word))
        score -= duplicate_count * 20  # Increased penalty for duplicate letters
        
        # Penalize words ending with 's'
        if word[-1] == 's':
            score -= 5
        
        # Bonus for diverse letters (mix of common and rare)
        diversity_bonus = len(set(word)) * 3
        score += diversity_bonus
        
        # Positional importance (more weight to first and last letters)
        if word[0] in frequencies:
            score += frequencies[word[0]] * 1.5
        if word[-1] in frequencies:
            score += frequencies[word[-1]] * 1.5
        
        return score
    
    return sorted(words, key=word_score, reverse=True)

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
    st.write("## Debugging Info")
    st.write(f"Criteria: {criteria}")
    st.write(f"Exclude Letters: {exclude_letters}")
    st.write(f"Exclude Positions for Letters: {exclude_positions_for_letters}")

    # Read the words from the file
    words = read_words('words.txt')

    # Filter the words based on criteria and exclusions
    filtered_words = filter_words(words, criteria, exclude_letters, exclude_positions_for_letters)

    # Calculate frequencies based on remaining valid words
    frequencies = calculate_frequencies(filtered_words, exclude_positions)

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
    st.title("Streamlit Wordlebot")

    # Create a 5x5 grid for input boxes and radio buttons
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            with cols[col]:
                key_input = f"input_{row}_{col}"
                key_radio = f"radio_{row}_{col}"
                st.session_state.inputs[row][col] = st.text_input(f"Input ({row+1},{col+1})", key=key_input)
                st.session_state.radio_states[row][col] = st.radio("Color", ["❓", "⬜", "🟩", "🟨"], key=key_radio, horizontal=True)

    # Submit button to process the inputs
    if st.button("Submit"):
        submit()

if __name__ == "__main__":
    main()