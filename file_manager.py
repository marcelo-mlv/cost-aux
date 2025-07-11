import os

class FileManager:
    def search_files_by_extension(self, directory, extension):
        files = [f for f in os.listdir(directory) if f.endswith(extension)]
        return files

    def does_file_exist(self, file_path):
        return os.path.exists(file_path)
    
    def start_file(self, file_path):
        if not self.does_file_exist(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        return os.startfile(file_path)
