import re
from collections import Counter

import streamlit as st


_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "he",
    "her",
    "hers",
    "him",
    "his",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "me",
    "my",
    "not",
    "of",
    "on",
    "or",
    "our",
    "she",
    "so",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "us",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "will",
    "with",
    "you",
    "your",
}


def _split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    # Lightweight sentence segmentation: good enough for a basic demo app.
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Za-z0-9']+", text)]


def summarize(text: str, max_sentences: int = 3) -> str:
    sentences = _split_sentences(text)
    if len(sentences) <= max_sentences:
        return " ".join(sentences).strip()

    words = [w for w in _tokenize(text) if w not in _STOPWORDS and len(w) > 2]
    if not words:
        return " ".join(sentences[:max_sentences]).strip()

    freq = Counter(words)

    scored: list[tuple[float, int, str]] = []
    for idx, s in enumerate(sentences):
        s_words = [w for w in _tokenize(s) if w not in _STOPWORDS and len(w) > 2]
        if not s_words:
            score = 0.0
        else:
            # Normalize by sentence length so long sentences don't dominate.
            score = sum(freq.get(w, 0) for w in s_words) / (len(s_words) ** 0.8)
        scored.append((score, idx, s))

    top = sorted(scored, key=lambda t: (t[0], -t[1]), reverse=True)[:max_sentences]
    top_sorted_by_original_order = [t[2] for t in sorted(top, key=lambda t: t[1])]
    return " ".join(top_sorted_by_original_order).strip()


st.set_page_config(page_title="Summarizer", page_icon="📝", layout="centered")

st.markdown(
    """
<style>
  /* Page spacing */
  .block-container { padding-top: 2.25rem; padding-bottom: 2.5rem; max-width: 980px; }

  /* Make widgets feel “SaaS” */
  div[data-testid="stTextArea"] textarea {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    background: rgba(255,255,255,0.03) !important;
    padding: 14px 14px !important;
    font-size: 0.98rem !important;
    line-height: 1.45 !important;
  }
  div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(124,58,237,0.70) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
  }

  /* Primary button */
  div.stButton > button {
    width: 100%;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    background: linear-gradient(135deg, rgba(124,58,237,1) 0%, rgba(99,102,241,1) 100%) !important;
    color: white !important;
    font-weight: 650 !important;
    letter-spacing: 0.2px;
    box-shadow: 0 10px 25px rgba(124,58,237,0.18);
  }
  div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(124,58,237,0.24);
  }

  /* “Card” containers (Streamlit alerts/containers are a bit plain by default) */
  .saas-card {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    padding: 18px 18px 6px 18px;
  }
  .muted { opacity: 0.8; }
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 📝 Summarizer")
    st.markdown(
        """
<div class="muted">
Turn long text into a short, readable summary in seconds.
</div>
""",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        """
- Paste text in the box
- Click **Summarize**
- Copy the result
"""
    )
    st.markdown("### Tips")
    st.markdown(
        """
- Works best with 2+ paragraphs
- Include headings if you have them
- If the text is short, the summary will be the original text
"""
    )

    example = (
        "Project update: We shipped the new onboarding flow last week. "
        "Activation improved, but drop-off is still highest on the billing step. "
        "Next, we’ll simplify the pricing page and add monthly/annual toggle defaults. "
        "Support also reported confusion about seat limits, so we’ll clarify that copy. "
        "Finally, we’ll run an A/B test for the new checkout before rolling out to all users."
    )
    if st.button("Paste an example", use_container_width=True):
        st.session_state["input_text"] = example

st.markdown("### Professional text summarization")
st.markdown(
    "<div class='muted'>Paste your text below and get a concise 3-sentence summary.</div>",
    unsafe_allow_html=True,
)
st.write("")

st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
text = st.text_area(
    "Your text",
    key="input_text",
    height=220,
    label_visibility="collapsed",
    placeholder="Paste an article, notes, meeting transcript, or any long text…",
)
col_a, col_b = st.columns([2, 1])
with col_a:
    summarize_clicked = st.button("Summarize", type="primary")
with col_b:
    st.markdown(
        f"<div class='muted' style='text-align:right; padding-top: 10px;'>"
        f"{len(text.strip()):,} chars</div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

if summarize_clicked:
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize(text, max_sentences=3)

        st.write("")
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("### Summary")
        st.write(summary)
        st.markdown("</div>", unsafe_allow_html=True)
