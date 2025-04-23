import os

def count_lines_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            return sum(1 for line in file)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

def count_lines(root_dir, exclude_dirs):
    total_lines = 0
    for root, dirs, files in os.walk(root_dir):
        # Удаляем исключенные директории из списка для обхода
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            total_lines += count_lines_in_file(file_path)
    
    return total_lines

if __name__ == "__main__":
    # Настройки
    ROOT_DIRECTORY = '.'  # Текущая директория
    EXCLUDE_DIRS = ['venv', '.git', '__pycache__', 'node_modules']  # Игнорируемые папки

    # Подсчет строк
    lines_count = count_lines(ROOT_DIRECTORY, EXCLUDE_DIRS)
    print(f"Total lines: {lines_count}")