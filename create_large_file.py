def double_file_contents(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    doubled_lines = [line.strip() * 2 + "\n" for line in lines]

    with open(file_path, "w") as file:
        file.writelines(doubled_lines)


# Example usage
file_path = "data.txt"
double_file_contents(file_path)
