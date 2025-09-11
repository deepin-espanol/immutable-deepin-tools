import os
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, 
                              QPushButton, QListWidget, QListWidgetItem, 
                              QInputDialog, QLineEdit, QLabel, QFrame,
                              QMessageBox, QDialog, QDialogButtonBox)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QCoreApplication, QTranslator

class SnapshotsTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_ui()
        self.connect_signals()
        self.refresh_snapshots()

    def tr(self, text):
        """Método wrapper para traducciones"""
        return QCoreApplication.translate("SnapshotsTab", text)

    def setup_ui(self):
        snapshot_main_layout = QHBoxLayout(self)
        snapshot_main_layout.setContentsMargins(20, 20, 20, 20)
        snapshot_main_layout.setSpacing(15)

        # Lista de snapshots
        snapshot_list_container = QGroupBox(self.tr("Gestión de Snapshots"))
        snapshot_list_layout = QVBoxLayout(snapshot_list_container)

        self.snapshot_list = QListWidget()
        snapshot_list_layout.addWidget(self.snapshot_list)

        # Botones de acciones
        snapshot_action_buttons_layout = QHBoxLayout()
        snapshot_action_buttons_layout.setSpacing(10)

        self.btn_create = QPushButton(self.tr("Crear"))
        self.btn_create.setObjectName("btn_create_snapshot")
        snapshot_action_buttons_layout.addWidget(self.btn_create)

        self.btn_delete = QPushButton(self.tr("Eliminar"))
        self.btn_delete.setObjectName("btn_delete_snapshot")
        self.btn_delete.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_delete)

        # Configurar botón mostrar con icono (usando QPixmap)
        self.btn_show = QPushButton()
        self.btn_show.setObjectName("btn_show_snapshot")
        self.btn_show.setToolTip(self.tr("Mostrar Información del Snapshot"))
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
        self.btn_modify.setToolTip(self.tr("Modificar Snapshot"))
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
        self.btn_refresh.setToolTip(self.tr("Refrescar Lista de Snapshots"))
        
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

        # Estilos CSS (sin cambios ya que no contienen texto)
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
        revert_group = QGroupBox(self.tr("Revertir Sistema a Snapshot"))
        revert_layout = QVBoxLayout(revert_group)

        self.btn_revert = QPushButton(self.tr("Revertir Ahora"))
        self.btn_revert.setEnabled(False)
        revert_layout.addWidget(self.btn_revert, alignment=Qt.AlignCenter)

        revert_explanation = QLabel(self.tr(
            "Revertir el sistema a un snapshot restaurará el estado del sistema al momento en que se creó ese snapshot. "
            "Esto eliminará permanentemente todos los cambios realizados posteriormente. "
            "Esta operación es irreversible y requerirá un reinicio inmediato del equipo."
        ))
        revert_explanation.setWordWrap(True)
        revert_layout.addWidget(revert_explanation)

        info_link_text = self.tr('<a href="https://xn--deepinenespaol-1nb.org/noticias/solido-como-acceder-a-root-en-v25/">Más información</a>')
        info_link = QLabel(info_link_text)
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
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Crear Snapshot"))
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Campo para el nombre
        name_label = QLabel(self.tr("Introduce un nombre para el snapshot (opcional):"))
        layout.addWidget(name_label)
        
        name_edit = QLineEdit()
        layout.addWidget(name_edit)
        
        # Campo para la descripción
        desc_label = QLabel(self.tr("Introduce una descripción (opcional):"))
        layout.addWidget(desc_label)
        
        desc_edit = QLineEdit()
        layout.addWidget(desc_edit)
        
        # Botones - con layout horizontal para separarlos
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        cancel_button = QPushButton(self.tr("Cancelar"))
        create_button = QPushButton(self.tr("Crear"))
        
        button_layout.addWidget(cancel_button, 0, Qt.AlignLeft)
        button_layout.addStretch(1)  # Espaciador para separar los botones
        button_layout.addWidget(create_button, 0, Qt.AlignRight)
        
        layout.addWidget(button_container)
        
        # Conectar señales
        def create_snapshot():
            name = name_edit.text().strip()
            description = desc_edit.text().strip()
            
            command = "pkexec deepin-immutable-ctl snapshot create"
            if name:
                command += f' "{name}"'
            if description:
                command += f' "{description}"'
            
            self.confirm_action(
                self.tr("Confirmar Creación de Snapshot"),
                self.tr("¿Está seguro que desea crear un snapshot con nombre '{}'?").format(name if name else self.tr("sin nombre")),
                command
            )
            dialog.accept()
        
        create_button.clicked.connect(create_snapshot)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

    def show_modify_snapshot_dialog(self):
        snapshot_id = self.get_selected_snapshot_id()
        if not snapshot_id:
            QMessageBox.warning(self, self.tr("Advertencia"), self.tr("Selecciona un snapshot primero"))
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Modificar Snapshot"))
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Campo para el nombre
        name_label = QLabel(self.tr("Nuevo nombre para {} (dejar en blanco para no cambiar):").format(snapshot_id))
        layout.addWidget(name_label)
        
        name_edit = QLineEdit()
        layout.addWidget(name_edit)
        
        # Campo para la descripción
        desc_label = QLabel(self.tr("Nueva descripción para {}:").format(snapshot_id))
        layout.addWidget(desc_label)
        
        desc_edit = QLineEdit()
        layout.addWidget(desc_edit)
        
        # Botones
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(self.tr("Modificar"), QDialogButtonBox.AcceptRole)
        cancel_button = button_box.addButton(self.tr("Cancelar"), QDialogButtonBox.RejectRole)
        layout.addWidget(button_box)
        
        # Conectar señales
        def modify_snapshot():
            name = name_edit.text().strip()
            description = desc_edit.text().strip()
            
            command_parts = [f'pkexec deepin-immutable-ctl snapshot modify "{snapshot_id}"']
            if name:
                command_parts.append(f'"{name}"')
            if description:
                command_parts.append(f'"{description}"')

            if len(command_parts) > 1:
                self.confirm_action(
                    self.tr("Confirmar Modificación"),
                    self.tr("¿Modificar snapshot {}?").format(snapshot_id),
                    " ".join(command_parts)
                )
            dialog.accept()
        
        ok_button.clicked.connect(modify_snapshot)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

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
                self.tr("Confirmar Eliminación"),
                self.tr("¿Eliminar snapshot {}?").format(snapshot_id),
                f'pkexec deepin-immutable-ctl snapshot delete "{snapshot_id}"'
            )

    def confirm_revert_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                self.tr("Confirmar Reversión"),
                self.tr("¡ADVERTENCIA! Revertir a {} es irreversible").format(snapshot_id),
                f'pkexec deepin-immutable-ctl snapshot rollback "{snapshot_id}"',
                requires_reboot=True
            )