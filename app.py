import streamlit as st
from calculator import calculate_expression

st.set_page_config(page_title="Scientific Calculator", layout="wide")

if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "history" not in st.session_state:
    st.session_state.history = []
st.markdown("""
<style>
.stButton button {
    height: 55px;
    font-size: 18px;
}
.calc-screen {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 10px;
    text-align: right;
    margin-bottom: 15px;
    border: 1px solid #333;
}
.expr-text {
    color: #aaaaaa;
    font-size: 20px;
    min-height: 28px;
}
.res-text {
    color: #ffffff;
    font-size: 34px;
    font-weight: bold;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

def press(val):
    st.session_state.expression += str(val)

def clear():
    st.session_state.expression = ""
    st.session_state.result = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def solve():
    expr = st.session_state.expression
    if not expr:
        return
    res = calculate_expression(expr, angle_mode)
    st.session_state.result = res
    if res != "Error":
        st.session_state.history.append((expr, res))
        st.session_state.expression = res

st.title("Scientific Calculator")

main_col, side_col = st.columns([3, 1.2])

with main_col:
    angle_mode = st.radio("Angle Unit:", ["DEG", "RAD"], horizontal=True)

    current_expr = st.session_state.expression if st.session_state.expression else "0"
    st.markdown(f"""
    <div class="calc-screen">
        <div class="expr-text">{current_expr}</div>
        <div class="res-text">{st.session_state.result}</div>
    </div>
    """, unsafe_allow_html=True)

    sci_rows = [
        ["sin(", "cos(", "tan(", "sqrt(", "log("],
        ["ln(", "exp(", "abs(", "pi", "e"]
    ]

    for r_idx, row in enumerate(sci_rows):
        cols = st.columns(5)
        for idx, label in enumerate(row):
            cols[idx].button(label, key=f"sci_{r_idx}_{idx}", use_container_width=True, on_click=press, args=(label,))

    st.write("---")

    num_rows = [
        ["AC", "DEL", "(", ")", "÷"],
        ["7", "8", "9", "^", "×"],
        ["4", "5", "6", "%", "-"],
        ["1", "2", "3", ".", "+"],
        ["0", "00", "pi", "e", "="]
    ]

    for r_idx, row in enumerate(num_rows):
        cols = st.columns(5)
        for idx, label in enumerate(row):
            btn_key = f"num_{r_idx}_{idx}"
            if label == "AC":
                cols[idx].button(label, key=btn_key, use_container_width=True, on_click=clear)
            elif label == "DEL":
                cols[idx].button(label, key=btn_key, use_container_width=True, on_click=backspace)
            elif label == "=":
                cols[idx].button(label, key=btn_key, use_container_width=True, type="primary", on_click=solve)
            else:
                val = "/" if label == "÷" else ("*" if label == "×" else label)
                cols[idx].button(label, key=btn_key, use_container_width=True, on_click=press, args=(val,))

with side_col:
    st.subheader("History")
    if st.button("Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    if len(st.session_state.history) == 0:
        st.write("No calculations yet.")
    else:
        for i, (old_expr, old_res) in enumerate(reversed(st.session_state.history)):
            st.info(f"{old_expr} = **{old_res}**")
            if st.button("Load", key=f"load_{i}"):
                st.session_state.expression = old_expr
                st.session_state.result = ""
                st.rerun()
