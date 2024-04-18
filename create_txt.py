import os

def get_absolute_jpg_paths(relative_directory):
    # Get the absolute path of the provided directory
    absolute_directory = os.path.abspath(relative_directory)

    # List to store the paths of the JPG files
    jpg_paths = []

    # Iterate through all files in the directory
    for root, _, files in os.walk(absolute_directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                # Create the full path to the JPG file and add it to the list
                full_path = os.path.join(root, file)
                jpg_paths.append(full_path)

    return jpg_paths

def save_paths_to_txt(paths, output_file):
    # Write the paths to the text file
    with open(output_file, 'w') as file:
        for path in paths:
            # Replace single backslashes with double backslashes for Windows paths
            windows_path = path.replace('\\', '\\\\')
            windows_path = path.replace('JPG', 'jpg')
            file.write(windows_path + '\n')

    print(f"Paths of the JPG files saved to '{output_file}'")

if __name__ == "__main__":
    directory = input("Enter the directory: ")
    # Relative directory provided by the user
    relative_directory = f"./{directory}"

    # Name of the text file where the paths will be saved
    output_file = f'./data/{directory}.txt'

    # Get the absolute paths of the JPG files in the provided directory
    absolute_jpg_paths = get_absolute_jpg_paths(relative_directory)

    # Save the paths to the text file
    save_paths_to_txt(absolute_jpg_paths, output_file)
