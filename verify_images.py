import os

def find_missing_files(directory):
    # Get the absolute path of the provided directory
    absolute_directory = os.path.abspath(directory)

    # List to store the paths of missing JPG and TXT files
    missing_jpg_files = []
    missing_txt_files = []

    # Iterate through all files in the directory
    for root, _, files in os.walk(absolute_directory):
        for file in files:
            # Check if the file is a JPG
            if file.lower().endswith('.jpg'):
                jpg_name = os.path.splitext(file)[0]  # Remove the extension
                # Check if there is no corresponding TXT file
                txt_file = jpg_name + '.txt'
                if txt_file not in files:
                    # Create the full path to the JPG file and add to the list
                    jpg_path = os.path.join(root, file)
                    missing_txt_files.append(jpg_path)
            # Check if the file is a TXT
            elif file.lower().endswith('.txt'):
                txt_name = os.path.splitext(file)[0]  # Remove the extension
                # Check if there is no corresponding JPG file
                jpg_file = txt_name + '.jpg'
                JPG_file = txt_name + '.JPG'
                if jpg_file not in files and JPG_file not in files:
                    # Create the full path to the TXT file and add to the list
                    txt_path = os.path.join(root, file)
                    missing_jpg_files.append(txt_path)

    return missing_jpg_files, missing_txt_files

if __name__ == "__main__":
    # Directory provided by the user
    directory = input("Enter the directory path: ")

    # Find the missing JPG and TXT files in the provided directory
    missing_jpg, missing_txt = find_missing_files(directory)

    # Print the missing JPG files
    if missing_jpg:
        print("JPG files without matching TXT files:")
        for jpg_path in missing_jpg:
            print(jpg_path)
    else:
        print("No JPG files without matching TXT files found.")

    print()  # Empty line for separation

    # Print the missing TXT files
    if missing_txt:
        print("TXT files without matching JPG files:")
        for txt_path in missing_txt:
            print(txt_path)
    else:
        print("No TXT files without matching JPG files found.")
