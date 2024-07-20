import os
import anthropic
from termcolor import colored
from dotenv import load_dotenv
import re
from datetime import datetime
import json

# Load environment variables to set up the Anthropic API Key
load_dotenv()


class PromptComposer:

    def __init__(self):
        # Set up the Anthropic API Key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-3-5-sonnet-20240620"

        # Load prompt templates
        self.prompts = {
            'midjourney': self.load_prompt('prompts/midjourney.txt'),
            'udio': self.load_prompt('prompts/udio.txt')
        }

    @staticmethod
    def load_prompt(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def user_input(prompt, color='cyan'):
        """Fetch colored input from the user"""
        return input(colored(prompt, color))

    @staticmethod
    def print_colored(message, color='magenta'):
        """Print colored text to the console"""
        print(colored(message, color))

    def generate_completion(self, prompt_type, question):
        """Generate completion using Anthropic API"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.7,
            system=self.prompts[prompt_type],
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return message.content[0].text if isinstance(message.content, list) else message.content

    def save_output(self, prompt_type, question, user_input, output):
        # Set up the output directory
        path = f"outputs/{prompt_type}"
        os.makedirs(path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_question = re.sub(r'[^\w\-_\. ]', '_', question[:30])
        filename = f"{timestamp}_{sanitized_question}.txt"

        with open(os.path.join(path, filename), "w") as file:
            file.write(f"User Input: {user_input}\n\n")
            file.write(f"Output:\n{output}")

        return os.path.join(path, filename)

    def run(self):
        """The main function to execute the script"""
        while True:
            self.print_colored("\n=== Welcome to Prompt Gen ===", "blue")
            self.print_colored("Instructions:", "blue")
            self.print_colored("- Enter 'exit' to quit.")
            self.print_colored("- Enter '1' for midjourney or '2' for udio.")

            prompt_type = self.user_input("\nSelect prompt type (1/2): ").strip()
            
            if prompt_type == "exit":
                self.print_colored('Exiting... Goodbye!', 'red')
                break
            
            if prompt_type == '1':
                prompt_type = 'midjourney'
            elif prompt_type == '2':
                prompt_type = 'udio'
            else:
                self.print_colored('Invalid prompt type. Please try again.', 'red')
                continue

            question = self.user_input(f"\nPlease describe the {'image' if prompt_type == 'midjourney' else 'music'} you'd like to create: ")

            if question.lower().strip() == "exit":
                self.print_colored('Exiting... Goodbye!', 'red')
                break

            # Generate the completion
            output = self.generate_completion(prompt_type, question)
            
            # Print the generated output
            self.print_colored("\nGenerated Output:", "cyan")
            self.print_colored(output, "yellow")

            # Save the output to a file
            saved_file = self.save_output(prompt_type, question, question, output)
            self.print_colored(f"\nSaved output to: {saved_file}\n")
            self.print_colored("-" * 80)

# Run the script
if __name__ == "__main__":
    PromptComposer().run()