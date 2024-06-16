import streamlit as st


def main():
    st.title("Instructions")
    st.markdown("""
                This is a basic wordle solver.  The ideas is you can use it as a companion to the game.  First in the game, enter your desired word and submit it.  Once you have the colord boxes back from Wordle, enter your word and select the radio buttons under the row and press the submit button. At the bottom of the page you will be presented with an ordered and ranked list of choices the fit the critieria.  You can simply chose the top item or you can pick anything from the list.
                
                **The following criteria are applied:**
                1. A base score is calculated by summing up the frequencies that the letters appear in the target word set (~12k words).  More commonly occuring letters such as S, E, and A will be given a higher weight and in turn the word a higher score.
                2. A penalty is applied to any word where any single letter repeats, wether adjacent or not.
                3. Words that end in S are penalized since Wordle doesn't allow plurals.
                4. Words with more unique available vowels will get a bonus applied for how many they have.
                5. Finally, the words are looked up to and referrenced to how often they appear in the english language and given a weighting to prioritize more common words.
                """)


if __name__ == "__main__":
    main()
