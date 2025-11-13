import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process as aksharamukha_process
from gtts import gTTS
from io import BytesIO
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Punjabi (Gurmukhi) → Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ AUDIO GENERATOR ------------------ #
def make_audio(text, lang="kn"):
    fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ------------------ PAGE TITLE ------------------ #
st.title("📝 Learn Kannada using Punjabi (Gurmukhi) Script")
st.subheader("ਪੰਜਾਬੀ (ਗੁਰਮੁਖੀ) ਲਿਪੀ ਨਾਲ ਕਨੜ ਸਿੱਖੋ")

text = st.text_area("Enter Punjabi (Gurmukhi) text here:", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # ---------------- FULL SENTENCE PROCESSING ---------------- #

            # Punjabi → Kannada sentence translation
            kannada = GoogleTranslator(source="pa", target="kn").translate(text)

            # Kannada → Gurmukhi script
            kannada_in_gurmukhi = aksharamukha_process("Kannada", "Gurmukhi", kannada)

            # Kannada → English phonetics
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada audio (sentence)
            audio_sentence = make_audio(kannada)

            # ---------------- OUTPUT ---------------- #
            st.markdown("## 🔹 Translation Results")

            st.markdown(f"**Punjabi Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")
            st.markdown(f"**Kannada in Gurmukhi Script:**  \n:orange[{kannada_in_gurmukhi}]")
            st.markdown(f"**English Phonetics:**  \n`{kannada_english}`")

            st.markdown("### 🔊 Kannada Audio (Sentence)")
            st.audio(audio_sentence, format="audio/mp3")
            st.download_button("Download Sentence Audio", audio_sentence, "sentence.mp3")

            # ---------------- WORD-BY-WORD FLASHCARDS ---------------- #

            st.markdown("---")
            st.markdown("## 🃏 Flashcards (Word-by-Word)")

            punjabi_words = text.split()
            kan_words = kannada.split()

            # Handle mismatch
            limit = min(len(punjabi_words), len(kan_words))

            for i in range(limit):
                pw = punjabi_words[i]
                kw = kan_words[i]

                # Kannada → Gurmukhi script (word)
                kw_gm = aksharamukha_process("Kannada", "Gurmukhi", kw)

                # Phonetics (word)
                kw_ph = transliterate(kw, sanscript.KANNADA, sanscript.ITRANS)

                # Audio (word)
                kw_audio = make_audio(kw)

                with st.expander(f"Word {i+1}: {pw}", expanded=False):
                    st.write("**Punjabi word:**", pw)
                    st.write("**Kannada word:**", kw)
                    st.write("**Kannada in Gurmukhi script:**", kw_gm)
                    st.write("**Phonetics:**", kw_ph)

                    st.audio(kw_audio, format="audio/mp3")
                    st.download_button(
                        f"Download Audio (Word {i+1})",
                        kw_audio,
                        f"word_{i+1}.mp3"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter Punjabi text.")
