# 2011Scape Drop Table Maker

![python3 11_2oUlTZsLmU](https://github.com/2011Scape/drop-table-maker/assets/75695035/71f08fad-f99e-4d1c-a682-86cf3a4ef39f)

Drop Table Maker is a Python application that allows you to create drop tables for game development in 2011Scape. It provides a user-friendly interface for defining item drops and their probabilities.

## Features

- Add and remove items with customizable drop probabilities to the drop table.
- Specify guaranteed drops for certain items.
- Generate Kotlin script code based on the defined drop table.
- Save the generated code to a file.

## Installation

1. Make sure you have Python 3 installed on your system.
2. Clone this repository:

   ```bash
   git clone https://github.com/HarleyGilpin/drop-table-maker.git
   ```

# Setting up the environment

To set up a Python virtual environment in VSCode on Windows, you can use the `venv` module that comes with Python. Here are the steps to follow:

1. Open VSCode and create a new folder for your project.
2. In the Explorer pane, right-click on the folder and select "Open in Terminal".
3. In the terminal, navigate to the folder you created in step 1.
4. Run the following command to create a new virtual environment:

```bash
python -m venv env
```

This will create a directory called `myenv/bin` that contains the scripts needed to activate and deactivate the virtual environment.

5. To activate the virtual environment, run the following command:

```bash
.\env\Scripts\activate
```

This will set up the necessary environment variables and make the virtual environment active. You can verify that the virtual environment is active by checking the prompt, which should now include the name of the virtual environment.

6. To deactivate the virtual environment, run the following command:

```bash
deactivate
```

This will restore the original environment and remove the virtual environment from the current terminal session.


# Building the Executable

Follow these steps to build your Python application into an executable:

1. Open a terminal or command prompt.
2. Navigate to the directory containing your Python application files.
3. Verify that the "Item_list.txt" file is present in the same directory as the "main.py" file. If the file is located elsewhere, adjust the file path accordingly in the command.
1. Run the following command to build the executable: `pyinstaller -w -F --add-data="Item_list.txt;." main.py`

   This command uses PyInstaller to create a single executable file (`-F`) that is launched as a Windows application without a console window (`-w`). The `--add-data` option includes the "Item_list.txt" file by specifying its filename and destination directory (`.` represents the current directory).
