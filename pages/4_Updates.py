import streamlit as st


def main():
    st.title("Updates")
    
    st.markdown("""
    | Date | Description |
    |------|-------------|
    | 2024-12-05 | Fixed a defect in the solver code that would would treat double letters wrong when one was marked as yellow and the other was marked as grey.  It would then prevent any instances of that yellow letter from occcuring. |
    """)

if __name__ == "__main__":
    main()
