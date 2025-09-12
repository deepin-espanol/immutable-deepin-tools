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
        
        self.stacked_widget = QStackedWidget()
        
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
        
        self.setup_main_widget()
        
        self.setup_command_widget()
        
        self.setup_file_op_widget()
        
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def setup_main_widget(self):
        """Configura el widget principal con los botones"""
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.setSpacing(15)
        
        # Botón Ejecutar Comando
        self.btn_exec = self.create_modern_button(
            self.tr("Ejecutar Comando"),
            "admin-run",
            self.tr("Ejecutar comandos sin la desactivación de la capa inmutable"),
            "#3498db"
        )
        top_buttons_layout.addWidget(self.btn_exec, 1)
        
        # Botón Operación de Archivos
        self.btn_file_op = self.create_modern_button(
            self.tr("Manipular Archivos"),
            "file-operation",
            self.tr("Realizar operaciones avanzadas en archivos"),
            "#2ecc71"
        )
        top_buttons_layout.addWidget(self.btn_file_op, 1)
        
        layout.addLayout(top_buttons_layout)

        deploy_group = QGroupBox(self.tr("Opciones de Despliegue"))
        deploy_layout = QGridLayout(deploy_group)
        
        self.btn_deploy = self.create_small_button(self.tr("Desplegar"), "deploy-save", "#f39c12")
        self.btn_finalize = self.create_small_button(self.tr("Finalizar"), "deploy-finalize", "#e74c3c")
        self.btn_rollback = self.create_small_button(self.tr("Revertir"), "deploy-rollback", "#9b59b6")
        
        deploy_layout.addWidget(self.btn_deploy, 0, 0)
        deploy_layout.addWidget(self.btn_finalize, 0, 1)
        deploy_layout.addWidget(self.btn_rollback, 0, 2)
        
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
            # Fallback
            icon_label = QLabel()
            icon_label.setPixmap(QIcon.fromTheme("go-previous").pixmap(16, 16))
            btn_back_layout.addWidget(icon_label)

        text_label = QLabel(self.tr("Volver"))
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
        description_text = self.tr("""Esta herramienta ejecutará el comando bajo <code>deepin-immutable-ctl admin exec</code>, 
lo que permite realizar cambios temporales en el sistema inmutable.

<b>Advertencias:</b>
<ul>
<li>Manipular archivos del sistema puede causar inestabilidad</li>
<li>Los cambios pueden perderse al reiniciar si no se consolidan</li>
<li>Algunas operaciones pueden requerir reinicio para aplicar cambios</li>
</ul>

<b>Se recomienda que realice una copia de seguridad para cambios importantes.</b>""")
        
        description = QLabel(description_text)
        description.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 15px;
            }
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        title = QLabel(self.tr("Ejecutar Comando (admin)"))
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        input_container = QHBoxLayout()
        input_container.setSpacing(10)
        
        # Campo de entrada de comandos
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText(self.tr("Ingresa el comando ej: apt update && apt upgrade -y"))
        input_container.addWidget(self.cmd_input, stretch=1)  # El campo de entrada ocupa todo el espacio disponible
        
        btn_execute = QPushButton()
        btn_execute.setMinimumWidth(120)  
        
        btn_layout = QHBoxLayout(btn_execute)
        btn_layout.setContentsMargins(10, 5, 10, 5)
        btn_layout.setSpacing(8)
        
        execute_icon = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "run-command.png")
        if os.path.exists(icon_path):
            execute_icon.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            execute_icon.setPixmap(QIcon.fromTheme("system-run").pixmap(icon_size, icon_size))
        btn_layout.addWidget(execute_icon)
        
        execute_text = QLabel(self.tr("Ejecutar"))
        execute_text.setStyleSheet("font-weight: bold;")
        btn_layout.addWidget(execute_text)
        
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

        common_commands_group = QGroupBox(self.tr("Comandos comunes"))
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

        text_label = QLabel(self.tr("Volver"))
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
        
        # Descripción del proceso
        description_text = self.tr("""Esta herramienta permite realizar operaciones en archivos del sistema 
usando deepin-immutable-ctl admin file-op.

Operaciones disponibles:
Establecer atributos extendidos (ej: setxattr /ruta/al/archivo user.key=value)
Eliminar atributos extendidos (ej: rmxattr /ruta/al/archivo user.key)
Cambiar atributos de archivo (ej: chattr /ruta/al/archivo +i)

Advertencia: Estas operaciones afectan directamente al sistema de archivos.""")
        
        description = QLabel(description_text)
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
        title = QLabel(self.tr("Operaciones de Archivos"))
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        input_container = QHBoxLayout()
        input_container.setSpacing(10)
        
        self.file_op_input = QLineEdit()
        self.file_op_input.setPlaceholderText(self.tr("Ingrese la operación de archivo (ej: setxattr /ruta/al/archivo user.key=value)"))
        input_container.addWidget(self.file_op_input, stretch=1) 
        
        btn_execute = QPushButton()
        btn_execute.setMinimumWidth(120)  
        
        btn_layout = QHBoxLayout(btn_execute)
        btn_layout.setContentsMargins(10, 5, 10, 5)
        btn_layout.setSpacing(8)
        
        execute_icon = QLabel()
        icon_size = 16
        icon_path = os.path.join(self.parent.current_dir, "resources", "run-command.png")
        if os.path.exists(icon_path):
            execute_icon.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            execute_icon.setPixmap(QIcon.fromTheme("system-run").pixmap(icon_size, icon_size))
        btn_layout.addWidget(execute_icon)
        
        execute_text = QLabel(self.tr("Ejecutar"))
        execute_text.setStyleSheet("font-weight: bold;")
        btn_layout.addWidget(execute_text)
        
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
        examples_group = QGroupBox(self.tr("Ejemplos de Operaciones"))
        examples_layout = QVBoxLayout(examples_group)
        
        examples = [
            (self.tr("Cambiar atributos"), "chattr /ruta/al/archivo +i"),
            (self.tr("Eliminar atributos"), "rmxattr /ruta/al/archivo user.key"),
            (self.tr("Establecer atributos"), "setxattr /ruta/al/archivo user.key=value"),
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
        
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)
        
        icon_label = QLabel()
        icon_size = 48  
        
        icon_path = os.path.join(self.parent.current_dir, "resources", f"{icon_name}.png")
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            icon_label.setPixmap(QIcon.fromTheme(icon_name).pixmap(icon_size, icon_size))
        
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
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
        btn.setMinimumHeight(80)  
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        icon_label = QLabel()
        icon_size = 24 
        
        icon_path = os.path.join(self.parent.current_dir, "resources", f"{icon_name}.png")
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(icon_size, icon_size))
        else:
            icon_label.setPixmap(QIcon.fromTheme(icon_name).pixmap(icon_size, icon_size))
        
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
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
        
        desc_text = ""
        if text == self.tr("Desplegar"):
            desc_text = self.tr("Crear nueva versión con cambios")
        elif text == self.tr("Finalizar"):
            desc_text = self.tr("Consolidar cambios en el sistema")
        elif text == self.tr("Revertir"):
            desc_text = self.tr("Volver a la versión anterior")
        
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
        self.cmd_input.clear() 
        self.stacked_widget.setCurrentWidget(self.command_widget)

    def show_file_op_view(self):
        """Muestra la vista de operaciones de archivos"""
        self.file_op_input.clear()
        self.stacked_widget.setCurrentWidget(self.file_op_widget)

    def execute_command(self):
        """Ejecuta el comando desde la vista de comandos"""
        command = self.cmd_input.text().strip()
        if not command:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Por favor ingrese un comando válido"))
            return
        
        try:
            terminal_command = f"deepin-immutable-ctl admin exec -- {command}"
            full_command = f"/usr/bin/deepin-terminal -e 'bash -c \"pkexec {terminal_command}; exec bash\"'"
            process = Popen(full_command, shell=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("No se pudo abrir la terminal: {0}").format(str(e)))

    def execute_file_op(self):
        """Ejecuta la operación de archivos"""
        operation = self.file_op_input.text().strip()
        if not operation:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Por favor ingrese una operación válida"))
            return
        
        self.confirm_action(
            self.tr("Confirmar Operación de Archivos"),
            self.tr("¿Está seguro que desea ejecutar la siguiente operación?\n\n{0}").format(operation),
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
        dialog.setWindowTitle(self.tr("Desplegar Cambios en el Sistema"))
        dialog.setFixedSize(500, 330)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        
        explanation_text = self.tr("""Esta acción creará una nueva versión del sistema con los cambios actuales.

Cambios que se aplicarán:
• Se creará un nuevo snapshot del estado actual
• Se preparará para el próximo arranque
• Se mantendrán los archivos modificados

Seleccione las opciones adicionales:""")
        
        explanation = QLabel(explanation_text)
        explanation.setStyleSheet("""
            QLabel {
                font-size: 13px;
                padding-top: 0px;
                margin-top: 0px;
            }
        """)
        explanation.setWordWrap(True)
        
        layout.addWidget(explanation)
        
        self.backup_check = QCheckBox(self.tr("Crear backup del sistema actual (--backup)"))
        self.backup_check.setToolTip(self.tr("Crea una copia de seguridad adicional del estado actual"))
        
        self.refresh_check = QCheckBox(self.tr("Refrescar capa de modificación (--refresh)"))
        self.refresh_check.setToolTip(self.tr("Actualiza los archivos modificados en la capa superior"))
        
        self.append_check = QCheckBox(self.tr("Añadir como nuevo despliegue (--append)"))
        self.append_check.setToolTip(self.tr("Método obsoleto, no recomendado para uso normal"))
        
        layout.addWidget(self.backup_check)
        layout.addWidget(self.refresh_check)
        layout.addWidget(self.append_check)
        
        btn_box = QHBoxLayout()
        btn_ok = QPushButton(self.tr("Desplegar"))
        btn_ok.clicked.connect(lambda: self.execute_deploy(dialog))
        btn_cancel = QPushButton(self.tr("Cancelar"))
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
            self.tr("Confirmar Despliegue"),
            self.tr("¿Está seguro que desea ejecutar el despliegue con estas opciones?\n\nComando: {0}").format(command),
            command,
            show_console=True
        )

    def confirm_finalize(self):
        """Confirma la finalización del despliegue con explicación detallada"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(self.tr("Confirmar Finalización"))
        msg.setText(self.tr("<h3>Finalizar Despliegue</h3>"))
        
        detailed_msg = self.tr("""Esta acción realizará los siguientes cambios:
