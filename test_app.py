import unittest
import os
from app import extract_text_from_pdf, summarize_text, generate_mind_map
from create_test_pdf import create_test_pdf

class TestApp(unittest.TestCase):

    def setUp(self):
        self.pdf_path = "test.pdf"
        self.test_content = "This is some introductory text. The main point is that summarization is important. This is some concluding text."
        create_test_pdf(self.pdf_path, self.test_content)

    def tearDown(self):
        os.remove(self.pdf_path)

    def test_extract_text_from_pdf(self):
        extracted_text = extract_text_from_pdf(self.pdf_path)
        self.assertIn("This is some introductory text", extracted_text)

    def test_summarize_text(self):
        summary = summarize_text(self.test_content, num_sentences=1)
        self.assertEqual(summary, "The main point is that summarization is important.")

    def test_generate_mind_map(self):
        mind_map = generate_mind_map("This is the main topic. This is a sub-topic.")
        self.assertIn("# This is the main topic.", mind_map)
        self.assertIn("- This is a sub-topic.", mind_map)

    def test_summarize_arabic_text(self):
        arabic_text = "هذا نص تجريبي باللغة العربية. الهدف من هذا النص هو اختبار وظيفة التلخيص. الجملة الثالثة هنا."
        summary = summarize_text(arabic_text, language='arabic', num_sentences=1)
        self.assertEqual(summary, "الهدف من هذا النص هو اختبار وظيفة التلخيص.")

    def test_summarize_french_text(self):
        french_text = "Ceci est un texte de test en français. Le but de ce texte est de tester la fonction de résumé. La troisième phrase est ici."
        summary = summarize_text(french_text, language='french', num_sentences=1)
        self.assertEqual(summary, "Le but de ce texte est de tester la fonction de résumé.")

if __name__ == "__main__":
    unittest.main()
