import os
from anthropic import Anthropic, AsyncAnthropic, APIError, APIConnectionError, RateLimitError, APIStatusError
import asyncio
from termcolor import colored
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()

class PromptComposer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.async_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20240620"  # Updated to the latest model version
        self.prompts = {
            'midjourney': self.load_prompt('prompts/midjourney.txt'),
            'udio': self.load_prompt('prompts/udio.txt')
        }

    @staticmethod
    def load_prompt(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    async def generate_completion_async(self, prompt_type, question):
        try:
            response = await self.async_client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=self.prompts[prompt_type],
                messages=[{"role": "user", "content": question}]
            )
            return response.content, response.usage
        except (APIConnectionError, RateLimitError, APIStatusError, APIError) as e:
            print(f"API error: {type(e).__name__} - {str(e)}")
            return None, None

    def generate_completion_stream(self, prompt_type, question):
        try:
            return self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=self.prompts[prompt_type],
                messages=[{"role": "user", "content": question}],
                stream=True
            )
        except (APIConnectionError, RateLimitError, APIStatusError, APIError) as e:
            print(f"API error: {type(e).__name__} - {str(e)}")
            return None

    def parse_output(self, output):
        if isinstance(output, str):
            items = re.findall(r'(\d+)\.\s*(.*?)(?=\n\n\d+\.|\Z)', output, re.DOTALL)
            if items:
                return [{'number': item[0], 'prompt': item[1].strip()} for item in items]
        return [{'number': '1', 'prompt': str(output)}]

    def save_output(self, prompt_type, question, output):
        path = f"outputs/{prompt_type}"
        os.makedirs(path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_question = re.sub(r'[^\w\-_\. ]', '_', question[:30])
        filename = f"{timestamp}_{sanitized_question}.txt"
        with open(os.path.join(path, filename), "w") as file:
            file.write(f"User Input: {question}\n\nOutput:\n{output}")
        return os.path.join(path, filename)

    def run(self):
        while True:
            print(colored("\n=== Prompt Gen ===", "blue", attrs=["bold"]))
            print(colored("Enter 'q' to quit.", "magenta"))
            print(colored("Select prompt type:", "magenta"))
            print(colored("1. Midjourney", "cyan"))
            print(colored("2. Udio", "cyan"))

            prompt_type = input(colored("\nChoice (1/2/q): ", "yellow")).strip().lower()
            
            if prompt_type == 'q':
                print(colored('Exiting... Goodbye!', 'red', attrs=["bold"]))
                break
            
            prompt_type = 'midjourney' if prompt_type == '1' else 'udio' if prompt_type == '2' else None
            if not prompt_type:
                print(colored('Invalid choice. Please try again.', 'red'))
                continue

            question = input(colored(f"\nDescribe the {'image' if prompt_type == 'midjourney' else 'music'} (or 'q' to quit): ", "green")).strip()
            
            if question.lower() == 'q':
                print(colored('Exiting... Goodbye!', 'red', attrs=["bold"]))
                break
            
            if not question:
                print(colored('Please provide a description.', 'red'))
                continue

            print(colored("\nGenerating...", "yellow"))
            stream = self.generate_completion_stream(prompt_type, question)
            if not stream:
                continue

            print(colored("\nGenerated Output:", "cyan", attrs=["bold"]))
            full_output = ""
            for chunk in stream:
                if chunk.type == "content_block_delta":
                    print(chunk.delta.text, end='', flush=True)
                    full_output += chunk.delta.text

            if full_output:
                saved_file = self.save_output(prompt_type, question, full_output)
                print(colored(f"\n\nSaved to: {saved_file}", "magenta"))
                print(colored(f"Token usage: {stream.usage}", "yellow"))
            print(colored("-" * 80, "magenta"))

if __name__ == "__main__":
    composer = PromptComposer()
    composer.run()