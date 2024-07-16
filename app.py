from flask import Flask, render_template
import os
import re
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    user_input = re.search(r'User Input: (.+)', content)
    output = re.search(r'Output:\n(.*)', content, re.DOTALL)
    
    if output:
        output_text = output.group(1).strip()
        try:
            root = ET.fromstring(f'<root>{output_text}</root>')
            formatted_output = ""
            for prompt in root.findall('.//prompt'):
                text = prompt.find('text').text.strip()
                explanation = prompt.find('explanation').text.strip()
                formatted_output += f"Prompt: {text}\n\nExplanation: {explanation}\n\n---\n\n"
        except ET.ParseError:
            formatted_output = output_text
    else:
        formatted_output = ""

    return {
        'user_input': user_input.group(1) if user_input else '',
        'output': formatted_output
    }

@app.route('/')
def index():
    outputs = {'midjourney': [], 'udio': []}
    for prompt_type in outputs.keys():
        outputs_dir = f'outputs/{prompt_type}'
        if os.path.exists(outputs_dir):
            for filename in sorted(os.listdir(outputs_dir), key=lambda x: x.split('_')[:2], reverse=True):
                if filename.endswith('.txt'):
                    file_path = os.path.join(outputs_dir, filename)
                    parsed_content = parse_file(file_path)
                    outputs[prompt_type].append({'filename': filename, 'content': parsed_content})
    return render_template('index.html', outputs=outputs)

if __name__ == '__main__':
    app.run(debug=True)