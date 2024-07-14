## README

### Project Overview

This project is a Prompt Generator designed to create and manage AI prompts using the Anthropic API and Flask for the web interface. It includes Python scripts for generating prompts and a simple web application for viewing the outputs.

### Project Structure

- **.gitignore**: Specifies files and directories to be ignored by Git.
- **app.py**: Main script for running the prompt generator and Flask web application.
- **main.py**: Script for handling prompt generation.
- **outputs/**: Directory where generated prompts and outputs are stored.
- **prompts/**: Directory containing prompt templates.
- **templates/**: Directory for storing HTML templates used in the web application.

### Usage

#### Running the Application

To run the prompt generator application, use the following command:

```sh
python main.py
```

#### Running the Flask Web Application

To run the Flask web application for viewing generated outputs, use the following command:

```sh
python app.py
```

Access the web application in your browser at `http://127.0.0.1:5000`.

### Project Components

#### Prompt Generation Script (main.py)

- **PromptComposer**: Class responsible for generating prompts using the Anthropic API.
- **Methods**:
  - `user_input(prompt, color='cyan')`: Fetch colored input from the user.
  - `print_colored(message, color='magenta')`: Print colored text to the console.
  - `generate_completion(question)`: Generate completion using Anthropic API.
  - `save_output(question, user_input, output)`: Save the generated output to a file.
  - `run()`: Main function to execute the script and interact with the user.

#### Flask Web Application (app.py)

- **index()**: Route to render the index page with a list of generated outputs.
- **parse_file(file_path)**: Function to parse the content of the output files.

### Directory Structure

- **outputs/**: Contains generated prompt outputs.
- **prompts/**: Contains prompt templates.
- **templates/**: Contains HTML templates for the Flask web application.

### Contact

For any questions or suggestions, please create an issue here on Github, or comment on X: https://x.com/jadotripp42/status/1812620615142330655
