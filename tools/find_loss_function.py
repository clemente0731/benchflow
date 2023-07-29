import os
import ast
import argparse


# WEIGHTS = {
#     "return loss.": 10,
#     "return loss": 10,
#     "total_loss": 10,
#     "loss_fn": 10,
#     "training_loss":10,
#     "loss_values": 5,
#     "criterion": 8,
#     "train_loss": 10,
#     "batch_loss": 5,
#     "metrics": 5,
#     "forward": 5,
#     "step": 1,
#     "losses": 5,
#     "train_epoch_loss": 5,
#     "one_epoch_loss": 5,
#     "step_losses": 5,
#     "training_step": 2,
#     "model.train()": 10,
#     "training step": 5,
#     "loss_gradients": 5,
#     "loss_tensor": 6,
#     "loss_reduction": 4,
#     "output_loss": 10,
#     "total_losses": 10,
#     "loss_metrics": 5,
#     "loss_sum": 5,
#     "step_loss": 1,
#     "model_loss": 10,
#     "loss_per_epoch": 5,
#     "mean_loss": 5,
#     "loss_values": 5,
#     "training_loss": 10,
#     "loss_value": 5,
#     "trainer_loss": 1,
#     "loss_rate": 5,
#     "loss_values_list": 5,
#     "batch_loss": 5,
#     "train_epoch_loss": 5,
#     "one_epoch_loss": 5,
#     "step_losses": 5,
#     "loss_gradients": 5,
#     "loss_tensor": 6,
#     "loss_reduction": 4,
#     "bce_loss": 6,
#     "bce_logits_loss": 6,
#     "nll_loss": 6,
#     "kld_loss": 5,
#     "l1_loss": 5,
#     "smooth_l1_loss": 5,
#     "cosine_similarity_loss": 4,
#     "triplet_margin_loss": 5,
#     "multi_label_margin_loss": 5,
#     "hinge_embedding_loss": 5,
#     "multi_label_soft_margin_loss": 6,
#     "multi_margin_loss": 6,
#     "soft_margin_loss": 6,
#     "triplet_margin_distance_loss": 6,
#     "cosine_embedding_loss": 6,
#     "margin_ranking_loss": 6,
#     "huber_loss": 6,
#     "mse_loss": 7,
#     "l1_loss": 5,
#     "cosine_embedding_loss": 7,
#     "cross_entropy_loss": 8,
#     "reduction_loss": 5,
#     "mse_loss_value": 8,
#     "mean_squared_error_loss": 8,
#     "l1_loss_value": 8,
#     "smooth_l1_loss_value": 8,
#     "loss_function": 5,
#     "loss_results": 5,
#     "loss_predictions": 5,
#     "L1_Loss": 5,
#     "loss_classification": 5,
#     "recon_loss": 5,
#     "recon_error": 5,
#     "mean()":5,
#     "sum()":5,
#     "trainer": 1,
#     "enumerate": 5,
#     "batch_idx": 5,
#     "train_one_epoch": 5,
#     "one_epoch": 5,
#     "one_step": 5,
#     "loss =": 5,
#     "loss": 5,
#     "torch.nn": 2,
#     "nn.Module": 2,
#     "functional": 2,
#     "CrossEntropyLoss": 6,
#     "MSELoss": 6,
#     "loss.backward": 5,
#     "torch.Tensor": 6,
#     "reduction": 4,
#     "BCELoss": 6,
#     "BCEWithLogitsLoss": 6,
#     "NLLLoss": 6,
#     "KLDivLoss": 5,
#     "L1Loss": 5,
#     "SmoothL1Loss": 5,
#     "CosineSimilarity": 4,
#     "TripletMarginLoss": 5,
#     "MultiLabelMarginLoss": 5,
#     "HingeEmbeddingLoss": 5,
#     "MultiLabelSoftMarginLoss": 6,
#     "MultiMarginLoss": 6,
#     "SoftMarginLoss": 6,
#     "TripletMarginWithDistanceLoss": 6,
#     "CosineEmbeddingLoss": 6,
#     "MarginRankingLoss": 6,
#     "HuberLoss": 6,
#     "MultiMarginLoss": 7,
#     "SoftMarginLoss": 5,
#     "CosineEmbeddingLoss": 7,
#     "cross_entropy": 8,
#     "reduction": 5,
#     "mse_loss": 8,
#     "mse": 8,
#     "l1_loss": 8,
#     "smooth_l1_loss": 8,
# }


