from discussion import discussion
from summary import summary

EXTERNAL_DIR = "../temp_external"
PROMPT_LOCATION = EXTERNAL_DIR + "/prompts.json"
BOOK_TEXT_DIR = EXTERNAL_DIR + "/books/project_hail_mary/project_hail_mary_text"
POST_DIR = EXTERNAL_DIR + "/posts"

# p = prompts(PROMPT_LOCATION, BOOK_TEXT_DIR)
# p.assemble_discuss('John',2)

d = discussion(PROMPT_LOCATION, BOOK_TEXT_DIR, POST_DIR)
d.process_section(3)

# s = summary(PROMPT_LOCATION, BOOK_TEXT_DIR)
# s.summarize_section(3)

# output = anthropic_helper.process("say one word")
