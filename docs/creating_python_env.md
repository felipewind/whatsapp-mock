To install pip modules only inside the scope of a project, you should use a virtual environment. This will isolate the dependencies for your project from the global Python environment. Here's how you can create and use a virtual environment:

1. **Create a virtual environment**:
   Navigate to your project directory and run:
   ```sh
   python -m venv env
   ```

   This will create a directory named `env` (or whatever you choose to name it) inside your project directory, containing a standalone Python installation.

2. **Activate the virtual environment**:
   - On Windows:
     ```sh
     .\env\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source env/bin/activate
     ```

   After activation, your command prompt will change to indicate that the virtual environment is active (typically by showing the name of the virtual environment in parentheses).

3. **Install pip modules**:
   With the virtual environment activated, install the modules you need using pip:
   ```sh
   pip install <package-name>
   ```

   These packages will be installed only within the virtual environment and won't affect the global Python installation.

4. **Deactivate the virtual environment**:
   Once you are done working in the virtual environment, you can deactivate it by simply running:
   ```sh
   deactivate
   ```

By following these steps, you ensure that all the pip modules are installed only within the scope of your project.