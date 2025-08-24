import os
from subprocess import Popen, PIPE
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QGroupBox, QPushButton, QLabel, QMessageBox, 
                              QDialog, QSizePolicy, QLineEdit, QFormLayout, 
                              QCheckBox, QStackedWidget, QTextEdit)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize


class AdminTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        
        # Creamos el stacked widget para manejar las vistas
        self.stacked_widget = QStackedWidget()
        
        # Creamos los widgets como atributos de clase
        self.main_widget = None
        self.command_widget = None
        self.file_op_widget = None
        self.btn_deploy = None
        self.btn_finalize = None
        self.btn_rollback = None
        self.btn_exec = None
        self.btn_file_op = None
        self.cmd_input = None
        self.file_op_input = None
        
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)
        
        # Configurar el widget principal
        self.setup_main_widget()
        
        # Configurar el widget de comandos
        self.setup_command_widget()
        
        # Configurar el widget de operaciones de archivos
        self.setup_file_op_widget()
        
        # Mostrar el widget principal por defecto
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def setup_main_widget(self):
        """Configura el widget principal con los botones"""
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Sección superior: Botones principales
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.setSpacing(15)
        
        # Botón Ejecutar Comando
        self.btn_exec = self.create_modern_button(
            "Ejecutar Comando",
            "admin-run",
            "Ejecutar comandos sin la desactivación de la capa inmutable",
            "#3498db"
        )
        top_buttons_layout.addWidget(self.btn_exec, 1)
        
        # Botón Operación de Archivos
        self.btn_file_op = self.create_modern_button(
            "Manipular Archivos",
            "file-operation",
            "Realizar operaciones avanzadas en archivos",
            "#2ecc71"
        )
        top_buttons_layout.addWidget(self.btn_file_op, 1)
        
        layout.addLayout(top_buttons_layout)

        # Sección media: Acciones de despliegue
        deploy_group = QGroupBox("Opciones de Despliegue")
        deploy_layout = QGridLayout(deploy_group)
        
        # Botones de despliegue con nuevo diseño
        self.btn_deploy = self.create_small_button("Desplegar", "deploy-save", "#f39c12")
        self.btn_finalize = self.create_small_button("Finalizar", "deploy-finalize", "#e74c3c")
        self.btn_rollback = self.create_small_button("Revertir", "deploy-rollback", "#9b59b6")
        
        deploy_layout.addWidget(self.btn_deploy, 0, 0)
        deploy_layout.addWidget(self.btn_finalize, 0, 1)
        deploy_layout.addWidget(self.btn_rollback, 0, 2)
        
        # Configuración responsive
        deploy_layout.setHorizontalSpacing(10)
        deploy_layout.setVerticalSpacing(10)
        deploy_layout.setContentsMargins(15, 25, 15, 15)
        
        for i in range(3):
            deploy_layout.setColumnStretch(i, 1)
        
        layout.addWidget(deploy_group)
        layout.addStretch(1)
        
        self.stacked_widget.addWidget(self.main_widget)

    def setup_command_widget(self):
        """Configura el widget de ejecución de comandos"""
        self.command_widget = QWidget()
        layout = QVBoxLayout(self.command_widget)
        layout.setContentsMargins(20, 20, 20, 20)
            
        # Botón de volver con icono PNG desde resources
        btn_back = QPushButton()
        btn_back_layout = QHBoxLayout(btn_back)
        btn_back_layout.setContentsMargins(5, 5, 10, 5)
        btn_back_layout.setSpacing(5)
        
        # Cargar icono desde resources
        icon_path = os.path.join(self.parent.current_dir, "resources", "back-btn.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            icon_pixmap = QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            btn_back_layout.addWidget(icon_label)
        else:
            # Fallback a icono del sistema si no existe el PNG
            icon_label = QLabel()
            icon_label.setPixmap(QIcon.fromTheme("go-previous").pixmap(16, 16))
            btn_back_layout.addWidget(icon_label)

        text_label = QLabel("Volver")
        btn_back_layout.addWidget(text_label)
        
        btn_back.setStyleSheet("""
            QPushButton {
                min-width: 30px;
                font-size: 13px;
                color: #FFFFFF;
                font-weight: bold;
                text-align: center;
            }
            QPushButton QLabel {
                color: #FFFFFF;  /* Fuerza el color blanco para el texto */
            }
        """)
        btn_back.clicked.connect(self.show_main_view)
        layout.addWidget(btn_back, alignment=Qt.AlignLeft)
        
        # Descripción del proceso
        description = QLabel("""
            <p>Esta herramienta ejecutará el comando bajo <code>deepin-immutable-ctl admin exec</code>, 
            lo que permite realizar cambios temporales en el sistema inmutable.</p>
            
            <p><b>Advertencias:</b></p>
            <ul>
                <li>Manipular archivos del sistema puede causar inestabilidad</li>
                <li>Los cambios pueden perderse al reiniciar si no se consolidan</li>
                <li>Algunas operaciones pueden requerir reinicio para aplicar cambios</li>
            </ul>
            
            <p><b>Se recomienda que realice una copia de seguridad para cambios importantes.</b></p>
        """)
        description.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 15px;
            }
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Título
        title = QLabel("Ejecutar Comando (admin)")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        # Contenedor horizontal para el campo de entrada y el botón
        input_container = QHBoxLayout()
        input_container.setSpacing(10)
        
        # Campo de entrada de comandos
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Ingresa el comando ej: apt update && apt upgrade -y")
        input_container.addWidget(self.cmd_input, stretch=1)  # El campo de entrada ocupa todo el espacio disponible
        
        # Botón de ejecución con icono y texto
        btn_execute = QPushButton()
        btn_execute.setMinimumWidth(120)  # Ancho mínimo para el botón
        
        # Layout interno para el botón (icono + texto)
        btn_layout = QHBoxLayout(btn_execute)
        btn_layout.setContentsMargins(10, 5, 10, 5)
        btn_layout.setSpacing(8)
        
        # Icono de ejecución
        execute_icon = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "run-command.png")
        if os.path.exists(icon_path):
            execute_icon.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            execute_icon.setPixmap(QIcon.fromTheme("system-run").pixmap(icon_size, icon_size))
        btn_layout.addWidget(execute_icon)
        
        # Texto del botón
        execute_text = QLabel("Ejecutar")
        execute_text.setStyleSheet("font-weight: bold;")
        btn_layout.addWidget(execute_text)
        
        # Estilo del botón
        btn_execute.setStyleSheet("""
            QPushButton {
                min-width: 55px;
                font-size: 13px;
                color: #FFFFFF;
                font-weight: bold;
                text-align: center;
            }
            QPushButton QLabel {
                color: #FFFFFF;  /* Fuerza el color blanco para el texto */
            }
        """)
        btn_execute.clicked.connect(self.execute_command)
        
        input_container.addWidget(btn_execute)
        layout.addLayout(input_container)

        # Sección de comandos comunes
        common_commands_group = QGroupBox("Comandos comunes")
        common_commands_layout = QGridLayout(common_commands_group)
        
        common_commands = [
            ("ls", "ls -la"),
            ("grep", "grep"),
            ("nano", "nano"),
            ("chmod", "chmod"),
            ("chown", "chown"),
            ("apt-get update", "apt-get update -y")
        ]
        
        row, col = 0, 0
        for text, command in common_commands:
            btn = QPushButton(text)
            btn.setObjectName("common_command_button")
            btn.clicked.connect(lambda _, cmd=command: self.cmd_input.setText(cmd))
            common_commands_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addWidget(common_commands_group)
        
        self.stacked_widget.addWidget(self.command_widget)

    def setup_file_op_widget(self):
        """Configura el widget de operaciones de archivos"""
        self.file_op_widget = QWidget()
        layout = QVBoxLayout(self.file_op_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Botón de volver (igual que antes)
        btn_back = QPushButton()
        btn_back_layout = QHBoxLayout(btn_back)
        btn_back_layout.setContentsMargins(5, 5, 10, 5)
        btn_back_layout.setSpacing(5)
        
        icon_path = os.path.join(self.parent.current_dir, "resources", "back-btn.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            icon_pixmap = QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            btn_back_layout.addWidget(icon_label)
        else:
            icon_label = QLabel()
            icon_label.setPixmap(QIcon.fromTheme("go-previous").pixmap(16, 16))
            btn_back_layout.addWidget(icon_label)

        text_label = QLabel("Volver")
        btn_back_layout.addWidget(text_label)
        
        btn_back.setStyleSheet("""
            QPushButton {
                min-width: 30px;
                font-size: 13px;
                color: #FFFFFF;
                font-weight: bold;
                text-align: center;
            }
            QPushButton QLabel {
                color: #FFFFFF;
            }
        """)
        btn_back.clicked.connect(self.show_main_view)
        layout.addWidget(btn_back, alignment=Qt.AlignLeft)
        
        # Descripción del proceso (igual que antes)
        description = QLabel("""
            <p>Esta herramienta permite realizar operaciones en archivos del sistema 
            usando <code>deepin-immutable-ctl admin file-op</code>.</p>
            
            <p><b>Operaciones disponibles:</b></p>
            <ul>
                <li><b>setxattr</b>: Establecer atributos extendidos (ej: setxattr /ruta/al/archivo user.key=value)</li>
                <li><b>rmxattr</b>: Eliminar atributos extendidos (ej: rmxattr /ruta/al/archivo user.key)</li>
                <li><b>chattr</b>: Cambiar atributos de archivo (ej: chattr /ruta/al/archivo +i)</li>
                <li><b>chown</b>: Cambiar propietario/grupo (ej: chown /ruta/al/archivo usuario:grupo)</li>
                <li><b>chmod</b>: Cambiar permisos (ej: chmod /ruta/al/archivo 755)</li>
            </ul>
            
            <p><b>⚠️ Advertencia:</b> Estas operaciones afectan directamente al sistema de archivos.</p>
        """)
        description.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 15px;
                padding: 10px;
            }
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Título
        title = QLabel("Operaciones de Archivos")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        # Contenedor horizontal para el campo de entrada y el botón
        input_container = QHBoxLayout()
        input_container.setSpacing(10)
        
        # Campo de entrada para la operación
        self.file_op_input = QLineEdit()
        self.file_op_input.setPlaceholderText("Ingrese la operación de archivo (ej: setxattr /ruta/al/archivo user.key=value)")
        input_container.addWidget(self.file_op_input, stretch=1)  # El campo de entrada ocupa todo el espacio disponible
        
        # Botón de ejecución con icono y texto (igual que en comandos)
        btn_execute = QPushButton()
        btn_execute.setMinimumWidth(120)  # Ancho mínimo para el botón
        
        # Layout interno para el botón (icono + texto)
        btn_layout = QHBoxLayout(btn_execute)
        btn_layout.setContentsMargins(10, 5, 10, 5)
        btn_layout.setSpacing(8)
        
        # Icono de ejecución
        execute_icon = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "run-command.png")
        if os.path.exists(icon_path):
            execute_icon.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            execute_icon.setPixmap(QIcon.fromTheme("system-run").pixmap(icon_size, icon_size))
        btn_layout.addWidget(execute_icon)
        
        # Texto del botón
        execute_text = QLabel("Ejecutar")
        execute_text.setStyleSheet("font-weight: bold;")
        btn_layout.addWidget(execute_text)
        
        # Estilo del botón (igual que en comandos)
        btn_execute.setStyleSheet("""
            QPushButton {
                min-width: 55px;
                font-size: 13px;
                color: #FFFFFF;
                font-weight: bold;
                text-align: center;
                background-color: #2ecc71;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
            QPushButton QLabel {
                color: #FFFFFF;
            }
        """)
        btn_execute.clicked.connect(self.execute_file_op)
        
        input_container.addWidget(btn_execute)
        layout.addLayout(input_container)

        # Ejemplos de comandos
        examples_group = QGroupBox("Ejemplos de Operaciones")
        examples_layout = QVBoxLayout(examples_group)
        
        examples = [
            ("Cambiar atributos", "chattr /ruta/al/archivo +i"),
            ("Eliminar atributos", "rmxattr /ruta/al/archivo user.key"),
            ("Establecer atributos", "setxattr /ruta/al/archivo user.key=value"),
        ]
        
        for desc, cmd in examples:
            example_btn = QPushButton(f"{desc}: {cmd}")
            example_btn.setStyleSheet("""
                QPushButton {
                    min-width: 55px;
                    font-size: 13px;
                    color: #FFFFFF;
                    font-weight: bold;
                    text-align: center;
                    background-color: #E74C3C;
                    color: white;
                }
                QPushButton:hover { background-color: #C0392B; }
                QPushButton:pressed { background-color: #A93226; }
                QPushButton:disabled { background-color: #555555; color: #777777; }
                QPushButton QLabel {
                    color: #FFFFFF;  /* Fuerza el color blanco para el texto */
                }
            """)
            example_btn.clicked.connect(lambda _, c=cmd: self.file_op_input.setText(c))
            examples_layout.addWidget(example_btn)
        
        layout.addWidget(examples_group)
        layout.addStretch(1)
        
        self.stacked_widget.addWidget(self.file_op_widget)

    def create_modern_button(self, text, icon_name, tooltip, color):
        """Crea un botón cuadrado grande con icono y texto"""
        btn = QPushButton()
        btn.setMinimumSize(160, 160)  # Tamaño mínimo cuadrado
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setToolTip(tooltip)
        
        # Layout interno vertical
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)
        
        # Icono
        icon_label = QLabel()
        icon_size = 48  # Tamaño del icono
        
        # Buscar icono en recursos primero
        icon_path = os.path.join(self.parent.current_dir, "resources", f"{icon_name}.png")
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            icon_label.setPixmap(QIcon.fromTheme(icon_name).pixmap(icon_size, icon_size))
        
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Texto principal
        title_label = QLabel(text)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 14px;
                color: {color};
                margin-top: 5px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel(tooltip)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #777;
                margin-top: 5px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Estilo del botón
        btn.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {color};
                border-radius: 15px;
                background-color: rgba({color[1:]}, 0.1);
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba({color[1:]}, 0.2);
                border: 2px solid {color};
            }}
            QPushButton:pressed {{
                background-color: rgba({color[1:]}, 0.3);
            }}
        """)
        
        return btn

    def create_small_button(self, text, icon_name, color):
        """Crea un botón con icono, texto y descripción para las opciones de deploy"""
        btn = QPushButton()
        btn.setMinimumHeight(80)  # Aumentamos la altura para acomodar más contenido
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Layout interno vertical
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Icono
        icon_label = QLabel()
        icon_size = 24  # Tamaño del icono más pequeño que en los botones grandes
        
        # Buscar icono en recursos
        icon_path = os.path.join(self.parent.current_dir, "resources", f"{icon_name}.png")
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            icon_label.setPixmap(QIcon.fromTheme(icon_name).pixmap(icon_size, icon_size))
        
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Texto principal
        title_label = QLabel(text)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 13px;
                color: {color};
                margin-top: 3px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Descripción (diferente según el botón)
        desc_text = ""
        if text == "Desplegar":
            desc_text = "Crear nueva versión con cambios"
        elif text == "Finalizar":
            desc_text = "Consolidar cambios en el sistema"
        elif text == "Revertir":
            desc_text = "Volver a la versión anterior"
        
        desc_label = QLabel(desc_text)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: #555;
                margin-top: 3px;
            }}
        """)
        layout.addWidget(desc_label)
        
        # Estilo del botón
        btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {color};
                border-radius: 10px;
                padding: 5px;
                background-color: rgba({color[1:]}, 0.1);
            }}
            QPushButton:hover {{
                background-color: rgba({color[1:]}, 0.2);
                border: 1px solid {color};
            }}
            QPushButton:pressed {{
                background-color: rgba({color[1:]}, 0.3);
            }}
        """)
        
        return btn

    def show_main_view(self):
        """Muestra la vista principal"""
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def show_command_view(self):
        """Muestra la vista de comandos"""
        self.cmd_input.clear()  # Limpiamos el campo de comando
        self.stacked_widget.setCurrentWidget(self.command_widget)

    def show_file_op_view(self):
        """Muestra la vista de operaciones de archivos"""
        self.file_op_input.clear()
        self.stacked_widget.setCurrentWidget(self.file_op_widget)

    def execute_command(self):
        """Ejecuta el comando desde la vista de comandos"""
        command = self.cmd_input.text().strip()
        if not command:
            QMessageBox.warning(self, "Error", "Por favor ingrese un comando válido")
            return
        
        try:
            terminal_command = f"deepin-immutable-ctl admin exec -- {command}"
            full_command = f"/usr/bin/deepin-terminal -e 'bash -c \"pkexec {terminal_command}; exec bash\"'"
            process = Popen(full_command, shell=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la terminal: {str(e)}")

    def execute_file_op(self):
        """Ejecuta la operación de archivos"""
        operation = self.file_op_input.text().strip()
        if not operation:
            QMessageBox.warning(self, "Error", "Por favor ingrese una operación válida")
            return
        
        self.confirm_action(
            "Confirmar Operación de Archivos",
            f"¿Está seguro que desea ejecutar la siguiente operación?\n\n{operation}",
            f"pkexec deepin-immutable-ctl admin file-op {operation}",
            show_console=True
        )

    def connect_signals(self):
        """Conecta las señales de los botones"""
        if self.btn_deploy:
            self.btn_deploy.clicked.connect(self.show_deploy_dialog)
        if self.btn_finalize:
            self.btn_finalize.clicked.connect(self.confirm_finalize)
        if self.btn_rollback:
            self.btn_rollback.clicked.connect(self.confirm_rollback)
        if self.btn_exec:
            self.btn_exec.clicked.connect(self.show_command_view)
        if self.btn_file_op:
            self.btn_file_op.clicked.connect(self.show_file_op_view)

    def show_deploy_dialog(self):
        """Muestra un diálogo para seleccionar opciones de deploy con explicación detallada"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Desplegar Cambios en el Sistema")
        dialog.setFixedSize(500, 330)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        
        explanation = QLabel("""
            Esta acción creará una nueva versión del sistema con los cambios actuales.<br><br>
            <b>Cambios que se aplicarán:</b><br>
            • Se creará un nuevo snapshot del estado actual<br>
            • Se preparará para el próximo arranque<br>
            • Se mantendrán los archivos modificados<br><br>
            Seleccione las opciones adicionales:
        """)
        explanation.setStyleSheet("""
            QLabel {
                font-size: 13px;
                padding-top: 0px;
                margin-top: 0px;
            }
        """)
        explanation.setWordWrap(True)
        
        layout.addWidget(explanation)
        
        self.backup_check = QCheckBox("Crear backup del sistema actual (--backup)")
        self.backup_check.setToolTip("Crea una copia de seguridad adicional del estado actual")
        
        self.refresh_check = QCheckBox("Refrescar capa de modificación (--refresh)")
        self.refresh_check.setToolTip("Actualiza los archivos modificados en la capa superior")
        
        self.append_check = QCheckBox("Añadir como nuevo despliegue (--append)")
        self.append_check.setToolTip("Método obsoleto, no recomendado para uso normal")
        
        layout.addWidget(self.backup_check)
        layout.addWidget(self.refresh_check)
        layout.addWidget(self.append_check)
        
        # Botones
        btn_box = QHBoxLayout()
        btn_ok = QPushButton("Desplegar")
        btn_ok.clicked.connect(lambda: self.execute_deploy(dialog))
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cancel)
        layout.addLayout(btn_box)
        
        dialog.exec()

    def execute_deploy(self, dialog):
        """Construye y ejecuta el comando deploy con las opciones seleccionadas"""
        command = "pkexec deepin-immutable-ctl admin deploy"
        
        if self.backup_check.isChecked():
            command += " --backup"
        if self.refresh_check.isChecked():
            command += " --refresh"
        if self.append_check.isChecked():
            command += " --append"
        
        dialog.accept()
        self.confirm_action(
            "Confirmar Despliegue",
            f"¿Está seguro que desea ejecutar el despliegue con estas opciones?\n\nComando: {command}",
            command,
            show_console=True
        )

    def confirm_finalize(self):
        """Confirma la finalización del despliegue con explicación detallada"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirmar Finalización")
        msg.setText("<h3>Finalizar Despliegue</h3>")
        
        detailed_msg = (
            "Esta acción realizará los siguientes cambios:\n"
            "• Eliminará las entradas de despliegue temporales\n"
            "• Consolidará los cambios en la versión principal\n"
            "• Limpiará archivos temporales\n\n"
            "<b>⚠️ Advertencia:</b>\n"
            "• Requerirá reinicio del sistema\n"
            "• No se podrá revertir esta acción\n"
        )
        
        msg.setInformativeText(detailed_msg)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, "Continuar")
        msg.setButtonText(QMessageBox.No, "Cancelar")
        
        if msg.exec() == QMessageBox.Yes:
            self.parent.confirm_action(
                "Finalizar Despliegue",
                "¿Confirmas que deseas finalizar el despliegue?",
                "pkexec deepin-immutable-ctl admin deploy --finalize",
                show_console=True,
                requires_reboot=True
            )

    def confirm_rollback(self):
        """Confirma la reversión al estado anterior con explicación detallada"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirmar Reversión")
        msg.setText("<h3>Revertir Sistema</h3>")
        
        detailed_msg = (
            "Esta acción realizará los siguientes cambios:\n"
            "• Restaurará el sistema al estado anterior\n"
            "• Eliminará los cambios no consolidados\n"
            "• Configurará el arranque a la versión previa\n\n"
            "<b>⚠️ Advertencia:</b>\n"
            "• Requerirá reinicio del sistema\n"
            "• Todos los cambios no consolidados se perderán\n"
            "• No se podrá deshacer esta acción\n"
        )
        
        msg.setInformativeText(detailed_msg)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, "Revertir")
        msg.setButtonText(QMessageBox.No, "Cancelar")
        
        if msg.exec() == QMessageBox.Yes:
            self.parent.confirm_action(
                "Confirmar Reversión",
                "¿Confirmas que deseas revertir el sistema?",
                "pkexec deepin-immutable-ctl admin rollback",
                show_console=True,
                requires_reboot=True
            )

    def confirm_action(self, title, message, command, show_console=True, requires_reboot=False):
        """Wrapper para usar el confirm_action de la ventana principal"""
        self.parent.confirm_action(title, message, command, show_console, requires_reboot)

    def show_file_op_dialog(self):
        """Muestra diálogo para operaciones de archivos"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Operación de Archivos")
        dialog.setFixedSize(600, 450)

        layout = QVBoxLayout(dialog)

        form = QFormLayout()
        op_input = QLineEdit()
        op_input.setPlaceholderText("ej: setxattr /ruta/al/archivo user.key=value")
        form.addRow("Operación:", op_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        btn_ok = QPushButton("Ejecutar")
        btn_ok.clicked.connect(lambda: self.confirm_action(
            "Confirmar Operación de Archivos",
            f"¿Está seguro que desea ejecutar la operación:\n\n{op_input.text()}?\n\nEsta acción requiere privilegios de root.",
            f"pkexec deepin-immutable-ctl admin file-op {op_input.text()}",
            show_console=True
        ))
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(dialog.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        dialog.exec()