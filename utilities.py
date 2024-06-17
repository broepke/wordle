# Function to get the rank of a word
from collections import Counter
import streamlit as st
from wordfreq import top_n_list

# Function to read words from a file
@st.cache_data
def read_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file if len(line.strip()) == 5]


# Get the top 100,000 words in English
top_words = top_n_list('en', 100000)

def get_word_rank(word):
    try:
        return top_words.index(word) + 1
    except ValueError:
        return None  # Word not found in the top list

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

    # st.write("Words matching green letter criteria:")
    # st.write(len(green_filtered_words))

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

    # st.write("Words matching yellow letter criteria:")
    # st.write(len(yellow_filtered_words))

    # Exclude words containing grey letters
    final_filtered_words = []
    for word in yellow_filtered_words:
        if not any(char in exclude_letters_set for char in word):
            final_filtered_words.append(word)

    st.write("Words matching all criteria:")
    st.write(len(final_filtered_words))
    # st.write(final_filtered_words)

    return final_filtered_words

# Function to calculate letter frequencies for specific positions based on full word list
def calculate_frequencies(words):
    letter_counts = Counter()
    for word in words:
        for char in word:
            letter_counts[char] += 1
    return letter_counts

# Improved function to score words with more nuanced criteria, using frequencies from full word list
def score_words(words, frequencies, exclude_positions):
    def word_score(word):
        score = 0
        # Base score from letter frequencies
        base_score = sum(frequencies[char] for i, char in enumerate(word) if i not in exclude_positions)

        # Calculate the number of duplicate letters and apply a heavier penalty
        dup_score = 1
        duplicate_count = len(word) - len(set(word))
        if duplicate_count > 0:
            dup_score = 0.5

        # Penalize words ending with 's'
        s_score = 1
        if word[-1] == 's':
            s_score = 0.1

        # Bonus for diverse vowels
        vowel_score = 0
        vowels = set('aeiou')
        unique_vowels = set(word) & vowels
        vowel_score += len(unique_vowels) * 1000

        # Add rank-based adjustment
        rank_score = 0
        rank = get_word_rank(word)
        if rank:
            rank_bonus = 100000 / rank  # Higher rank means more common, higher score
            rank_score = int(rank_bonus * 1000)
        else:
            rank_score = -5000  # Penalty if the word is not in the top 100,000 list
            
        score = base_score * dup_score * s_score + vowel_score + rank_score

        st.write(f"**{word}**")
        st.write("Base Score", base_score)
        st.write("Duplicate Letters (*)", dup_score)
        st.write("End S (*):", s_score)
        st.write("Vowels (+):", vowel_score)
        st.write("Word Rank (+):", rank, "Rank Score:", rank_score)
        st.write("Final Score:", score)
        return score

    return sorted(words, key=word_score, reverse=True)