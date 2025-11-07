import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    :param pdf_path: The path to the PDF file.
    :return: The extracted text as a single string.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

import argparse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest

def download_nltk_data():
    """Downloads the required NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.DownloadError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except nltk.downloader.DownloadError:
        nltk.download('stopwords')

def summarize_text(text, language='english', num_sentences=5):
    """
    Generates a summary of the text using an extractive summarization algorithm.

    :param text: The text to summarize.
    :param language: The language of the text ('english', 'french', 'arabic').
    :param num_sentences: The number of sentences in the summary.
    :return: The summarized text.
    """
    # For Arabic, we need to use a different tokenizer and avoid lowercasing
    if language == 'arabic':
        sentences = sent_tokenize(text) # Default tokenizer might not be optimal
        words = word_tokenize(text)
    else:
        sentences = sent_tokenize(text, language=language)
        words = word_tokenize(text.lower(), language=language)

    # Ensure language is supported by NLTK's stopwords
    supported_languages = set(stopwords.fileids())
    if language not in supported_languages:
        raise ValueError(f"Language '{language}' is not supported for stopwords.")

    stop_words = set(stopwords.words(language))

    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    if not word_frequencies:
        return ""

    maximum_frequency = max(word_frequencies.values()) if word_frequencies else 0
    if maximum_frequency == 0:
        return ""

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    sentence_scores = {}
    for sent in sentences:
        if language == 'arabic':
            tokenized_sent = word_tokenize(sent)
        else:
            tokenized_sent = word_tokenize(sent.lower(), language=language)

        for word in tokenized_sent:
            if word in word_frequencies.keys():
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def generate_mind_map(summary):
    """
    Formats the summary as a hierarchical Markdown list.

    :param summary: The summarized text.
    :return: A string formatted as a Markdown list.
    """
    sentences = sent_tokenize(summary)
    if not sentences:
        return ""

    # The first sentence is the main topic
    mind_map = f"# {sentences[0]}\n\n"

    # Subsequent sentences are sub-topics
    for sentence in sentences[1:]:
        mind_map += f"- {sentence}\n"

    return mind_map

def main():
    """Main function to run the PDF summarizer."""
    parser = argparse.ArgumentParser(description="Summarize a PDF and generate a mind map.")
    parser.add_argument("pdf_path", help="The path to the PDF file.")
    parser.add_argument("--language", default="english", help="The language of the text (english, french, or arabic).")
    parser.add_argument("--num_sentences", type=int, default=5, help="The number of sentences in the summary.")

    args = parser.parse_args()

    try:
        download_nltk_data()
        text = extract_text_from_pdf(args.pdf_path)
        summary = summarize_text(text, args.language, args.num_sentences)
        mind_map = generate_mind_map(summary)

        print(mind_map)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
