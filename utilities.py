# Function to get the rank of a word
from collections import Counter
import streamlit as st
from wordfreq import top_n_list


# Function to read words from a file
@st.cache_data
def read_words(file_path):
    with open(file_path, "r") as file:
        return [line.strip().lower() for line in file if len(line.strip()) == 5]


# Get the top 100,000 words in English
top_words = top_n_list("en", 100000)


def get_word_rank(word):
    try:
        return top_words.index(word) + 1
    except ValueError:
        return None  # Word not found in the top list


# Function to filter words based on specific criteria, exclusion list, and exclude positions for certain letters
def filter_words(words, criteria, exclude_letters, exclude_positions_for_letters):
    exclude_letters_set = set(exclude_letters)

    print("Initial word count:", len(words))
    print("Criteria (Green):", criteria)
    print("Exclude Letters (Grey):", exclude_letters_set)
    print("Exclude Positions for Letters (Yellow):", exclude_positions_for_letters)

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

    print("Words after applying green letter criteria:", len(green_filtered_words))
    print("Words:", green_filtered_words[:10])  # Print first 10 for brevity

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

    print("Words after applying yellow letter criteria:", len(yellow_filtered_words))
    print("Words:", yellow_filtered_words[:10])  # Print first 10 for brevity

    # Exclude words containing grey letters, but account for yellow/green instances
    final_filtered_words = []
    for word in yellow_filtered_words:
        match = True
        for i, char in enumerate(word):
            # Skip this position if it's a green letter
            if i in criteria and criteria[i] == char:
                continue
                
            # Skip this position if it's a yellow letter position
            if char in exclude_positions_for_letters:
                # Count how many times this letter appears in yellow positions
                yellow_count = len(exclude_positions_for_letters[char])
                # Count how many times this letter appears in the word
                word_char_count = word.count(char)
                # Count how many times this letter appears in green positions
                green_count = sum(1 for pos, c in criteria.items() if c == char)
                
                # If we have the right number of this letter (yellow + green instances),
                # then this position is okay even if the letter is in exclude_letters
                if word_char_count <= (yellow_count + green_count):
                    continue
            
            # If we get here and the character is in exclude_letters,
            # then this is an extra occurrence that should be excluded
            if char in exclude_letters_set:
                match = False
                print(f"Excluding {word} due to grey letter '{char}' at position {i}")
                break
                
        if match:
            final_filtered_words.append(word)

    print("Words after applying grey letter criteria:", len(final_filtered_words))
    print("Final words:", final_filtered_words)

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
        base_score = sum(
            frequencies[char]
            for i, char in enumerate(word)
            if i not in exclude_positions
        )

        # Calculate the number of duplicate letters and apply a heavier penalty
        dup_score = 1
        duplicate_count = len(word) - len(set(word))
        if duplicate_count > 0:
            dup_score = 0.5

        # Penalize words ending with 's'
        s_score = 1
        if word[-1] == "s":
            s_score = 0.1

        # Bonus for diverse vowels
        vowel_score = 0
        vowels = set("aeiou")
        unique_vowels = set(word) & vowels
        vowel_score += len(unique_vowels) * 1000

        # Add rank-based adjustment
        rank_score = 0
        rank = get_word_rank(word)
        if rank:
            rank_bonus = 100000 / rank  # Higher rank means more common, higher score
            rank_score = int(rank_bonus * 10)
        else:
            rank_score = -5000  # Penalty if the word is not in the top 100,000 list

        score = base_score * dup_score * s_score + vowel_score + rank_score

        # st.write(f"**{word}**")
        # st.write("Base Score", base_score)
        # st.write("Duplicate Letters (*)", dup_score)
        # st.write("End S (*):", s_score)
        # st.write("Vowels (+):", vowel_score)
        # st.write("Word Rank (+):", rank, "Rank Score:", rank_score)
        # st.write("Final Score:", score)
        return score

    return sorted(words, key=word_score, reverse=True)
