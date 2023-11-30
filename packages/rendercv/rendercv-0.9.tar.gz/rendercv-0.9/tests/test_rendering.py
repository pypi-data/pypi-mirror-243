import unittest
import os
from datetime import date
import shutil

from rendercv import rendering, data_model


class TestRendering(unittest.TestCase):
    def test_markdown_to_latex(self):
        input = "[link](www.example.com)"
        expected = r"\href{www.example.com}{link}"
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="only one link"):
            self.assertEqual(output, expected)

        input = "[link](www.example.com) and [link2](www.example2.com)"
        expected = (
            r"\href{www.example.com}{link} and" r" \href{www.example2.com}{link2}"
        )
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="two links"):
            self.assertEqual(output, expected)

        input = "[**link**](www.example.com)"
        expected = r"\href{www.example.com}{\textbf{link}}"
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="bold link"):
            self.assertEqual(output, expected)

        input = "[*link*](www.example.com)"
        expected = r"\href{www.example.com}{\textit{link}}"
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="italic link"):
            self.assertEqual(output, expected)

        input = "[*link*](www.example.com) and [**link2**](www.example2.com)"
        expected = (
            r"\href{www.example.com}{\textit{link}} and"
            r" \href{www.example2.com}{\textbf{link2}}"
        )
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="italic and bold links"):
            self.assertEqual(output, expected)

        input = "**bold**, *italic*, and [link](www.example.com)"
        expected = (
            r"\textbf{bold}, \textit{italic}, and" r" \href{www.example.com}{link}"
        )
        output = rendering.markdown_to_latex(input)
        with self.subTest(msg="bold, italic, and link"):
            self.assertEqual(output, expected)

        # invalid input:
        input = 20
        with self.subTest(msg="float input"):
            with self.assertRaises(ValueError):
                rendering.markdown_to_latex(input)  # type: ignore

    def test_markdown_link_to_url(self):
        input = "[link](www.example.com)"
        expected = "www.example.com"
        output = rendering.markdown_link_to_url(input)
        with self.subTest(msg="only one link"):
            self.assertEqual(output, expected)

        input = "[**link**](www.example.com)"
        expected = "www.example.com"
        output = rendering.markdown_link_to_url(input)
        with self.subTest(msg="bold link"):
            self.assertEqual(output, expected)

        input = "[*link*](www.example.com)"
        expected = "www.example.com"
        output = rendering.markdown_link_to_url(input)
        with self.subTest(msg="italic link"):
            self.assertEqual(output, expected)

        # invalid input:
        input = 20
        with self.subTest(msg="float input"):
            with self.assertRaises(ValueError):
                rendering.markdown_link_to_url(input)  # type: ignore

        input = "not a markdown link"
        with self.subTest(msg="invalid input"):
            with self.assertRaises(ValueError):
                rendering.markdown_link_to_url(input)

        input = "[]()"
        with self.subTest(msg="empty link"):
            with self.assertRaises(ValueError):
                rendering.markdown_link_to_url(input)

    def test_make_it_something(self):
        # invalid input:
        input = "test"
        keyword = "invalid keyword"
        with self.subTest(msg="invalid keyword"):
            with self.assertRaises(ValueError):
                rendering.make_it_something(input, keyword)

    def test_make_it_bold(self):
        input = "some text"
        expected = r"\textbf{some text}"
        output = rendering.make_it_bold(input)
        with self.subTest(msg="without match_str input"):
            self.assertEqual(output, expected)

        match_str = "text"
        expected = r"some \textbf{text}"
        output = rendering.make_it_bold(input, match_str)
        with self.subTest(msg="with match_str input"):
            self.assertEqual(output, expected)

        match_str = 2423
        with self.subTest(msg="invalid match_str input"):
            with self.assertRaises(ValueError):
                rendering.make_it_bold(input, match_str)  # type: ignore

        input = 20
        with self.subTest(msg="float input"):
            with self.assertRaises(ValueError):
                rendering.make_it_bold(input)  # type: ignore

    def test_make_it_underlined(self):
        input = "some text"
        expected = r"\underline{some text}"
        output = rendering.make_it_underlined(input)
        with self.subTest(msg="without match_str input"):
            self.assertEqual(output, expected)

        input = "some text"
        match_str = "text"
        expected = r"some \underline{text}"
        output = rendering.make_it_underlined(input, match_str)
        with self.subTest(msg="with match_str input"):
            self.assertEqual(output, expected)

        input = 20
        with self.subTest(msg="float input"):
            with self.assertRaises(ValueError):
                rendering.make_it_underlined(input)  # type: ignore

    def test_make_it_italic(self):
        input = "some text"
        expected = r"\textit{some text}"
        output = rendering.make_it_italic(input)
        with self.subTest(msg="without match_str input"):
            self.assertEqual(output, expected)

        input = "some text"
        match_str = "text"
        expected = r"some \textit{text}"
        output = rendering.make_it_italic(input, match_str)
        with self.subTest(msg="with match_str input"):
            self.assertEqual(output, expected)

        input = 20
        with self.subTest(msg="float input"):
            with self.assertRaises(ValueError):
                rendering.make_it_italic(input)  # type: ignore

    def test_divide_length_by(self):
        lengths = [
            "10cm",
            "10.24in",
            "10 pt",
            "10.24 mm",
            "10.24    em",
            "1024    ex",
        ]
        divider = 10
        expected = [
            "1.0 cm",
            "1.024 in",
            "1.0 pt",
            "1.024 mm",
            "1.024 em",
            "102.4 ex",
        ]
        for length, exp in zip(lengths, expected):
            with self.subTest(length=length, msg="valid input"):
                self.assertEqual(rendering.divide_length_by(length, divider), exp)

    def test_get_today(self):
        expected = date.today().strftime("%B %d, %Y")
        result = rendering.get_today()
        self.assertEqual(expected, result, msg="Today's date is not correct.")

    def test_get_path_to_font_directory(self):
        font_name = "test"
        expected = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "rendercv",
            "templates",
            "fonts",
            font_name,
        )
        result = rendering.get_path_to_font_directory(font_name)
        self.assertEqual(expected, result, msg="Font directory path is not correct.")

    def test_render_template(self):
        # Read the reference YAML file:
        input_file_path = os.path.join(
            os.path.dirname(__file__),
            "reference_files",
            "John_Doe_CV_yaml_reference.yaml",
        )
        data = data_model.read_input_file(input_file_path)
        output_file_path = rendering.render_template(
            data=data, output_path=os.path.dirname(__file__)
        )

        # Check if the output file exists:
        self.assertTrue(
            os.path.exists(output_file_path), msg="LaTeX file couldn't be generated."
        )

        # Compare the output file with the reference file:
        reference_file_path = os.path.join(
            os.path.dirname(__file__),
            "reference_files",
            "John_Doe_CV_tex_reference.tex",
        )
        with open(output_file_path, "r") as file:
            output = file.read()
        with open(reference_file_path, "r") as file:
            reference = file.read()
            reference = reference.replace("REPLACETHISWITHTODAY", rendering.get_today())

        self.assertEqual(
            output, reference, msg="LaTeX file didn't match the reference."
        )

        # Check if the font directory exists:
        output_folder_path = os.path.dirname(output_file_path)
        font_directory_path = os.path.join(output_folder_path, "fonts")
        self.assertTrue(
            os.path.exists(font_directory_path), msg="Font directory doesn't exist."
        )

        required_files = [
            f"{data.design.font}-Italic.ttf",
            f"{data.design.font}-Regular.ttf",
            f"{data.design.font}-Bold.ttf",
            f"{data.design.font}-BoldItalic.ttf",
        ]
        font_files = os.listdir(font_directory_path)
        for required_file in required_files:
            with self.subTest(required_file=required_file):
                self.assertIn(
                    required_file,
                    font_files,
                    msg=f"Font file ({required_file}) is missing.",
                )

        # Remove the output directory:
        shutil.rmtree(output_folder_path)

    def test_run_latex(self):
        latex_file_path = os.path.join(
            os.path.dirname(__file__),
            "reference_files",
            "John_Doe_CV_tex_reference.tex",
        )

        with self.subTest(msg="Existent file name"):
            pdf_file = rendering.run_latex(latex_file_path)

            # Check if the output file exists:
            self.assertTrue(
                os.path.exists(pdf_file), msg="PDF file couldn't be generated."
            )

            # Compare the pdf file with the reference pdf file:
            reference_pdf_file = pdf_file.replace(
                "_tex_reference.pdf", "_pdf_reference.pdf"
            )
            reference_pdf_file_size = os.path.getsize(reference_pdf_file)
            pdf_file_size = os.path.getsize(pdf_file)

            # Remove the output file:
            os.remove(pdf_file)

            ratio = min(reference_pdf_file_size, pdf_file_size) / max(
                reference_pdf_file_size, pdf_file_size
            )
            self.assertTrue(ratio > 0.98, msg="PDF file didn't match the reference.")

        nonexistent_latex_file_path = os.path.join(
            os.path.dirname(__file__), "reference_files", "nonexistent.tex"
        )

        with self.subTest(msg="Nonexistent file name"):
            with self.assertRaises(
                FileNotFoundError, msg="File not found error didn't raise."
            ):
                rendering.run_latex(nonexistent_latex_file_path)