• Eliminará las entradas de despliegue temporales
• Consolidará los cambios en la versión principal
• Limpiará archivos temporales

Advertencia:
• Requerirá reinicio del sistema
• No se podrá revertir esta acción""")
        
        msg.setInformativeText(detailed_msg)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, self.tr("Continuar"))
        msg.setButtonText(QMessageBox.No, self.tr("Cancelar"))
        
        if msg.exec() == QMessageBox.Yes:
            self.parent.confirm_action(
                self.tr("Finalizar Despliegue"),
                self.tr("¿Confirmas que deseas finalizar el despliegue?"),
                "pkexec deepin-immutable-ctl admin deploy --finalize",
                show_console=True,
                requires_reboot=True
            )

    def confirm_rollback(self):
        """Confirma la reversión al estado anterior con explicación detallada"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(self.tr("Confirmar Reversión"))
        msg.setText(self.tr("<h3>Revertir Sistema</h3>"))
        
        detailed_msg = self.tr("""Esta acción realizará los siguientes cambios:
• Restaurará el sistema al estado anterior
• Eliminará los cambios no consolidados
• Configurará el arranque a la versión previa

Advertencia:
• Requerirá reinicio del sistema
• Todos los cambios no consolidados se perderán
• No se podrá deshacer esta acción""")
        
        msg.setInformativeText(detailed_msg)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, self.tr("Revertir"))
        msg.setButtonText(QMessageBox.No, self.tr("Cancelar"))
        
        if msg.exec() == QMessageBox.Yes:
            self.parent.confirm_action(
                self.tr("Confirmar Reversión"),
                self.tr("¿Confirmas que deseas revertir el sistema?"),
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
        dialog.setWindowTitle(self.tr("Operación de Archivos"))
        dialog.setFixedSize(600, 450)

        layout = QVBoxLayout(dialog)

        form = QFormLayout()
        op_input = QLineEdit()
        op_input.setPlaceholderText(self.tr("ej: setxattr /ruta/al/archivo user.key=value"))
        form.addRow(self.tr("Operación:"), op_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        btn_ok = QPushButton(self.tr("Ejecutar"))
        btn_ok.clicked.connect(lambda: self.confirm_action(
            self.tr("Confirmar Operación de Archivos"),
            self.tr("¿Está seguro que desea ejecutar la operación:\n\n{0}?\n\nEsta acción requiere privilegios de root.").format(op_input.text()),
            f"pkexec deepin-immutable-ctl admin file-op {op_input.text()}",
            show_console=True
        ))
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel = QPushButton(self.tr("Cancelar"))
        btn_cancel.clicked.connect(dialog.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        dialog.exec()
