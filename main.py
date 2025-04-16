import argparse
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait
import os

executor = ThreadPoolExecutor(max_workers=os.cpu_count())
futures = []

def copy_file(file_path: Path, target_dir: Path):
    ext = file_path.suffix[1:].lower()
    if not ext:
        return
    target_path = target_dir / ext
    target_path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, target_path / file_path.name)

def process_directory(source_dir: Path, target_dir: Path):
    for item in source_dir.iterdir():
        if item.is_dir():
            futures.append(executor.submit(process_directory, item, target_dir))
        elif item.is_file():
            futures.append(executor.submit(copy_file, item, target_dir))

def main():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширеннями.")
    parser.add_argument("source", help="Шлях до директорії з файлами.")
    parser.add_argument("destination", nargs="?", default="dist", help="Цільова директорія (за замовчуванням dist).")

    args = parser.parse_args()
    source = Path(args.source)
    destination = Path(args.destination)

    if not source.exists() or not source.is_dir():
        print(f"Вказаний шлях {source} не існує або не є директорією.")
        return

    destination.mkdir(parents=True, exist_ok=True)

    process_directory(source, destination)

    # Чекаємо, поки всі задачі завершаться
    wait(futures)
    executor.shutdown(wait=True)
    print("Копіювання завершено.")

if __name__ == "__main__":
    main()
