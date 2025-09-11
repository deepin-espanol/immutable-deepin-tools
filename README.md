# immutable-deepin-tools
Unofficial application for manipulating the immutability of Deepin Linux 25.

<img width="1012" height="648" alt="imagen" src="https://github.com/user-attachments/assets/523a270e-bf39-4db1-b1af-285616a327cc" />

## List of options:
Manipulate files using parameters.
Run commands without disabling immutability.
Manage system backups.
Deploy, revert, and apply changes to the Ostree system.

Available languages:
 -   Chinese
 -   Portuguese
 -   Spanish
 -   English

Compile binary:
pyinstaller --onefile --windowed --add-data "resources:resources" --hidden-import "PySide6.QtCore" --hidden-import "PySide6.QtGui" --hidden-import "PySide6.QtWidgets" main.py

Compile Deb package:
1. Create release file.

dch --create -D stable --package "immutable-deepin-tools" --newversion=1.x.x "New release."

2. Compilation Dependencies:

sudo apt build-dep .

3. Compile Package:

dpkg-buildpackage -Zxz -rfakeroot -b


### Warning: The quality of this product is not guaranteed. If you encounter any problems, please report them.

Using the MIT license.
