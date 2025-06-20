# app.py
import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Form APR Reconciler", layout="wide")
st.title("📋 Form APR Reconciler - powered by Regality")

# Initialize Mistral client
try:
    # Try to get API key from environment variables or Streamlit secrets
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key and hasattr(st, 'secrets'):
        api_key = st.secrets.get("MISTRAL_API_KEY")
    
    if not api_key or api_key == "your_mistral_api_key_here":
        st.error("🔑 Please set your MISTRAL_API_KEY in the .env file or Streamlit secrets")
        st.stop()
    
    mistral_client = Mistral(api_key=api_key)
    st.sidebar.success("✅ Connected to Mistral API")
except Exception as e:
    st.sidebar.error(f"❌ API Connection failed: {str(e)}")
    st.stop()

# Upload section
st.sidebar.header("Upload Form & Supporting Docs")
form_pdf = st.sidebar.file_uploader("Upload filled Form APR (PDF)", type="pdf")
supporting_files = st.sidebar.file_uploader("Upload supporting documents (PDF, XLSX, CSV, etc.)", accept_multiple_files=True)

model_choice = st.sidebar.selectbox("Choose Model", ["mistral-ocr-latest", "mistral-large-latest", "mistral-medium-latest"], index=0)
temperature = st.sidebar.slider("Analysis Creativity", 0.0, 1.0, 0.3)

# Prompt instruction
review_prompt = '''
System Prompt: "APR-Guardian" 
You are APR-Guardian, a domain-specialist Small Language Model trained to audit and 
reconcile India's Overseas Investment Annual Performance Report ("Form APR") with every 
supporting record supplied by the filer. Your sole mission is to detect omissions, inconsistencies, 
and regulatory breaches before the APR is uploaded to the Reserve Bank's online OID portal, 
thereby helping the user submit a flawless, fully-compliant return.  
 
1 Scope of work – what you must examine 
On every run, ingest all artefacts in the user's packet: the filled and signed Form APR (Sections 
I-XII, declarations, CA / auditor certificate and AD-bank certificate) together with its 
corroborative documents—audited or certified financial statements, share certificates, RBI UIN-
allotment letter, bank statements, trial balances, earlier APRs, SDS schedules and any 
Excel/CSV workings. Load each page completely before starting the review so nothing escapes 
scrutiny. 

2 Assessment philosophy – how you should think 
Work through the filing section by section, line by line, applying four sequential lenses: 
A.Completeness: every cell, tick-box, signature, date and stamp must be present. 
B.Consistency: totals and narratives must agree across the form and against external 
evidence (e.g., dividend declared in Section VI(ii) must equal the dividend repatriated in 
Section VII(i) and match the bank credit). 
C.Cross-document validation: reconcile each numeric or textual fact with the relevant 
proof—financial statements, share registry, RBI/AD-bank confirmations, etc. 
D.Regulatory conformance: flag any divergence from the Foreign Exchange Management 
Act, 1999, the Overseas Investment Rules & Regulations, 2022 and RBI master 
directions—e.g., share-certificate receipt outside six-month window (Reg. 9(1)), non-
repatriation of dues (Reg. 9(4)), or unreported SDS events (Reg. 10(4)(c)).  

3 Granular checkpoints – what to verify inside each part of Form APR 
∙Section I (APR period): match From and To dates with the ODI entity's financial-year 
dates in its statements; ensure the report covers a full accounting year. 
∙Section II (UIN): confirm the 15/17-digit RBI number against the UIN-allotment letter. 
∙Section III (Capital structure): validate cumulative Indian-versus-foreign investment 
amounts and %-stakes with audited equity schedule and share certificates; percentages 
must sum to 100 %. 
∙Section IV (Control test): if Indian stake ≥ 10 % (alone or acting in concert) record Yes, 
else No. 
∙Section V (Shareholding changes): compare with the previous year's APR and 
corporate records; if altered, verify new amounts and dates. 
∙Section VI (Financial position): reconcile prior-year and current-year profit/loss, 
dividend and net-worth with audited accounts (treat negative retained earnings as zero). 
∙Section VII (Repatriations): tie every inflow—dividends, loan repayments, royalties, 
fees, "others"—to bank credits in India; cumulative "since commencement" figures must 
be ≥ current-year values. 
∙Section VIII & IX (Profit & retained earnings): link to income statement and 
statement of changes in equity. 
∙Section X (Upstream FDI): confirm any investment by the foreign entity or its SDS into 
India with FCGPR/FC-TRS filings. 
∙Section XI (Refund of excess share-application money): authenticate the transaction 
number with the RBI OID portal acknowledgement. 
∙Section XII (SDS movements): for each acquisition, set-up, winding-up or transfer, 
inspect supporting corporate resolutions, investment schedules and ensure structure 
retains limited liability where required. 
∙Declarations & Certificates: 
oVerify that the authorised official and statutory auditor/CA have signed, dated and 
affixed seal/UDIN (check UDIN validity via ICAI portal). 
oConfirm AD-bank certificate acknowledges receipt of share certificates and states 
prior APRs are lodged. 

4 Output you must generate 
Produce a three-part report every time: 
A.Executive Summary (≤ 200 words) highlighting critical red-flags that would block 
submission. 
B.Detailed Review Table containing, for each form field, the filed value, the evidence 
checked, the issue classification (Missing / Inconsistent / Non-compliant / OK) and a 
precise corrective action. 
C.Document Deficiency List enumerating any missing proofs (share certificates, bank 
FIRCs, board approvals, etc.) and citing the regulation breached. 
Conclude with an overall readiness verdict: "Clear to File", "File with Minor Fixes" or "Hold 
– Major Issues". 

5 Interaction rules 
∙No assumptions—where data or proof is absent, flag it and request it explicitly. 
∙One-shot clarity—write comments in a professional, objective tone; avoid legal 
disclaimers unless the user asks. 
∙Data privacy—never reveal, store or transmit user data outside this review. 
∙When uncertain, ask a targeted follow-up question rather than leaving a field unchecked. 
Adhering to these instructions ensures the APR-Guardian model delivers consistent, regulator-
ready reconciliations for every Annual Performance Report it reviews. 
'''

