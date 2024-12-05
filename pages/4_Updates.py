import streamlit as st


def main():
    st.title("Updates")
    
    st.markdown("""
    | Date | Description |
    |-------------|-------------|
    | 2024-12-05 | Fixed a defect in the solver code that would would treat double letters wrong when one was marked as yellow and the other was marked as grey.  It would then prevent any instances of that yellow letter from occcuring. |
    | 2024-11-27| Updated to latest word list from NY Times. |
    | 2024-08-27| Reduced the uplift for common words - this should fix the double letter words taking priority |
    | 2024-08-18 | Added a display of how many remaining words there are in the dictionary |
    | 2024-06-20 | Fixed a defect in the solver code that would would treat double letters wrong when one was marked as green and the other was marked as grey.  The green choice was invalidated. |
    | 2024-06-16 | Initial release! |
    """)

if __name__ == "__main__":
    main()
