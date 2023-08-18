import os
import json

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def process_skill(skill_dir):
    skillconfig_path = os.path.join(skill_dir, 'skillconfig.json')
    skillconfig_data = read_json_file(skillconfig_path)

    skill_name = skillconfig_data['name']
    intents = skillconfig_data['intents']
    functions = skillconfig_data['functions']

    output = f'{skill_name}:\n'
    for intent in intents:
        intent_name = intent['name']
        # intent_description = intent['description']
        intent_samples = intent['samples']
        for sample in intent_samples:
            intent_q = sample['Q']
            intent_a = sample['A']
            if type(intent_q) == list:
                for q in intent_q:
                    output += f'  {q}: {intent_a}\n'
            elif type(intent_q) == str:
                output += f'  {intent_q}: {intent_a}\n'
            else:
                print("type error")

    return output

def test_prompt():
    skills_directory = 'skills'

    # Process each skill directory
    skills_output = ""
    for subdir in os.listdir(skills_directory):
        if subdir != "map":
            continue
        skill_dir = os.path.join(skills_directory, subdir)
        if os.path.isdir(skill_dir):
            skills_output += process_skill(skill_dir)

    return skills_output

def main():
    print(test_prompt())

if __name__ == "__main__":
    main()
