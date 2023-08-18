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
            intent_fewshot = sample['fewshot'] if 'fewshot' in sample else False
            if intent_fewshot:
                intent_q = sample['Q']
                if type(intent_q) == list:
                    intent_q = intent_q[0]
                
                intent_a = sample['A']
                output += f'  {intent_q}: {intent_a}\n'

        # intent_function = intent['function']

        # output += f'  {intent_description}(e.g.{intent_samples}): {intent_function}\n'
        # output += f'  {intent_description}: {intent_samples}\n'

    output += f'\n\nFunctions: {functions}\n'
    return output

def get_prompt():
    skills_directory = 'skills'
    instruction_path = os.path.join(skills_directory, 'instruction.txt')
    instruction_data = read_text_file(instruction_path)

    # Process each skill directory
    skills_output = ""
    for subdir in os.listdir(skills_directory):
        if subdir != "map":
            continue
        skill_dir = os.path.join(skills_directory, subdir)
        if os.path.isdir(skill_dir):
            skills_output += process_skill(skill_dir)

    # Replace {Skills} with skills_output
    instruction_data = instruction_data.replace("{Skills}", skills_output)

    # Read fewshots.json and replace {FewShots} with its content
    # fewshots_path = os.path.join(skills_directory, 'fewshots.txt')
    # fewshots_data = read_text_file(fewshots_path)
    # instruction_data = instruction_data.replace("{FewShots}", json.dumps(fewshots_data, indent=2, ensure_ascii=False))

    return instruction_data

def main():
    print(get_prompt())

if __name__ == "__main__":
    main()
