import os

def clean_cache_dir():
    current_file = os.path.abspath(__file__)
    cache_dir = os.path.dirname(current_file)
    for filename in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, filename)
        if file_path != current_file and os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    clean_cache_dir()