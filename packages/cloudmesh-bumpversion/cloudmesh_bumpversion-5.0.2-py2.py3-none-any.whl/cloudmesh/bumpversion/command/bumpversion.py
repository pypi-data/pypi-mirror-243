from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.variables import Variables
from cloudmesh.common.util import banner
from cloudmesh.bumpversion.bumpversion import BumpVersion

class BumpversionCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_bumpversion(self, args, arguments):
        """
        ::

          Usage:
                bumpversion patch
                bumpversion minor
                bumpversion major
                bumpversion info
                bumpversion set --version=VERSION
                bumpversion --config=YAML --version=VERSION


          Manages bumping the version for cloudmesh

          Arguments:
              VERSION  the version number to set
              YAML  the yaml file name

          Options:
              --version=VERSION   the version number to set
              --config=YAML   the YAML FILE

          Description:

            this program modifies the following files.

            It reads the VERSION form the ./VERSION file
            the number is of the form MAYOR.MINOR.PATCH
            It increase the specified number
            It writes the number to the files
            ./VERSION
            ./cloudmesh/cloudmesh-PACKAGE/__init__.py
            ./cloudmesh/cloudmesh-PACKAGE/__version__.py

            > cms bumpversion patch
            >    increaments the third number

            > cms bumpversion minor
            >    increaments the second number number

            > cms bumpversion mayor
            >    increaments the first number number

            > cms bumpversion info
            >    lists the numbers and identifies if one of them is wrong

            > cms bumpversion set --version=VERSION
            >   sets the version number to the spcified number

            > cms bumpversion --config=YAML --version=VERSION
            >   sets the versions in the files specifed in the yaml file

            > Example: bumpversion.yaml
            >
            > bumpversion:
            > - cloudmesh/bumpversion/__init__.py
            > - cloudmesh/bumpversion/__version__.py
            > - VERSION


        """


        # arguments.FILE = arguments['--file'] or None

        # switch debug on

        def update(component):

            bump_version = BumpVersion()

            bump_version.info()


            new_version = bump_version.incr(component)

            banner(new_version)

            if bump_version.verify_version_format(new_version):
                bump_version.update_version(new_version)
                bump_version.read_version_from_file()
                bump_version.info()

                package = bump_version.read_package_name_from_setup().replace("-", "/")

                # Update version in bumpversion/{package}/__init__.py
                init_file_path = f"{package}/__init__.py"  # Change this to the actual path of your __init__.py file
                bump_version.update_version_in_file(init_file_path, new_version, version_variable="__version__")

                # Example 2: Update version in bumpversion/version.py
                version_file_path = f"{package}/__version__.py"  # Change this to the actual path of your version.py file
                bump_version.update_version_in_file(version_file_path, new_version, version_variable="version")

                bump_version.read_version_from_file()
                bump_version.info()
            else:
                print("Invalid version format. Please provide a version in X.X.X format with integer components.")

        map_parameters(arguments, "version", "config")

        VERBOSE(arguments)

        if arguments.patch:
            update("patch")

        elif arguments.minor:
            update("minor")

        elif arguments.major:
            update("major")

        elif arguments.info:
            version_file_path = "VERSION"  # Change this to the actual path of your VERSION file

            bump_version = BumpVersion()
            bump_version.read_version_from_file()
            bump_version.info()

        elif arguments.set:

            bump_version = BumpVersion()
            bump_version.read_version_from_file()
            bump_version.info()
            new_version = arguments.version

            if bump_version.verify_version_format(new_version):
                bump_version.update_version(new_version)
                bump_version.read_version_from_file()
                bump_version.info()

                package = bump_version.read_package_name_from_setup().replace("-", "/")

                # Update version in bumpversion/{package}/__init__.py
                init_file_path = f"{package}/__init__.py"  # Change this to the actual path of your __init__.py file
                bump_version.update_version_in_file(init_file_path, new_version, version_variable="__version__")

                # Example 2: Update version in bumpversion/version.py
                version_file_path = f"{package}/__version__.py"  # Change this to the actual path of your version.py file
                bump_version.update_version_in_file(version_file_path, new_version, version_variable="version")


                bump_version.read_version_from_file()
                bump_version.info()
            else:
                print("Invalid version format. Please provide a version in X.X.X format with integer components.")

        elif arguments.config:

            bump_version = BumpVersion()
            bump_version.info()
            new_version = arguments.version

            bump_version.change_files(new_version)

            print ("AAA")


        return ""
