from tools.prompts import prompts
from pathlib import Path
from tools.anthropic_helper import anthropic_helper

class summary:
    def __init__(self, prompt_location: str, book_text_location: str):
        self.prompts = prompts(prompt_location, book_text_location)
        self.book_text_location = book_text_location

    def summarize_section(self, section: int):
        summarize_query = self.prompts.assemble_summarize(section)

        summarize_output = anthropic_helper.process(summarize_query)

        summary_file_path = Path(self.prompts.book_text_location) / f"section_{section}" / f"summary_{section}.txt"

        with open(summary_file_path, "w", encoding="utf-8") as f:
            f.write(summarize_output)