import streamlit as st
from google import genai
from google.genai import types  # <--- THIS WAS THE MISSING PIECE

# 1. Page Config
st.set_page_config(page_title="Fair-Work Legal Navigator 2026", layout="wide")

# 2. Initialize the New 2026 Client
# Make sure your GitHub secrets or Streamlit Cloud secrets have "GEMINI_API_KEY"
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing or invalid. Check your Streamlit Secrets.")

# 3. Modern Analysis Function
def run_legal_audit(contract_text, model_name):
    # Constructing a 2026-optimized system prompt
    sys_prompt = f"""
    You are a senior legal auditor specializing in the 2025/2026 Indian Labour Codes.
    Analyze the text below and categorize findings as:
    🔴 CRITICAL: Direct violation of the law.
    🟡 WARNING: Ambiguous or high-risk language.
    🟢 COMPLIANT: Follows current regulations.
    
    Contract Text: {contract_text}
    """
    
    # Using the new stateless generate_content method
    response = client.models.generate_content(
        model=model_name,
        contents=sys_prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,  # Keep it precise for legal work
        )
    )
    return response.text

# 4. Streamlit UI
def main():
    st.title("⚖️ Fair-Work Legal Navigator")
    st.info("Updated for the 2026 Unified Google GenAI SDK.")

    with st.sidebar:
        # March 2026 Stable Models
        model_choice = st.selectbox("Select Intelligence Level", 
                                    ["gemini-2.0-flash-lite", "gemini-2.0-flash"])
        st.write("---")
        st.caption("Ensures compliance with current Indian Labour Codes.")

    contract_input = st.text_area("Paste Contract Clauses Here:", height=250)

    if st.button("Run Compliance Audit"):
        if not contract_input.strip():
            st.error("Please paste some text first to avoid an API error!")
            return

        with st.spinner(f"Auditing via {model_choice}..."):
            try:
                result = run_legal_audit(contract_input, model_choice)
                st.subheader("Audit Results")
                st.markdown(result)
                
                # Add a download button for the audit report
                st.download_button(
                    label="Download Audit Report",
                    data=result,
                    file_name="legal_audit_report.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Audit failed. Error: {e}")

if __name__ == "__main__":
    main()
