import os
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, 
                              QPushButton, QListWidget, QListWidgetItem, 
                              QInputDialog, QLineEdit, QLabel, QFrame,
                              QMessageBox)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

class SnapshotsTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_ui()
        self.connect_signals()
        self.refresh_snapshots()

    def setup_ui(self):
        snapshot_main_layout = QHBoxLayout(self)
        snapshot_main_layout.setContentsMargins(20, 20, 20, 20)
        snapshot_main_layout.setSpacing(15)

        # Lista de snapshots
        snapshot_list_container = QGroupBox("Gestión de Snapshots")
        snapshot_list_layout = QVBoxLayout(snapshot_list_container)

        self.snapshot_list = QListWidget()
        snapshot_list_layout.addWidget(self.snapshot_list)

        # Botones de acciones
        snapshot_action_buttons_layout = QHBoxLayout()
        snapshot_action_buttons_layout.setSpacing(10)

        self.btn_create = QPushButton("Crear")
        self.btn_create.setObjectName("btn_create_snapshot")
        snapshot_action_buttons_layout.addWidget(self.btn_create)

        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.setObjectName("btn_delete_snapshot")
        self.btn_delete.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_delete)

        # Configurar botón mostrar con icono (usando QPixmap)
        self.btn_show = QPushButton()
        self.btn_show.setObjectName("btn_show_snapshot")
        self.btn_show.setToolTip("Mostrar Información del Snapshot")
        self.btn_show.setEnabled(False)
        
        btn_show_layout = QHBoxLayout(self.btn_show)
        btn_show_layout.setContentsMargins(5, 5, 5, 5)
        btn_show_layout.setSpacing(5)

        icon_show = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-info-snapshot.png")
        if os.path.exists(icon_path):
            icon_show.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_show.setPixmap(QIcon.fromTheme("dialog-information").pixmap(icon_size, icon_size))
        btn_show_layout.addWidget(icon_show)
        
        snapshot_action_buttons_layout.addWidget(self.btn_show)

        # Configurar botón modificar con icono (usando QPixmap)
        self.btn_modify = QPushButton()
        self.btn_modify.setObjectName("btn_modify_snapshot")
        self.btn_modify.setToolTip("Modificar Snapshot")
        self.btn_modify.setEnabled(False)
        
        btn_modify_layout = QHBoxLayout(self.btn_modify)
        btn_modify_layout.setContentsMargins(5, 5, 5, 5)
        btn_modify_layout.setSpacing(5)
        
        icon_modify = QLabel()
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-modify-snapshot.png")
        if os.path.exists(icon_path):
            icon_modify.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_modify.setPixmap(QIcon.fromTheme("document-edit").pixmap(icon_size, icon_size))
        btn_modify_layout.addWidget(icon_modify)
        
        snapshot_action_buttons_layout.addWidget(self.btn_modify)

        # Configurar botón refrescar con icono (usando QPixmap)
        self.btn_refresh = QPushButton()
        self.btn_refresh.setObjectName("btn_refresh_list")
        self.btn_refresh.setToolTip("Refrescar Lista de Snapshots")
        
        btn_refresh_layout = QHBoxLayout(self.btn_refresh)
        btn_refresh_layout.setContentsMargins(5, 5, 5, 5)
        btn_refresh_layout.setSpacing(5)

        icon_refresh = QLabel()
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-refresh-snapshot.png")
        if os.path.exists(icon_path):
            icon_refresh.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_refresh.setPixmap(QIcon.fromTheme("view-refresh").pixmap(icon_size, icon_size))
        btn_refresh_layout.addWidget(icon_refresh)
        
        snapshot_action_buttons_layout.addWidget(self.btn_refresh)

        self.btn_delete.setStyleSheet("""
            QPushButton:hover {
                background-color: #1d8dd8;
            }
            QPushButton:pressed {
                background-color: #0a70b9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #777777;
            }
        """)

        self.btn_create.setStyleSheet("""
            QPushButton:hover {
                background-color: #1d8dd8;
            }
            QPushButton:pressed {
                background-color: #0a70b9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #777777;
            }
        """)

        self.btn_show.setStyleSheet("""
            QPushButton {
                min-width: 11px;
                max-width: 11px;
            }
            QPushButton:hover {
                background-color: #1d8dd8;
            }
            QPushButton:pressed {
                background-color: #0a70b9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #777777;
            }
        """)

        self.btn_modify.setStyleSheet("""
            QPushButton {
                min-width: 11px;
                max-width: 11px;
            }
            QPushButton:hover {
                background-color: #1d8dd8;
            }
            QPushButton:pressed {
                background-color: #0a70b9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #777777;
            }
        """)

        self.btn_refresh.setStyleSheet("""
            QPushButton {
                min-width: 11px;
                max-width: 11px;
            }
            QPushButton:hover {
                background-color: #1d8dd8;
            }
            QPushButton:pressed {
                background-color: #0a70b9;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #777777;
            }
        """)

        snapshot_list_layout.addLayout(snapshot_action_buttons_layout)
        snapshot_main_layout.addWidget(snapshot_list_container, 2)

        # Panel de revertir
        revert_group = QGroupBox("Revertir Sistema a Snapshot")
        revert_layout = QVBoxLayout(revert_group)

        self.btn_revert = QPushButton("Revertir Ahora")
        self.btn_revert.setEnabled(False)
        revert_layout.addWidget(self.btn_revert, alignment=Qt.AlignCenter)

        revert_explanation = QLabel(
            "Revertir el sistema a un snapshot restaurará el estado del sistema al momento en que se creó ese snapshot. "
            "Esto eliminará permanentemente todos los cambios realizados posteriormente. "
            "Esta operación es irreversible y requerirá un reinicio inmediato del equipo."
        )
        revert_explanation.setWordWrap(True)
        revert_layout.addWidget(revert_explanation)

        info_link = QLabel('<a href="https://xn--deepinenespaol-1nb.org/noticias/solido-como-acceder-a-root-en-v25/">Más información</a>')
        info_link.setOpenExternalLinks(True)
        revert_layout.addWidget(info_link)

        revert_group.setMinimumWidth(280)
        snapshot_main_layout.addWidget(revert_group, 1)

    def connect_signals(self):
        self.snapshot_list.itemSelectionChanged.connect(self.enable_snapshot_buttons)
        self.btn_create.clicked.connect(self.show_create_snapshot_dialog)
        self.btn_delete.clicked.connect(self.confirm_delete_snapshot)
        self.btn_show.clicked.connect(self.show_snapshot_info)
        self.btn_modify.clicked.connect(self.show_modify_snapshot_dialog)
        self.btn_refresh.clicked.connect(self.refresh_snapshots)
        self.btn_revert.clicked.connect(self.confirm_revert_snapshot)

    def refresh_snapshots(self):
        self.snapshot_list.clear()
        output = self.controller.execute_command(
            "deepin-immutable-ctl snapshot list", 
            show_in_console=False
        )

        lines = output.split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        snapshot_id = parts[0]
                        name = parts[1]
                        time = ' '.join(parts[2:4])
                        desc = ' '.join(parts[4:]) if len(parts) > 4 else ''
                        item_text = f"{name} ({snapshot_id})\n{time} - {desc}"
                        self.snapshot_list.addItem(item_text)
        self.enable_snapshot_buttons()

    def get_selected_snapshot_id(self):
        current_item = self.snapshot_list.currentItem()
        if current_item:
            text = current_item.text()
            start = text.find("(") + 1
            end = text.find(")")
            if start > 0 and end > start:
                return text[start:end]
        return None

    def enable_snapshot_buttons(self):
        selected = self.snapshot_list.currentItem() is not None
        self.btn_delete.setEnabled(selected)
        self.btn_show.setEnabled(selected)
        self.btn_modify.setEnabled(selected)
        self.btn_revert.setEnabled(selected)

    def confirm_action(self, title, message, command, show_console=True, requires_reboot=False):
        """Wrapper para usar el confirm_action de la ventana principal"""
        self.parent.confirm_action(title, message, command, show_console, requires_reboot)

    def show_create_snapshot_dialog(self):
        text, ok = QInputDialog.getText(
            self, "Crear Snapshot",
            "Introduce un nombre para el snapshot (opcional):",
            QLineEdit.Normal, ""
        )
        if ok:
            description, ok_desc = QInputDialog.getText(
                self, "Crear Snapshot",
                "Introduce una descripción (opcional):",
                QLineEdit.Normal, ""
            )
            if ok_desc:
                command = "pkexec deepin-immutable-ctl snapshot create"
                if text:
                    command += f' --name="{text}"'
                if description:
                    command += f' --description="{description}"'
                
                self.confirm_action(
                    "Confirmar Creación de Snapshot",
                    f"¿Está seguro que desea crear un snapshot con nombre '{text}'?",
                    command
                )

    def show_modify_snapshot_dialog(self):
        snapshot_id = self.get_selected_snapshot_id()
        if not snapshot_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un snapshot primero")
            return

        name, ok_name = QInputDialog.getText(
            self, "Modificar Snapshot",
            f"Nuevo nombre para {snapshot_id} (dejar en blanco para no cambiar):",
            QLineEdit.Normal, ""
        )
        if ok_name:
            description, ok_desc = QInputDialog.getText(
                self, "Modificar Snapshot",
                f"Nueva descripción para {snapshot_id}:",
                QLineEdit.Normal, ""
            )
            if ok_desc:
                command_parts = [f'pkexec deepin-immutable-ctl snapshot modify "{snapshot_id}"']
                if name:
                    command_parts.append(f'--set-name="{name}"')
                if description:
                    command_parts.append(f'--set-description="{description}"')

                if len(command_parts) > 1:
                    self.confirm_action(
                        "Confirmar Modificación",
                        f"¿Modificar snapshot {snapshot_id}?",
                        " ".join(command_parts)
                    )

    def show_snapshot_info(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.controller.execute_command(
                f'deepin-immutable-ctl snapshot show "{snapshot_id}"',
                show_in_console=True
            )

    def confirm_delete_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                "Confirmar Eliminación",
                f"¿Eliminar snapshot {snapshot_id}?",
                f'pkexec deepin-immutable-ctl snapshot delete "{snapshot_id}"'
            )

    def confirm_revert_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                "Confirmar Reversión",
                f"¡ADVERTENCIA! Revertir a {snapshot_id} es irreversible",
                f'pkexec deepin-immutable-ctl snapshot rollback "{snapshot_id}"',
                requires_reboot=True
            )