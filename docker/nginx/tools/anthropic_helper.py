import anthropic

# MODEL = "claude-3-5-haiku-latest"
MODEL = "claude-sonnet-4-20250514"

client = anthropic.Anthropic()

class anthropic_helper:
    @staticmethod
    def process(msg) -> str:
        """
        Inputs -> message to process
        Outputs -> dictionary with output string, input token count, and output token count
        """

        output = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": msg
                }
            ]
        )
        output_dict = output.to_dict()

        print("Input tokens used:", output_dict["usage"]["input_tokens"])
        print("Output tokens used:", output_dict["usage"]["output_tokens"])

        return str(output_dict["content"][0]["text"]).strip()