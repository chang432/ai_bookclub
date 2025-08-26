from pathlib import Path
import os
from tools.prompts import prompts
from tools.anthropic_helper import anthropic_helper
from tools.summary import summary
import json


class discussion:
    def __init__(self, base_path, book_title):
        self.base_path = Path(base_path)
        self.prompt_path = self.base_path / "prompts.json"
        self.book_text_dir = self.base_path / "books" / book_title / f"{book_title}_text"
        self.post_dir = self.base_path / "posts"

        self.prompts = prompts(self.prompt_path, self.book_text_dir)
        self.summary = summary(self.prompt_path, self.book_text_dir)


    def process_character(self, name: str, section: int):
        print(f"Processing discussion for character: {name} in section {section}...")
        final_query = self.prompts.assemble_discuss(name, section)
        # Here you would call the anthropic_helper.process method with final_query
        discuss_output = anthropic_helper.process(final_query)

        output_obj = {
            "author": name,
            "post": discuss_output,
        }

        post_file_path = Path(self.post_dir) / f"section_{section}" / f"post_{section}.json"

        print(f"Storing post in {post_file_path}...")

        if post_file_path.exists():
            with open(post_file_path, "r") as f:
                data = json.load(f)
        else:
            data = []
        
        data.append(output_obj)

        with open(post_file_path, "w") as f:
            json.dump(data, f, indent=4)


    def process_section(self, section: int):
        print(f"Processing section {section}!")
        os.makedirs(self.post_dir / f"section_{section}", exist_ok=True)

        if section > 1 and not (self.book_text_dir / f"section_{section-1}" / f"summary_{section-1}.txt").exists():
            print("Creating summary from previous section for context...")
            self.summary.summarize_section(section - 1)

        print("Initiating discussion processing for all characters...")
        for character in self.prompts.content['characters']:
            print(f"Generating {character['name']}'s discussion post..")
            self.process_character(character['name'], section)

        # if os.path.exists("")
        # with open(external_dir + "/posts")