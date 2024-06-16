import streamlit as st

# Initialize session state to keep track of the current row and radio button states
if 'current_row' not in st.session_state:
    st.session_state.current_row = 0
if 'inputs' not in st.session_state:
    st.session_state.inputs = [["" for _ in range(5)] for _ in range(5)]
if 'radio_states' not in st.session_state:
    st.session_state.radio_states = [["Select" for _ in range(5)] for _ in range(5)]

# Function to render a single input cell
def render_input_cell(row, col):
    key_input = f"input_{row}_{col}"
    st.session_state.inputs[row][col] = st.text_input(f"Input ({row+1},{col+1})", key=key_input)

# Function to render a single radio cell
def render_radio_cell(row, col, key_suffix):
    key_radio = f"radio_{row}_{col}_{key_suffix}"
    color = st.radio("Color", ["Select", "Grey", "Green", "Yellow"], key=key_radio, horizontal=True)
    st.session_state.radio_states[row][col] = color

    # Determine background color based on radio button selection
    color_dict = {"Select": "#FFFFFF", "Grey": "#D3D3D3", "Green": "#90EE90", "Yellow": "#FFFFE0"}
    background_color = color_dict.get(color, "#FFFFFF")
    
    # Style the input box based on the selected color
    st.markdown(
        f"""
        <style>
        div[data-testid="stTextInput"] input[data-baseweb="input"] {{
            background-color: {background_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to handle the submission
def submit_row():
    current_row = st.session_state.current_row
    if "Select" not in st.session_state.radio_states[current_row]:
        if st.session_state.current_row < 4:
            st.session_state.current_row += 1
        print(f"Row {current_row} submitted, moving to row {st.session_state.current_row}")
    else:
        st.warning("Please fill in all color selections for the current row before submitting the next row.")

def main():
    st.title("5x5 Grid with Input Boxes and Color Marking")

    # Create a 5x5 grid for input boxes and radio buttons
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            with cols[col]:
                # Render input boxes for the current row
                if row == st.session_state.current_row:
                    render_input_cell(row, col)
                # Render radio buttons for the previous rows
                elif row < st.session_state.current_row:
                    render_radio_cell(row, col, "grid")

    # Submit button to move to the next row
    if st.session_state.current_row < 5:
        if st.session_state.current_row == 0 or (st.session_state.current_row > 0 and "Select" not in st.session_state.radio_states[st.session_state.current_row - 1]):
            if st.button("Submit Row"):
                st.session_state.current_row += 1

    # Render radio buttons below the input boxes after submission
    if st.session_state.current_row > 0:
        st.markdown("## Color Selections")
        for row in range(st.session_state.current_row):
            cols = st.columns(5)
            for col in range(5):
                with cols[col]:
                    render_radio_cell(row, col, "below")

if __name__ == "__main__":
    main()