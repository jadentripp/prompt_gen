import os
import anthropic
from termcolor import colored
from dotenv import load_dotenv
import re
from datetime import datetime

# Load environment variables and set up the Anthropic API Key
load_dotenv()


class PromptComposer:

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-3-5-sonnet-20240620"

        # Load the prompt template
        with open('prompts/claude_prompt.txt', 'r') as file:
            self.system_prompt = file.read()

    @staticmethod
    def user_input(prompt, color='cyan'):
        """Fetch colored input from the user"""
        return input(colored(prompt, color))

    @staticmethod
    def print_colored(message, color='magenta'):
        """Print colored text to the console"""
        print(colored(message, color))

    def generate_completion(self, question):
        """Generate completion using Anthropic API"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.7,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return message.content[0].text if isinstance(message.content, list) else message.content

    def save_output(self, question, user_input, output):
        path = "outputs/claude"
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
            self.print_colored(
                "\n=== Welcome to the Midjourney Prompt Composer (Claude Edition) ===",
                "blue")
            self.print_colored("Instructions:", "blue")
            self.print_colored("- Enter 'exit' to quit.")

            question = self.user_input(
                "\nPlease describe the image you'd like to create today. "
                "This can be a simple idea like a single word, a category like 'images of space in pastel', or a more detailed description. "
                "When offering a detailed description, consider factors such as the setting, objects, people, colors, mood, time of day, and more. "
                "The more specific you are, the better the output will align with your vision. "
                "For instance, instead of 'a garden', you might say 'a sunlit garden in spring, full of blooming tulips and a wooden bench'. "
                "However, don't worry if you only have a broad concept in mind — the tool can still create interesting results from less detailed prompts.\n"
            )

            if question.lower().strip() == "exit":
                self.print_colored('Exiting... Goodbye!', 'red')
                break

            output = self.generate_completion(question)
            self.print_colored("\nGenerated Output:", "cyan")
            self.print_colored(output, "yellow")
            
            saved_file = self.save_output(question, question, output)
            self.print_colored(f"\nSaved output to: {saved_file}\n")
            self.print_colored("-" * 80)


if __name__ == "__main__":
    PromptComposer().run()