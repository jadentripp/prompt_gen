# AI Prompt Generator

## Project Overview

This project is an AI Prompt Generator that creates prompts for Midjourney v6 image generation and Udio music generation using the Anthropic API. It includes a command-line interface for generating prompts and a Flask web application for viewing the outputs.

## Project Structure

- `app.py`: Flask web application for viewing generated prompts
- `main.py`: Command-line interface for generating prompts
- `prompts/`: Directory containing prompt templates
  - `midjourney.txt`: Template for Midjourney v6 prompts
  - `udio.txt`: Template for Udio music prompts
- `outputs/`: Directory where generated prompts are stored
- `templates/`: HTML templates for the web application

## Setup and Usage

1. Install required dependencies:
   ```
   pip install flask anthropic termcolor python-dotenv
   ```

2. Set up your Anthropic API key in a `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. Run the prompt generator:
   ```
   python main.py
   ```

4. Run the Flask web application:
   ```
   python app.py
   ```
   Access the web interface at `http://127.0.0.1:5000`

## Features

### Prompt Generation (main.py)

- Supports Midjourney v6 and Udio prompt generation
- Uses Anthropic's Claude 3.5 Sonnet model
- Saves generated prompts to files with timestamps

### Web Interface (app.py)

- Displays generated prompts in a responsive layout
- Supports pagination for large numbers of prompts
- Parses and formats XML output from the prompt generator

## Prompt Templates

### Midjourney v6 (midjourney.txt)

- Generates 5 diverse image prompts
- Incorporates Midjourney v6 best practices and parameters
- Includes explanations for each generated prompt

Key parameters:
- Aspect ratio (--ar)
- Chaos (--chaos)
- Quality (--quality)
- Seed (--seed)
- Stylize (--stylize)
- Weird (--weird)
- Tile (--tile)
- No (negative prompting)

### Udio Music (udio.txt)

- Generates 5 diverse music prompts
- Focuses on genre, mood, instruments, tempo, and lyrical themes
- Utilizes Udio-specific features and parameters

Key features:
- Custom lyrics
- Instrumental mode
- Manual mode
- Extension mode
- Remixing
- Inpainting

## Development

- The project uses Flask for the web framework
- Jinja2 is used for HTML templating
- CSS is used for responsive design
- JavaScript handles dynamic content loading and pagination

## Contributing

Contributions are welcome! Please submit pull requests or open issues for any bugs or feature requests.
