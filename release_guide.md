`OCE Release Guide
-----------------

How to release a new version of OCE:

1. Increase the version and build number accordingly in oce.py.
2. Make sure everything you want to release is pushed to git.
3. Create a new tag on the git repository with the new version number.
4. Clone a new copy of the repository in another directory and switch to the new tag.
5. Install PyInstaller into the same python environment as you develop OCE in.
   (pip install pyinstaller)
6. Open a terminal in your OCE development folder and activate your python environment.
7. Run the following command: "pyinstaller oce.py" to generate the executable.
8. Copy over some resources to the new build:
logging.conf to build/oce/logging.conf
icons folder to build/oce/icons
9. Test the application by running oce in the build/oce directory