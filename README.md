# immutable-deepin-tools
Unofficial application for manipulating the immutability of Deepin Linux 25.

<img width="1053" height="600" alt="imagen" src="https://github.com/user-attachments/assets/9cb90a0e-1cc3-474a-a6b5-1a16702ac6e9" />

**List of options:**
Manipulate files using parameters.
Run commands without disabling immutability.
Manage system backups.
Deploy, revert, and apply changes to the Ostree system.

**Compile binary:**
pyinstaller --onefile --windowed --add-data "resources:resources" --hidden-import "PySide6.QtCore" --hidden-import "PySide6.QtGui" --hidden-import "PySide6.QtWidgets" main.py

Warning: Product quality is not guaranteed. If you encounter any problems, please report them.

**Under the MIT license.**
