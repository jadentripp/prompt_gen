from flask import Flask, render_template
import os
import re

app = Flask(__name__)

def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    user_input = re.search(r'User Input: (.+)', content)
    output = re.search(r'Output:\n(.*?)<prompts>', content, re.DOTALL)
    prompts = re.findall(r'<prompt>\s*<text>(.*?)</text>\s*<explanation>(.*?)</explanation>\s*</prompt>', content, re.DOTALL)
    
    return {
        'user_input': user_input.group(1) if user_input else '',
        'output': output.group(1).strip() if output else '',
        'prompts': [{'text': text.strip(), 'explanation': explanation.strip()} for text, explanation in prompts]
    }

@app.route('/')
def index():
    outputs = []
    outputs_dir = 'outputs/claude'
    for filename in os.listdir(outputs_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(outputs_dir, filename)
            parsed_content = parse_file(file_path)
            outputs.append({'filename': filename, 'content': parsed_content})
    return render_template('index.html', outputs=outputs)

if __name__ == '__main__':
    app.run(debug=True)