WEIGHTS = {
"loss": 3.0,
"loss = ":10.0,
"losses = sum": 10.0,
"losses = ":10.0,
"total_loss": 10.0,
"return loss": 10.0,
"model_loss": 10.0,
"training_loss": 10.0,
"output_loss": 10.0,
"loss_fn": 10.0,
"metrics": 5.0,
"training": 7.0,
"return loss.": 10.0,
"model.train()": 10.0,
"train_loss": 10.0,
"cross_entropy_loss": 8.0,
"mse_loss": 7.667,
"mse_loss_value": 8.0,
"mse": 8.0,
"smooth_l1_loss": 7.667,
"smooth_l1_loss_value": 8.0,
"l1_loss": 6.0,
"cosine_embedding_loss": 6.33,
"bceloss": 6.0,
"bcewithlogitsloss": 6.0,
"nllloss": 6.0,
"kldivloss": 5.0,
"mseloss": 6.0,
"bce_loss": 6.0,
"bce_logits_loss": 6.0,
"multi_label_soft_margin_loss": 6.0,
"margin_ranking_loss": 6.0,
"multi_margin_loss": 6.0,
"soft_margin_loss": 5.667,
"multi_label_margin_loss": 5.0,
"hinge_embedding_loss": 5.0,
"loss_metrics": 5.0,
"loss_sum": 5.0,
"step_loss": 1.0,
"losses": 5.0,
"training_step": 2.0,
"loss_per_epoch": 5.0,
"mean_loss": 5.0,
"loss_values": 5.0,
"loss_value": 5.0,
"trainer_loss": 1.0,
"loss_rate": 5.0,
"loss_values_list": 5.0,
"batch_loss": 5.0,
"train_epoch_loss": 5.0,
"one_epoch_loss": 5.0,
"step_losses": 5.0,
"loss_gradients": 5.0,
"loss_tensor": 6.0,
"loss_reduction": 4.5,
"cosine_similarity_loss": 4.0,
"triplet_margin_loss": 5.0,
"hinge_embedding_loss": 5.0,
"cosine_similarity_loss": 4.0,
"triplet_margin_loss": 5.0,
"multi_label_margin_loss": 5.0,
"hinge_embedding_loss": 5.0,
"multi_label_soft_margin_loss": 6.0,
"multi_margin_loss": 6.0,
"soft_margin_loss": 5.67,
"triplet_margin_distance_loss": 6.0,
"cosine_embedding_loss": 6.0,
"margin_ranking_loss": 6.0,
"huber_loss": 6.0,
"mse_loss": 7.67,
"l1_loss": 6.0,
"cosine_embedding_loss": 6.33,
"cross_entropy_loss": 8.0,
"reduction_loss": 4.5,
"mean_squared_error_loss": 8.0,
"l1_loss_value": 8.0,
"mean_squared_error_loss": 8.0,
"l1_loss_value": 8.0,
"smooth_l1_loss_value": 8.0,
"loss_function": 5.0,
"loss_results": 5.0,
"loss_predictions": 5.0,
"loss_classification": 5.0,
"recon_loss": 5.0,
"recon_error": 5.0,
"mean()": 5.0,
"sum()": 5.0,
"trainer": 1.0,
"enumerate": 5.0,
"batch_idx": 5.0,
"train_one_epoch": 5.0,
"one_epoch": 5.0,
"one_step": 5.0,
"loss =": 5.0,
"torch.nn": 2.0,
"nn.module": 2.0,
"functional": 2.0,
"crossentropyloss": 6.0,
"mseloss": 6.0,
"loss.backward": 5.0,
"torch.tensor": 6.0,
"reduction": 4.0,
"bceloss": 6.0,
"bcewithlogitsloss": 6.0,
"nllloss": 6.0
}


def get_py_files(dir_path):
    """Recursively find all Python files in the given directory, excluding files starting with 'test_'.

    Args:
        dir_path (str): Path to the directory to search for Python files.

    Returns:
        List[str]: List of file paths to Python files found in the directory.
    """
    py_files = []
    current_file = os.path.basename(__file__)
    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file ends with '.py', is not the current script file, and doesn't start with 'test_'
            if (
                file.endswith(".py")
                and current_file not in file_path
                and not os.path.basename(file_path).startswith("test_")
            ):
                py_files.append(file_path)
    return py_files