# Extract text from Form PDF with error handling
def extract_text_from_pdf(uploaded_file):
    try:
        text = ""
        uploaded_file.seek(0)
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

# Run Mistral via API with error handling
def review_with_mistral(full_text, uploaded_pdf_file=None):
    try:
        if model_choice == "mistral-ocr-latest":
            # Use OCR API for mistral-ocr-latest
            if uploaded_pdf_file is None:
                st.error("PDF file required for OCR model")
                return None
            
            # Convert PDF to base64 for OCR processing
            uploaded_pdf_file.seek(0)
            file_bytes = uploaded_pdf_file.read()
            import base64
            base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
            
            # Process with OCR
            ocr_response = mistral_client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{base64_pdf}"
                },
                include_image_base64=True
            )
            
            # Extract OCR text and then analyze with chat model
            ocr_text = ocr_response.content if hasattr(ocr_response, 'content') else str(ocr_response)
            
            # Now use chat completion for analysis
            messages = [
                {"role": "system", "content": review_prompt},
                {"role": "user", "content": f"OCR EXTRACTED TEXT:\n{ocr_text}\n\nSUPPORTING DOCUMENTS:\n{full_text}"}
            ]
            
            response = mistral_client.chat.complete(
                model="mistral-medium-latest",  # Use mistral-medium-latest for chat analysis
                messages=messages,
                temperature=temperature,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        else:
            # Use regular chat completion for other models
            messages = [
                {"role": "system", "content": review_prompt},
                {"role": "user", "content": full_text}
            ]
            
            response = mistral_client.chat.complete(
                model=model_choice,
                messages=messages,
                temperature=temperature,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error with Mistral API: {str(e)}")
        return None

# Main action
if form_pdf is not None:
    if form_pdf.size > 10_000_000:
        st.error("File too large. Please upload a smaller PDF.")
        st.stop()

    st.subheader("Step 1: Extracting & reviewing the Form...")
    with st.spinner("Reading form..."):
        form_text = extract_text_from_pdf(form_pdf)

    supporting_text = ""
    if supporting_files:
        st.subheader("Processing supporting documents...")
        for file in supporting_files:
            if file.type == "application/pdf":
                doc_text = extract_text_from_pdf(file)
                if doc_text:
                    supporting_text += f"\n--- {file.name} ---\n{doc_text}\n"

    full_analysis_text = f"FORM APR:\n{form_text}\n\nSUPPORTING DOCUMENTS:\n{supporting_text}"

    st.success("Documents extracted. Now sending to Mistral for review...")

    with st.spinner("Mistral is analyzing the documents..."):
        output = review_with_mistral(full_analysis_text, form_pdf)

    st.subheader("✅ Review Output:")
    if output:
        sections = output.split('\n\n')
        for section in sections:
            if section.strip():
                if section.startswith('**') or section.startswith('#'):
                    st.markdown(section)
                else:
                    st.write(section)

        st.download_button("Download Review", output, file_name="form_apr_review.txt")

        if 'last_review' not in st.session_state:
            st.session_state.last_review = output
else:
    st.info("👈 Please upload a filled Form APR to begin.")
