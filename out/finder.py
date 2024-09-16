import os
import sys
import re

def search_word_in_file(file_path, word):
    matches = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for i, line in enumerate(file, 1):
            if re.search(word, line, re.IGNORECASE):
                matches.append((i, line.strip()))
    return matches

def search_word_in_project(project_path, word):
    results = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.txt', '.md', '.java', '.js', '.html', '.css')):  # Adicione ou remova extensões conforme necessário
                file_path = os.path.join(root, file)
                matches = search_word_in_file(file_path, word)
                if matches:
                    results.append((file_path, matches))
    return results

def print_results(results):
    for file_path, matches in results:
        print(f"Arquivo: {file_path}")
        for line_num, line in matches:
            print(f"  Linha {line_num}: {line}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python Finder.py <caminho do projeto> <palavra para busca>")
        sys.exit(1)

    project_path = sys.argv[1]
    word = sys.argv[2]

    if not os.path.isdir(project_path):
        print(f"O caminho {project_path} não é um diretório válido.")
        sys.exit(1)

    results = search_word_in_project(project_path, word)
    print_results(results)

if __name__ == "__main__":
    main()
