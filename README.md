Versioner
=========
Automatic or manual versioning with git hooks.

Install
-------
Clone and run
```sh
sudo ./versioner-install
```

to install versioner on your system.

To install for specific git repo run
```sh
versioner-install
```
And follow questions. Set the file where the version is stored and what versioning you want [manual, automatic].
Automatic for now automatically upgrades maintanence part of version (the third number 1.2.3.4).

Usage
-----
I personally preffer to create an alias for script versioner-update (in my case simply vu).
* To get the current version
```sh
versioner-update
```
* Upgrade major (minor, maintanence, build) version
```sh
versioner-update --major
versioner-update --minor
versioner-update --main
versioner-update --build
```

If automatic is picked, then maintanence version is always upgraded before commit.
For manual, you have to manually upgrade.
Version number will be prefixed to each commit message, and on each upgrade a new tag with summary since last version is created.