def get_function_scores(file_path):
    """Calculate the function scores and keywords found in a Python file."""
    function_scores = {}
    keywords_found = []  # Changed to list instead of set
    try:
        with open(file_path, "r") as f:
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
                        keywords_found.append(keyword)  # Append to the list
            elif isinstance(node, ast.Name):
                for keyword in WEIGHTS:
                    weight = WEIGHTS.get(keyword, 1)
                    if keyword in node.id:
                        if file_path not in function_scores:
                            function_scores[file_path] = 0
                        function_scores[file_path] += weight
                        keywords_found.append(keyword)  # Append to the list
            elif isinstance(node, ast.Str):
                for keyword in WEIGHTS:
                    weight = WEIGHTS.get(keyword, 1)
                    if keyword in node.s:
                        if file_path not in function_scores:
                            function_scores[file_path] = 0
                        function_scores[file_path] += weight
                        keywords_found.append(keyword)  # Append to the list

    except SyntaxError as e:
        # Skip the file with ast parsing error and print a red warning
        print("\033[91mWARNING: Error parsing file - {}\033[0m".format(file_path))
    return function_scores, keywords_found


def print_green(text):
    """Print text in green color."""
    print("\033[92m" + text + "\033[0m")

def get_scores(dir_path):
    """Get the scores for all Python files in the given directory."""
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
    """Find the most likely loss function in Python files."""
    file_scores, all_keywords_found = get_scores(dir_path)
    sorted_file_scores = sorted(file_scores, key=lambda x: x[1], reverse=True)

    total_files = len(sorted_file_scores)
    top_percentile_files = int(total_files * 0.5)
    top_files = sorted_file_scores[:top_percentile_files]

    if top_files:
        print(
            "\n/*===----------------------------------------------------------------------===*/"
        )
        print(" * Files and their scores (Top 50%)")
        print(
            "/*===----------------------------------------------------------------------===*/"
        )
        for file_path, file_score, keywords in top_files:
            print(f"\033[93m{file_path}\033[0m Total Score: {file_score}")
            print(f"\tKeywords Found: {', '.join(keywords)}")
            
            # Calculate the total number of keywords found in the file
            total_keywords_found = len(keywords)
            print(f"\tTotal Keywords Found: {total_keywords_found}")

            # Calculate the occurrence count of each keyword in the file
            keyword_occurrence_count = {}
            for keyword in keywords:
                keyword_occurrence_count[keyword] = keywords.count(keyword)

            # Print the occurrence count of each keyword
            print("\tKeyword Occurrence Count:")
            for keyword, count in keyword_occurrence_count.items():
                print(f"\t\t{keyword}: {count} occurrences")

            # Calculate the sum of scores for functions in the file
            functions_score_sum = sum(WEIGHTS.get(keyword, 1) for keyword in keywords)

            # Sort functions based on their weighted score proportions
            functions_with_scores = []
            printed_functions = set()  # To keep track of already printed functions
            with open(file_path, "r") as f:
                tree = ast.parse(f.read(), filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        if func_name in printed_functions:
                            continue  # Skip if the function name has already been printed
                        func_weighted_score = WEIGHTS.get(func_name, 1)
                        func_proportion = func_weighted_score / functions_score_sum
                        functions_with_scores.append((func_name, func_proportion))
                        printed_functions.add(func_name)

            # Sort functions in descending order based on their score proportions
            sorted_functions = sorted(
                functions_with_scores, key=lambda x: x[1], reverse=True
            )

            # Display the top 30% functions within each file
            top_percentile_functions = int(len(sorted_functions) * 0.3)
            for func_name, func_proportion in sorted_functions[
                :top_percentile_functions
            ]:
                print(
                    f"\tdef {func_name}: ===> Weighted Score Proportion: {func_proportion}"
                )

            print(
                "---------------------------------------------------------------------------"
            )
        print(
            "\n/*===----------------------------------------------------------------------===*/"
        )

        # Display the most likely files overall (top 10) in green color
        print_green("\nMost Likely Loss Function Files (Top 10):")
        for idx, (file_path, file_score, _) in enumerate(sorted_file_scores[:10]):
            print_green(f"{idx + 1}. {file_path} ===> Total Score: {file_score}")

    else:
        print("No file found that contains the keywords")

def main():
    parser = argparse.ArgumentParser(
        description="Find the most likely loss function in Python files."
    )
    parser.add_argument(
        "--dir_path",
        type=str,
        default="./",
        help="Path to the directory to scan (default: current directory)",
    )
    args = parser.parse_args()

    find_most_likely_loss_function(args.dir_path)


if __name__ == "__main__":
    main()
