from pathlib import Path
import os
from prompts import prompts
import anthropic_helper
import json

class discussion:
    def __init__(self, prompt_location, book_text_dir, post_dir):
        self.prompt_location = prompt_location
        self.book_text_dir = book_text_dir
        self.post_dir = post_dir
        self.prompts = prompts(self.prompt_location, self.book_text_dir)


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
        print(f"Processing section {section} discussions for all characters...")
        section_dir = self.post_dir+"/section_"+str(section)

        if not os.path.exists(section_dir):
            os.mkdir(section_dir)
        
        for character in self.prompts.content['characters']:
            print(character["name"])

        self.process_character("John", section)

        # if os.path.exists("")
        # with open(external_dir + "/posts")