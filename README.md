# Simple automatic versioning hooked to pre-commit in git

This will automatically control the version of a project, by incrementing maintanence version with each commit.

The script expects a "main file" to contain version. This text is searched and automatically incremented.  
Manually can be used to increment major and minor version.

TODO: added automatic increment for build version in jenkins.

Usage:
    
   Clone this repo and run as sudo ./versioner-install
   This will copy required files to /usr/local/bin.

   For each project you want to control the version, run versioner-install from it's directory. That will copy pre-commit script to .git/hooks. !! There is no check if pre-commit already exists !!

   For manual increment run version-update 'file' with --major --minor --maintanence or --build.


This can automatically control python, c++ and haskell projects.
For python, it will search for text: version = "x.y.z.a".
For c++: string version = "x.y.z.a".
For haskell it expects cabal file and text: version: x.y.z.a.
