
import json
from pathlib import Path

class prompts():
    content = None

    def __init__(self, prompt_location: str, book_text_location: str):
        if not self.content:
            with open(prompt_location, "r") as f:
                self.content = json.load(f)
        self.book_text_location = book_text_location


    def assemble_discuss(self, name: str, section: int) -> str:
        main_section = self.content["discuss"]
        char_info = self.get_char_info(name)
        prev_section_summary = self.get_section_summary(section - 1) if section > 1 else ""
        book_text = f"Input Text:\n{self.combine_section_text(self.book_text_location, section).strip()}"

        query = "\n\n".join([main_section,char_info,prev_section_summary,book_text])
        print("==============================================")
        print(f"{name}'s discussion query:\n" + query)
        print("==============================================")

        return query
    
    
    def assemble_summarize(self, section: int) -> str:
        main_section = self.content["summarize"]

        prev_summary = ""
        prev_summary_file = Path(self.book_text_location) / f"section_{section-1}" / f"summary_{section-1}.txt"
        if prev_summary_file.exists():
            prev_summary = prev_summary_file.read_text(encoding="utf-8").strip()

        book_text = self.combine_section_text(self.book_text_location, section)

        query = "\n\n".join([main_section, prev_summary, book_text])
        print("==============================================")
        print(f"Summary query for section {section}:\n" + query)
        print("==============================================")

        return query
    

    def get_section_summary(self, section: int) -> str:
        """
        Retrieve the summary for a specific section.
        
        Args:
            section (int): The section number to retrieve the summary for.
        
        Returns:
            str: The summary text for the specified section.
        """
        summary_file = Path(self.book_text_location) / f"section_{section}" / f"summary_{section}.txt"
        if not summary_file.exists():
            raise FileNotFoundError(f"Summary file for section {section} does not exist at {summary_file}")

        return f"Summary:\n{summary_file.read_text(encoding="utf-8").strip()}"

    
    def combine_section_text(self, book_text_dir: str, section_number: int) -> str:
        """
        Combine text from all .txt files in a given section into a single string.

        Args:
            section_number (int): The section number to combine.

        Returns:
            str: Concatenated text of all files in the section.
        """
        section_dir = Path(book_text_dir) / f"section_{str(section_number)}"
        if not section_dir.exists():
            raise FileNotFoundError(f"Section {section_number} not found at {section_dir}")

        # Collect all .txt files, sorted by numeric page number
        txt_files = sorted(
            [f for f in section_dir.glob("*.txt") if "summary" not in f.name],
            key=lambda f: int(f.stem)
        )

        combined_text = []
        for txt_file in txt_files:
            try:
                content = txt_file.read_text(encoding="utf-8")
                combined_text.append(content.strip())
            except Exception as e:
                print(f"Warning: could not read {txt_file}: {e}")

        return "\n".join(combined_text).strip()


    def get_char_info(self, name):
        """
        Inputs name, retrieves char info related to the name and returns the info as a comma separated string
        """
        char_info = None
        for char_dict in self.content["characters"]:
            if char_dict["name"] == name:
                char_info = ",".join(char_dict["descriptions"])
        
        if not char_info:
            raise Exception(f"Character named {name} does not exist in the data")

        final_char_query = f"Character:\nName:{name}\n" + char_info
        return final_char_query