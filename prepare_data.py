# prepare_data.py

import json

def prepare_data(input_file, output_file, data_type='mitigation'):
    data = []
    with open(input_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if '|||' in line:
            if data_type == 'mitigation':
                mitigation, bug_overview = line.strip().split('|||')
                prompt = (
                    f"Given the following mitigations, provide a comprehensive bug overview:\n\n"
                    f"Mitigations:\n{mitigation.strip()}\n\nBug Overview:"
                )
                completion = f" {bug_overview.strip()}"
            elif data_type == 'code':
                code_snippet, analysis = line.strip().split('|||')
                prompt = (
                    f"As a highly skilled developer, analyze the following code for bugs and potential issues. "
                    f"Provide a detailed list of bugs, security vulnerabilities, and any improvements that can be made.\n\n"
                    f"Code:\n{code_snippet.strip()}\n\nAnalysis:"
                )
                completion = f" {analysis.strip()}"
            else:
                continue
            data.append({"prompt": prompt, "completion": completion})
    with open(output_file, 'w') as f_out:
        for item in data:
            f_out.write(json.dumps(item) + '\n')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Prepare data for fine-tuning.')
    parser.add_argument('--input_file', type=str, required=True, help='The input data file.')
    parser.add_argument('--output_file', type=str, default='training_data_prepared.jsonl', help='The output file name.')
    parser.add_argument('--data_type', type=str, choices=['mitigation', 'code'], default='mitigation', help='The type of data: mitigation or code.')

    args = parser.parse_args()

    prepare_data(args.input_file, args.output_file, data_type=args.data_type)
    print(f"Prepared data saved to {args.output_file}")
