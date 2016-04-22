OCE Release Guide
-----------------

How to release a new version of OCE:

1. Increase the version and build number accordingly in oce.py.
2. Make sure everything you want to release is pushed to git.
3. Create a new tag on the git repository with the new version number.
4. Clone a new copy of the repository in another directory and switch to the new tag.
5. Install PyInstaller into the same python environment as you develop OCE in.
   (pip install pyinstaller)
6. Open a terminal in your OCE development folder and activate your python environment.
7. Run the following command: "pyinstaller oce.spec" to generate the executables from the specifications file.
This will create two directories, "build" and "dist". "build" is a temporary directory for build files. "dist" is the output dir.
In the "dist" directory you will find directories for the normal version of OCE and the portable version.
8. Test the application by running oce in each of the directories in "dist"
9. Zip both of the versions of the application and name them "OCE_<OS>_vx.x" for the normal build and "OCE_<OS>_Portable_vx.x" for the portable build, where <OS> is the operating system the build is for (e.g. Linux), and vx.x is the version (e.g. v1.1b4)
10. Upload the archives as releases to the repository
