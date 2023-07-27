import os
import ast
import argparse


WEIGHTS = {
    'return loss.': 10,
    'return loss': 10,
    'total_loss': 10,
    'forward': 5,
    'step': 1,
    'losses': 2,
    'training_step': 2,
    'model.train()': 10,
    'training step': 1,
    'trainer': 2,
    'enumerate': 1,
    'batch_idx': 1,
    'train_one_epoch': 5,
    'one_epoch': 1,
    'one_step': 1,
    'loss =': 5,
    'loss': 1
}

def get_py_files(dir_path):
    py_files = []
    current_file = os.path.basename(__file__)
    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py') and current_file not in file_path:
                py_files.append(file_path)
    return py_files

def get_function_scores(file_path):
    function_scores = {}
    keywords_found = set()
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            for keyword in WEIGHTS:
                weight = WEIGHTS.get(keyword, 1)
                if keyword in name:
                    if file_path not in function_scores:
                        function_scores[file_path] = 0
                    function_scores[file_path] += weight
                    keywords_found.add(keyword)
        elif isinstance(node, ast.Name):
            for keyword in WEIGHTS:
                weight = WEIGHTS.get(keyword, 1)
                if keyword in node.id:
                    if file_path not in function_scores:
                        function_scores[file_path] = 0
                    function_scores[file_path] += weight
                    keywords_found.add(keyword)
        elif isinstance(node, ast.Str):
            for keyword in WEIGHTS:
                weight = WEIGHTS.get(keyword, 1)
                if keyword in node.s:
                    if file_path not in function_scores:
                        function_scores[file_path] = 0
                    function_scores[file_path] += weight
                    keywords_found.add(keyword)

    return function_scores, keywords_found

def get_scores(dir_path):
    file_scores = []
    py_files = get_py_files(dir_path)
    all_keywords_found = set()
    for file_path in py_files:
        function_score, keywords_found = get_function_scores(file_path)
        if function_score:
            file_scores.append((file_path, function_score[file_path], keywords_found))
            all_keywords_found.update(keywords_found)
    return file_scores, all_keywords_found

def find_most_likely_loss_function(dir_path):
    file_scores, all_keywords_found = get_scores(dir_path)
    sorted_file_scores = sorted(file_scores, key=lambda x: x[1], reverse=True)

    if sorted_file_scores:
        print("\n/*===----------------------------------------------------------------------===*/")
        print(" * Files and their scores")
        print("/*===----------------------------------------------------------------------===*/")
        max_len = max(len(file_path) for file_path, _, _ in sorted_file_scores)
        for file_path, score, keywords in sorted_file_scores:
            spaces = " " * (max_len - len(file_path))
            print(f"\033[93m{file_path}{spaces}\033[0m Score: {score}")
            print(f"\tKeywords Found: {', '.join(keywords)}")
            print("---------------------------------------------------------------------------")
    else:
        print("No file found that contains the keywords")
    
    print("\nKeywords and their weights in the files:")
    for keyword in all_keywords_found:
        weight = WEIGHTS.get(keyword, 1)
        print(f"{keyword}: {weight}")

    if sorted_file_scores:
        most_likely_file = sorted_file_scores[0][0]
        print("\n/*===----------------------------------------------------------------------===*/")
        print(" * Most Likely Loss Function")
        print(f"\033[92m =====> {most_likely_file} \033[0m")
        print("/*===----------------------------------------------------------------------===*/")

def main():
    parser = argparse.ArgumentParser(description="Find the most likely loss function in Python files.")
    parser.add_argument("--dir_path", type=str, default="./", help="Path to the directory to scan (default: current directory)")
    args = parser.parse_args()

    find_most_likely_loss_function(args.dir_path)

if __name__ == "__main__":
    main()