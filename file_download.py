import sys
import file_translation








if __name__ == "__main__":
    parameters = sys.argv[1:]
    user_folder = str(parameters[1])
    file = str(parameters[0])
    directory = str(parameters[2])
    rel_path = str(parameters[3])
    print("FILE: "+file)
    print("USER_FOLDER = "+user_folder)
    file_translation.file_recomposition(file, user_folder, directory, rel_path)
