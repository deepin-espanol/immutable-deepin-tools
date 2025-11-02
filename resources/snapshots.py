import os
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, 
                              QPushButton, QListWidget, QListWidgetItem, 
                              QInputDialog, QLineEdit, QLabel, QFrame,
                              QMessageBox, QDialog, QDialogButtonBox)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QCoreApplication, QTranslator

class SnapshotInfoDialog(QDialog):
    def __init__(self, parent=None, snapshot_info=None):
        super().__init__(parent)
        self.parent = parent
        self.snapshot_info = snapshot_info or {}
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 450)  # Aumenté la altura para dar más espacio al botón
        self.setup_ui()

    def setup_ui(self):
        # Widget principal con bordes redondeados
        main_widget = QWidget()
        main_widget.setObjectName("info_dialog")
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Título
        title_label = QLabel(self.tr("Información del Snapshot"))
        title_label.setObjectName("dialog_title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel#dialog_title {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: transparent;
            }
        """)
        layout.addWidget(title_label)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedHeight(2)
        layout.addWidget(separator)

        # Información del snapshot - Contenedor principal
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(15)

        # Nombre
        name_container = QWidget()
        name_layout = QHBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QLabel(self.tr("Nombre:"))
        name_label.setObjectName("field_label")
        name_label.setFixedWidth(120)
        self.name_value = QLabel(self.snapshot_info.get('name', 'N/A'))
        self.name_value.setObjectName("field_value")
        self.name_value.setWordWrap(True)
        self.name_value.setMinimumHeight(25)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_value)
        info_layout.addWidget(name_container)

        # ID
        id_container = QWidget()
        id_layout = QHBoxLayout(id_container)
        id_layout.setContentsMargins(0, 0, 0, 0)
        id_label = QLabel(self.tr("ID del respaldo:"))
        id_label.setObjectName("field_label")
        id_label.setFixedWidth(120)
        self.id_value = QLabel(self.snapshot_info.get('id', 'N/A'))
        self.id_value.setObjectName("field_value")
        self.id_value.setWordWrap(True)
        self.id_value.setMinimumHeight(25)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_value)
        info_layout.addWidget(id_container)

        # Fecha
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_label = QLabel(self.tr("Fecha:"))
        date_label.setObjectName("field_label")
        date_label.setFixedWidth(120)
        self.date_value = QLabel(self.snapshot_info.get('time', 'N/A'))
        self.date_value.setObjectName("field_value")
        self.date_value.setWordWrap(True)
        self.date_value.setMinimumHeight(25)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_value)
        info_layout.addWidget(date_container)

        # Descripción
        desc_container = QWidget()
        desc_layout = QVBoxLayout(desc_container)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(5)
        desc_label = QLabel(self.tr("Descripción:"))
        desc_label.setObjectName("field_label")
        self.desc_value = QLabel(self.snapshot_info.get('desc', 'N/A'))
        self.desc_value.setObjectName("field_value")
        self.desc_value.setWordWrap(True)
        self.desc_value.setMinimumHeight(60)
        self.desc_value.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_value)
        info_layout.addWidget(desc_container)

        # Espaciador para empujar el botón hacia abajo
        info_layout.addStretch(1)

        layout.addWidget(info_container, 1)  # El 1 hace que ocupe todo el espacio disponible

        # Botón de cerrar - ahora con más margen superior
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Margen superior de 20px
        button_layout.addStretch(1)
        
        self.close_button = QPushButton(self.tr("Cerrar"))  # Texto correcto
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(100, 49)
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        button_layout.addStretch(1)
        
        layout.addWidget(button_container)

        # Layout principal del diálogo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_widget)

        # Aplicar estilos según el tema del parent
        self.apply_theme()

    def apply_theme(self):
        # Obtener el tema del parent principal (MainWindow)
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'dark_mode'):
            dark_mode = self.parent.parent.dark_mode
        elif hasattr(self.parent, 'dark_mode'):
            dark_mode = self.parent.dark_mode
        else:
            dark_mode = True  # Por defecto oscuro
        
        if dark_mode:
            stylesheet = """
                #info_dialog {
                    background-color: #3A3A3A;
                    border: 1px solid #555555;
                    border-radius: 8px;
                }
                #dialog_title {
                    color: #FFFFFF;
                    background-color: transparent;
                }
                #field_label {
                    font-weight: bold;
                    color: #BEBEBE;
                    font-size: 13px;
                    background-color: transparent;
                }
                #field_value {
                    color: #E0E0E0;
                    font-size: 13px;
                    background-color: #2D2D2D;
                    padding: 6px 10px;
                    border-radius: 4px;
                    border: 1px solid #444444;
                }
                #close_button {
                    background-color: #2ca7f8;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: bold;
                }
                #close_button:hover {
                    background-color: #1d8dd8;
                }
                #close_button:pressed {
                    background-color: #0a70b9;
                }
                QFrame {
                    background-color: #555555;
                }
            """
        else:
            stylesheet = """
                #info_dialog {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                }
                #dialog_title {
                    color: #333333;
                    background-color: transparent;
                }
                #field_label {
                    font-weight: bold;
                    color: #333333;
                    font-size: 13px;
                    background-color: transparent;
                }
                #field_value {
                    color: #333333;
                    font-size: 13px;
                    background-color: #F8F8F8;
                    padding: 6px 10px;
                    border-radius: 4px;
                    border: 1px solid #E0E0E0;
                }
                #close_button {
                    background-color: #2ca7f8;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: bold;
                }
                #close_button:hover {
                    background-color: #1d8dd8;
                }
                #close_button:pressed {
                    background-color: #0a70b9;
                }
                QFrame {
                    background-color: #E0E0E0;
                }
            """
        
        self.setStyleSheet(stylesheet)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

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
        snapshot_action_buttons_layout.setSpacing(5)  # Reducir espaciado entre botones

        self.btn_create = QPushButton(self.tr("Crear"))
        self.btn_create.setObjectName("btn_create_snapshot")
        snapshot_action_buttons_layout.addWidget(self.btn_create)

        self.btn_delete = QPushButton(self.tr("Eliminar"))
        self.btn_delete.setObjectName("btn_delete_snapshot")
        self.btn_delete.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_delete)

        # Configurar botón mostrar con icono - TAMAÑO FIJADO
        self.btn_show = QPushButton()
        self.btn_show.setObjectName("btn_show_snapshot")
        self.btn_show.setToolTip(self.tr("Mostrar Información del Snapshot"))
        self.btn_show.setEnabled(False)
        self.btn_show.setFixedSize(32, 32)  # Tamaño fijo pequeño
        
        btn_show_layout = QHBoxLayout(self.btn_show)
        btn_show_layout.setContentsMargins(2, 2, 2, 2)  # Márgenes mínimos
        btn_show_layout.setSpacing(2)

        icon_show = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-info-snapshot.png")
        if os.path.exists(icon_path):
            icon_show.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_show.setPixmap(QIcon.fromTheme("dialog-information").pixmap(icon_size, icon_size))
        btn_show_layout.addWidget(icon_show)
        
        snapshot_action_buttons_layout.addWidget(self.btn_show)

        # Configurar botón modificar con icono - TAMAÑO FIJADO
        self.btn_modify = QPushButton()
        self.btn_modify.setObjectName("btn_modify_snapshot")
        self.btn_modify.setToolTip(self.tr("Modificar Snapshot"))
        self.btn_modify.setEnabled(False)
        self.btn_modify.setFixedSize(32, 32)  # Tamaño fijo pequeño
        
        btn_modify_layout = QHBoxLayout(self.btn_modify)
        btn_modify_layout.setContentsMargins(2, 2, 2, 2)  # Márgenes mínimos
        btn_modify_layout.setSpacing(2)
        
        icon_modify = QLabel()
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-modify-snapshot.png")
        if os.path.exists(icon_path):
            icon_modify.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_modify.setPixmap(QIcon.fromTheme("document-edit").pixmap(icon_size, icon_size))
        btn_modify_layout.addWidget(icon_modify)
        
        snapshot_action_buttons_layout.addWidget(self.btn_modify)

        # Configurar botón refrescar con icono - TAMAÑO FIJADO
        self.btn_refresh = QPushButton()
        self.btn_refresh.setObjectName("btn_refresh_list")
        self.btn_refresh.setToolTip(self.tr("Refrescar Lista de Snapshots"))
        self.btn_refresh.setFixedSize(32, 32)  # Tamaño fijo pequeño
        
        btn_refresh_layout = QHBoxLayout(self.btn_refresh)
        btn_refresh_layout.setContentsMargins(2, 2, 2, 2)  # Márgenes mínimos
        btn_refresh_layout.setSpacing(2)

        icon_refresh = QLabel()
        icon_path = os.path.join(self.parent.current_dir, "resources", "btn-refresh-snapshot.png")
        if os.path.exists(icon_path):
            icon_refresh.setPixmap(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon_refresh.setPixmap(QIcon.fromTheme("view-refresh").pixmap(icon_size, icon_size))
        btn_refresh_layout.addWidget(icon_refresh)
        
        snapshot_action_buttons_layout.addWidget(self.btn_refresh)

        # Añadir espaciador para empujar los botones a la izquierda
        snapshot_action_buttons_layout.addStretch(1)

        # Estilos CSS para los botones - AÑADIR ESTILOS ESPECÍFICOS PARA BOTONES PEQUEÑOS
        button_style = """
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
            /* Estilos específicos para botones pequeños con iconos */
            #btn_show_snapshot, #btn_modify_snapshot, #btn_refresh_list {
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
                margin: 0px;
            }
        """
        
        self.btn_delete.setStyleSheet(button_style)
        self.btn_create.setStyleSheet(button_style)
        self.btn_show.setStyleSheet(button_style)
        self.btn_modify.setStyleSheet(button_style)
        self.btn_refresh.setStyleSheet(button_style)

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

        # --- INICIO DE LA MODIFICACIÓN ---
        # Definir los estilos del enlace
        link_style = "style='color:#2ECC71; text-decoration:none;'"
        hover_style = ("onmouseover=\"this.style.color='#27AE60'; this.style.textDecoration='underline'\" "
                     "onmouseout=\"this.style.color='#2ECC71'; this.style.textDecoration='none'\"")

        # Aplicar los estilos al HTML del enlace
        info_link_text = self.tr(
            '<a href="https://xn--deepinenespaol-1nb.org/noticias/solido-como-acceder-a-root-en-v25/" {0} {1}>Más información</a>'
        ).format(link_style, hover_style)
        
        info_link = QLabel(info_link_text)
        info_link.setOpenExternalLinks(True)
        revert_layout.addWidget(info_link)
        # --- FIN DE LA MODIFICACIÓN ---

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

    def get_selected_snapshot_info(self):
        """Obtiene información detallada del snapshot seleccionado"""
        snapshot_id = self.get_selected_snapshot_id()
        if not snapshot_id:
            return None

        output = self.controller.execute_command(
            f'deepin-immutable-ctl snapshot show "{snapshot_id}"',
            show_in_console=False
        )

        # Parsear la información del snapshot
        snapshot_info = {'id': snapshot_id}
        lines = output.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if key == 'ID':
                    snapshot_info['id'] = value
                elif key == 'Name':
                    snapshot_info['name'] = value
                elif key == 'Time':
                    snapshot_info['time'] = value
                elif key == 'Desc':
                    snapshot_info['desc'] = value

        return snapshot_info

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
                command,
                requires_reboot=False
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
                    " ".join(command_parts),
                    requires_reboot=False
                )
            dialog.accept()
        
        ok_button.clicked.connect(modify_snapshot)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

    def show_snapshot_info(self):
        snapshot_info = self.get_selected_snapshot_info()
        if snapshot_info:
            dialog = SnapshotInfoDialog(self, snapshot_info)
            dialog.exec()
        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("No se pudo obtener la información del snapshot"))

    def confirm_delete_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                self.tr("Confirmar Eliminación"),
                self.tr("¿Eliminar snapshot {}?").format(snapshot_id),
                f'pkexec deepin-immutable-ctl snapshot delete "{snapshot_id}"',
                requires_reboot=False
            )

    def confirm_revert_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                self.tr("Confirmar Reversión"),
                self.tr("¡ADVERTENCIA! Revertir a {} es irreversible. Esta acción requerirá un reinicio inmediato del sistema.").format(snapshot_id),
                f'pkexec deepin-immutable-ctl snapshot rollback "{snapshot_id}"',
                requires_reboot=True
            )