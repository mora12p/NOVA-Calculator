
import streamlit as st
import html
from calculator import NovaCalculator

# ================= CONFIG =================

st.set_page_config(
    page_title="NOVA | Scientific Calculator",
    page_icon="🪐",
    layout="wide"
)

calc = NovaCalculator()

# ================= SESSION STATE =================

defaults = {
    "expression": "",
    "result": "",
    "history": [],
    "angle_mode": "DEG"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ================= CSS =================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #080607;
    --surface: #140d10;
    --primary: #ff3b20;
    --secondary: #ff8a00;
    --text: #fff4f1;
    --muted: #a99ba0;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 30%, rgba(255,45,15,.13), transparent 40%),
        radial-gradient(ellipse at 90% 85%, rgba(255,100,0,.10), transparent 35%),
        #080607;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
}

.nova-logo {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 8px;
    background: linear-gradient(90deg, #ff321c, #ff9a00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nova-subtitle {
    color: #a99ba0;
    font-size: 11px;
    letter-spacing: 5px;
    margin-bottom: 35px;
}

.display {
    background: linear-gradient(145deg, #211116, #0e090c);
    border: 1px solid rgba(255,75,35,.55);
    border-radius: 22px;
    padding: 30px;
    min-height: 155px;
    margin: 15px 0 25px;
    box-shadow: 0 0 30px rgba(255,45,15,.12);
}

.display-label {
    color: #a99ba0;
    font-size: 11px;
    letter-spacing: 3px;
}

.display-expression {
    color: #d8c6cc;
    font-size: 25px;
    text-align: right;
    overflow-wrap: anywhere;
    margin-top: 15px;
}

.display-result {
    color: #ff8a00;
    font-size: 42px;
    font-weight: 800;
    text-align: right;
    text-shadow: 0 0 20px rgba(255,100,0,.5);
    overflow-wrap: anywhere;
}

.stButton button {
    background: linear-gradient(145deg, #211419, #120c10);
    color: white;
    border: 1px solid rgba(255,75,35,.3);
    border-radius: 15px;
    min-height: 62px;
    font-size: 19px;
    font-weight: 600;
    transition: all .2s ease;
}

.stButton button:hover {
    background: linear-gradient(135deg, #ff421e, #ff8500);
    color: white;
    border-color: #ff9a50;
    box-shadow: 0 0 22px rgba(255,65,20,.35);
    transform: translateY(-2px);
}

.stButton button:active {
    transform: scale(.97);
}

div[data-testid="stTextInput"] input {
    background: #170e12;
    color: white;
    border: 1px solid rgba(255,75,35,.3);
    border-radius: 13px;
}

div[data-testid="stSegmentedControl"] {
    background: #170e12;
    border-radius: 12px;
}

.history-heading {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 5px;
}

.history-heading span {
    color: #ff8a00;
    margin-right: 8px;
}

.history-item {
    background: linear-gradient(145deg, #211419, #130d10);
    border: 1px solid rgba(255,75,35,.2);
    border-radius: 15px;
    padding: 15px;
    margin: 12px 0;
    overflow-wrap: anywhere;
}

.history-expression {
    color: #d8c6cc;
    font-size: 14px;
}

.history-result {
    color: #ff8a00;
    font-size: 19px;
    font-weight: 700;
    margin-top: 8px;
}

.nova-footer {
    color: #78676d;
    text-align: center;
    font-size: 11px;
    letter-spacing: 2px;
    padding: 30px;
}

hr {
    border-color: rgba(255,75,35,.2);
}

</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================

def add_value(value):
    st.session_state.expression += value
    st.session_state.result = ""

def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""

def delete_last():
    st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.result = ""

def calculate():
    expression = st.session_state.expression

    if not expression.strip():
        return

    try:
        result = calc.calculate(
            expression,
            st.session_state.angle_mode
        )

        result_text = str(result)

        st.session_state.result = result_text

        st.session_state.history.append({
            "expression": expression,
            "result": result_text
        })

        st.session_state.expression = result_text

    except (ValueError, TypeError, ArithmeticError):
        st.session_state.result = "Error"

def reuse_expression(expression):
    st.session_state.expression = expression
    st.session_state.result = ""

# ================= HEADER =================

st.markdown("""
<div class="nova-logo">NOVA</div>
<div class="nova-subtitle">
SCIENTIFIC CALCULATOR
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT =================

calculator_col, history_col = st.columns(
    [3, 1.15],
    gap="large"
)

# ================= CALCULATOR =================

with calculator_col:

    top_left, top_right = st.columns([2, 1])

    with top_left:
        st.markdown("### Calculator")

    with top_right:
        st.segmented_control(
            "Angle Mode",
            options=["DEG", "RAD"],
            key="angle_mode",
            label_visibility="collapsed"
        )

    expression_display = html.escape(
        st.session_state.expression or "0"
    )

    result_display = html.escape(
        st.session_state.result
    )

    st.markdown(f"""
    <div class="display">
        <div class="display-label">NOVA DISPLAY</div>
        <div class="display-expression">
            {expression_display}
        </div>
        <div class="display-result">
            {result_display}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SCIENTIFIC BUTTONS

    scientific_buttons = [
        ["sin(", "cos(", "tan(", "sqrt(", "log("],
        ["ln(", "exp(", "abs(", "pi", "e"]
    ]

    for row_index, row in enumerate(scientific_buttons):
        cols = st.columns(5)

        for col, value in zip(cols, row):
            with col:
                st.button(
                    value,
                    key=f"sci_{row_index}_{value}",
                    use_container_width=True,
                    on_click=add_value,
                    args=(value,)
                )

    st.divider()

    # MAIN KEYPAD

    buttons = [
        ["AC", "DEL", "(", ")", "÷"],
        ["7", "8", "9", "^", "×"],
        ["4", "5", "6", "%", "-"],
        ["1", "2", "3", ".", "+"],
        ["0", "00", "pi", "e", "="]
    ]

    for row_index, row in enumerate(buttons):

        cols = st.columns(5)

        for col, value in zip(cols, row):

            with col:

                if value == "AC":
                    st.button(
                        value,
                        key=f"key_{row_index}_{value}",
                        use_container_width=True,
                        on_click=clear_all
                    )

                elif value == "DEL":
                    st.button(
                        value,
                        key=f"key_{row_index}_{value}",
                        use_container_width=True,
                        on_click=delete_last
                    )

                elif value == "=":
                    st.button(
                        value,
                        key=f"key_{row_index}_{value}",
                        use_container_width=True,
                        on_click=calculate,
                        type="primary"
                    )

                else:
                    actual_value = {
                        "÷": "/",
                        "×": "*"
                    }.get(value, value)

                    st.button(
                        value,
                        key=f"key_{row_index}_{value}",
                        use_container_width=True,
                        on_click=add_value,
                        args=(actual_value,)
                    )

# ================= HISTORY =================

with history_col:

    st.markdown("""
    <div class="history-heading">
        <span>◷</span> History
    </div>
    """, unsafe_allow_html=True)

    st.caption("Your recent calculations")

    if st.button("Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    if not st.session_state.history:
        st.info("No calculations yet.")

    else:
        for index, item in enumerate(
            reversed(st.session_state.history)
        ):

            safe_expression = html.escape(item["expression"])
            safe_result = html.escape(item["result"])

            st.markdown(f"""
            <div class="history-item">
                <div class="history-expression">
                    {safe_expression}
                </div>
                <div class="history-result">
                    = {safe_result}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.button(
                "Reuse calculation",
                key=f"reuse_{index}",
                use_container_width=True,
                on_click=reuse_expression,
                args=(item["expression"],)
            )

# ================= FOOTER =================

st.markdown("""
<div class="nova-footer">
    NOVA SCIENTIFIC CALCULATOR · VERSION 1.0
    <br>
    BUILT WITH PYTHON
</div>
""", unsafe_allow_html=True)