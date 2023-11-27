import re
import yaml
import fileinput

class BumpVersion:
    def __init__(self, file_path="./VERSION"):
        self.file_path = file_path
        self.version = None  # Initialize version to None

    def info(self):
        print(f"File Path: {self.file_path}")
        if self.version:
            print(f"Current Version: {self.version['major']}.{self.version['minor']}.{self.version['patch']}")
        else:
            print("Version information not available. Use read_version_from_file method to read the version.")

    def read_version_from_file(self, file_path="./VERSION"):
        try:
            # Use the provided file_path or the default one
            file_path = file_path or self.file_path

            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()

            # Use regular expression to extract the version number
            version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', content)

            if version_match:
                # Populate the version dictionary
                self.version = {
                    'major': int(version_match.group(1)),
                    'minor': int(version_match.group(2)),
                    'patch': int(version_match.group(3))
                }
            else:
                print("Error: Unable to extract version from file.")

        except Exception as e:
            print(f"Error: {e}")

    def verify_version_format(self, version):
        try:
            # Split version into major, minor, and patch components
            major, minor, patch = map(int, version.split('.'))
            return True
        except ValueError:
            return False

    def update_version(self, new_version):
        try:
            # Verify the format of the new version
            if not self.verify_version_format(new_version):
                print("Error: Invalid version format. Please provide a version in X.X.X format.")
                return

            # Read the content of the file if version is not populated
            if self.version is None:
                self.read_version_from_file()

            # Update the version dictionary with the new version
            self.version['major'], self.version['minor'], self.version['patch'] = map(int, new_version.split('.'))

            # Format the new version string
            new_version_str = f"{self.version['major']}.{self.version['minor']}.{self.version['patch']}"

            # Read the content of the file
            with open(self.file_path, 'r') as file:
                content = file.read()

            # Use regular expression to find and replace the version number
            updated_content = re.sub(r'\d+\.\d+\.\d+', new_version_str, content)

            # Write the updated content back to the file
            with open(self.file_path, 'w') as file:
                file.write(updated_content)

            print(f"Version updated to {new_version_str} successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def update_version_in_file(self, file_path, new_version, version_variable="__version__"):
        try:
            # Read the content of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Find the line containing the specified version variable
            for i, line in enumerate(lines):
                if re.search(fr'{version_variable}\s*=\s*"\d+\.\d+\.\d+"', line):
                    lines[i] = f'{version_variable} = "{new_version}"\n'
                    break

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Version in {file_path} updated to {new_version} successfully.")

        except Exception as e:
            print(f"Error: {e}")
        print("Current version:", self.version)

        if self.verify_version_format(new_version):
            self.update_version(new_version)
            self.read_version_from_file()
            print("Updated version:", self.version)
        else:
            print("Invalid version format. Please provide a version in X.X.X format.")


    def read_package_name_from_setup(self):
        try:
            with open("setup.py", 'r') as file:
                content = file.read()

            # Use regular expression to find the package name in setup.py
            name_match = re.search(r'NAME\s*=\s*[\'"]([^\'"]+)[\'"]', content)

            if name_match:
                self.package_name = name_match.group(1)
                return self.package_name
            else:
                print("Error: Unable to extract package name from setup.py.")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def _read_files_to_change(self, yaml_file="bumpversion.yaml"):
        """

        :param yaml_file:
        :type yaml_file:
        :return:
        :rtype:

        the bumpversion yaml file looks like

        bumpversion:
        - cloudmesh/bumpversion/__init__.py
        - cloudmesh/bumpversion/__version__.py

        """
        try:
            with open(yaml_file, 'r') as file:
                yaml_data = yaml.safe_load(file)

            if 'bumpversion' in yaml_data and isinstance(yaml_data['bumpversion'], list):
                self.files_to_change = yaml_data['bumpversion']
                return self.files_to_change
            else:
                print(f"Error: Invalid or missing 'bumpversion' in {yaml_file}.")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def change_files(self, new_version):

        files = self._read_files_to_change(yaml_file="bumpversion.yaml")

        for file_path in files:
            self.update_version_in_file(file_path, new_version, version_variable="__version__")
            self.update_version_in_file(file_path, new_version, version_variable="version")

    def incr(self, component, file_path="./VERSION"):
        """
        Increments the specified version component (major, minor, or patch) in the specified file.

        :param component: The version component to increment (major, minor, or patch).
        :type component: str
        :param file_path: The path to the file containing the version information. If None, the default file_path is used.
        :type file_path: str
        """
        try:
            self.read_version_from_file(file_path=file_path)

            # Increment the specified version component
            if component == "major":
                self.version['major'] += 1
            elif component == "minor":
                self.version['minor'] += 1
            elif component == "patch":
                self.version['patch'] += 1
            else:
                print("Error: Invalid component. Use 'major', 'minor', or 'patch'.")
                return

            # Format the new version string
            new_version_str = f"{self.version['major']}.{self.version['minor']}.{self.version['patch']}"
            return new_version_str

        except Exception as e:
            print(f"Error: {e}")