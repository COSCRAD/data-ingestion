import unittest

from docx import Document


from data_ingestion.text_document import TextDocument

class TextDocumentTest(unittest.TestCase):
    def build_test_document():
        doc_name = "my document"
        paragraphs = [
            # "[AP]: this is what was said _00:00:05_ and then this _00:00:07_ and finally _00:00:09_"
             "[AP]: this is what was said _00:00:05_"
        ]
        docx_doc = Document()

        # here we build the test document
        for p in paragraphs:
            docx_doc.add_paragraph(p)


        test_filename = "test_docx_import.docx"

        docx_doc.save(test_filename)

        return TextDocument.from_docx(file_path = test_filename, name = doc_name)

    def test_that_it_builds_from_a_word_document(self):
        doc_name = "my document"
        paragraphs = [
            "[AP]: this is what was said _00:00:05_ and then this _00:01:23_"
        ]
        docx_doc = Document()

        # here we build the test document
        for p in paragraphs:
            docx_doc.add_paragraph(p)


        test_filename = "test_docx_import.docx"

        docx_doc.save(test_filename)

        doc = TextDocument.from_docx(file_path = test_filename, name = doc_name)

        self.assertEqual(doc_name, doc.name)


        for index, docx_paragraph in enumerate(docx_doc.paragraphs):
            self.assertEqual(docx_paragraph.text, doc.paragraphs[index].text)

    def test_that_it_builds_audio_labels_with_timestamp_at_end(self):
        test_doc = TextDocumentTest.build_test_document()

        labels = test_doc.emit_audio_labels()

        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0].text,'[AP]: this is what was said ')
        self.assertEqual(labels[1].text,' and then this ')