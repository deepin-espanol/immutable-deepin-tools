#!/usr/bin/env python3

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                              QPushButton, QLabel, QFrame, QGridLayout)
from PySide6.QtCore import Qt

class StatusTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.create_ui()
        
    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        status_group = QGroupBox(self.tr("Estado Actual del Sistema Inmutable"))
        status_group_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel(self.tr("Cargando estado..."))
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_group_layout.addWidget(self.status_label)

        btn_check_status = QPushButton(self.tr("Actualizar Estado"))
        btn_check_status.clicked.connect(self.check_immutable_status)
        status_group_layout.addWidget(btn_check_status, alignment=Qt.AlignCenter)

        status_group_layout.addWidget(self.create_separator())

        # Grupo para parámetros de configuración
        params_group = QGroupBox(self.tr("Parámetros de Configuración"))
        params_layout = QGridLayout(params_group)
        params_layout.setVerticalSpacing(5)
        params_layout.setHorizontalSpacing(15)

        # Etiquetas para los parámetros
        self.whitelist_label = QLabel(self.tr("Lista Blanca:"))
        self.whitelist_value = QLabel("Cargando...")
        
        self.clear_reboot_label = QLabel(self.tr("Limpiar tras Reinicio:"))
        self.clear_reboot_value = QLabel("Cargando...")
        
        self.clean_data_label = QLabel(self.tr("Limpiar Datos:"))
        self.clean_data_value = QLabel("Cargando...")
        
        self.overlay_dirs_label = QLabel(self.tr("Directorios en Overlay:"))
        self.overlay_dirs_value = QLabel("Cargando...")
        
        self.overlay_all_label = QLabel(self.tr("Overlay en Todos los Directorios:"))
        self.overlay_all_value = QLabel("Cargando...")

        # Agregar al layout en dos columnas
        params_layout.addWidget(self.whitelist_label, 0, 0)
        params_layout.addWidget(self.whitelist_value, 0, 1)
        
        params_layout.addWidget(self.clear_reboot_label, 1, 0)
        params_layout.addWidget(self.clear_reboot_value, 1, 1)
        
        params_layout.addWidget(self.clean_data_label, 2, 0)
        params_layout.addWidget(self.clean_data_value, 2, 1)
        
        params_layout.addWidget(self.overlay_dirs_label, 3, 0)
        params_layout.addWidget(self.overlay_dirs_value, 3, 1)
        
        params_layout.addWidget(self.overlay_all_label, 4, 0)
        params_layout.addWidget(self.overlay_all_value, 4, 1)

        status_group_layout.addWidget(params_group)

        status_group_layout.addWidget(self.create_separator())

        immutable_toggle_layout = QHBoxLayout()
        
        self.btn_disable_immutable = QPushButton(self.tr("Desactivar Inmutabilidad"))
        self.btn_disable_immutable.setStyleSheet("""
            QPushButton { background-color: #E74C3C; color: white; }
            QPushButton:hover { background-color: #C0392B; }
            QPushButton:pressed { background-color: #A93226; }
            QPushButton:disabled { background-color: #555555; color: #777777; }
        """)
        self.btn_disable_immutable.clicked.connect(self.disable_immutable_mode)
        immutable_toggle_layout.addWidget(self.btn_disable_immutable)

        self.btn_enable_immutable = QPushButton(self.tr("Activar Inmutabilidad"))
        self.btn_enable_immutable.setStyleSheet("""
            QPushButton { background-color: #2ECC71; color: white; }
            QPushButton:hover { background-color: #27AE60; }
            QPushButton:pressed { background-color: #1E8449; }
            QPushButton:disabled { background-color: #555555; color: #777777; }
        """)
        self.btn_enable_immutable.clicked.connect(self.enable_immutable_mode)
        immutable_toggle_layout.addWidget(self.btn_enable_immutable)

        status_group_layout.addLayout(immutable_toggle_layout)

        immutable_info_label = QLabel(self.tr(
            "Al desactivar la inmutabilidad, el directorio `/usr` se vuelve escribible, permitiendo la instalación de software y modificaciones directas en el sistema base. "
            "Esto es útil para desarrolladores o usuarios avanzados, pero reduce la seguridad y estabilidad del sistema inmutable."
            "<br><br>"
            "Al activar la inmutabilidad, `/usr` vuelve a ser de solo lectura, protegiendo el sistema base de cambios no deseados."
        ))
        immutable_info_label.setWordWrap(True)
        status_group_layout.addWidget(immutable_info_label)

        layout.addWidget(status_group)
        layout.addStretch(1)
        
        # Verificar estado inicial
        self.check_immutable_status()

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedHeight(2)
        
        # Usar la referencia al parent para determinar el tema
        if hasattr(self.parent, 'dark_mode') and self.parent.dark_mode:
            separator.setStyleSheet("background-color: #444444; border: none;")
        else:
            separator.setStyleSheet("background-color: #DDDDDD; border: none;")
            
        return separator

    def parse_status_output(self, output):
        """Parsea la salida del comando de estado y extrae los parámetros"""
        params = {}
        
        # Dividir por líneas y procesar cada una
        for line in output.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().rstrip(',')  # Quitar la coma final
                params[key] = value
                
        return params

    def check_immutable_status(self):
        # Obtener el estado completo
        output = self.controller.execute_command("deepin-immutable-writable status", show_in_console=False)
        
        # Parsear la salida
        params = self.parse_status_output(output)
        
        # --- ESTE ES EL CAMBIO ---
        # `Enable: true` significa que la ESCRITURA está habilitada,
        # por lo tanto, la INMUTABILIDAD está deshabilitada.
        # La lógica debe ser inversa:
        is_immutable = params.get('Enable', 'false').lower() == 'false'
        # -------------------------
        
        is_booted = params.get('Booted', 'false').lower() == 'true'

        if is_immutable:
            status_text = self.tr("✔ Sistema en modo inmutable")
            if is_booted:
                # Si 'Enable' es false, 'Booted' también debería ser false, pero mantenemos la lógica por si acaso
                status_text += self.tr(" (Arrancado en modo inmutable)")
            else:
                status_text += self.tr(" (Configurado pero no arrancado en modo escritura)")
                
            self.status_label.setText(status_text)
            self.status_label.setStyleSheet("color: #2ECC71;")
            self.btn_disable_immutable.setEnabled(True)  # Permitir desactivar (habilitar escritura)
            self.btn_enable_immutable.setEnabled(False) # Ya está activada
        else:
            # Esto significa que Enable: true (modo escritura activado)
            self.status_label.setText(self.tr("✖ El sistema NO está en modo inmutable (Modo Escritura Habilitado)"))
            self.status_label.setStyleSheet("color: #E74C3C;")
            self.btn_disable_immutable.setEnabled(False) # Ya está desactivada
            self.btn_enable_immutable.setEnabled(True)   # Permitir activar (deshabilitar escritura)

        # Actualizar parámetros de configuración
        self.whitelist_value.setText(params.get('Whitelist', 'N/A'))
        self.clear_reboot_value.setText(self.tr("Sí") if params.get('ClearAfterReboot', 'false').lower() == 'true' else self.tr("No"))
        self.clean_data_value.setText(self.tr("Sí") if params.get('CleanData', 'false').lower() == 'true' else self.tr("No"))
        self.overlay_dirs_value.setText(params.get('OverlayDirs', 'N/A'))
        self.overlay_all_value.setText(self.tr("Sí") if params.get('OverlayAllDirs', 'false').lower() == 'true' else self.tr("No"))

    def disable_immutable_mode(self):
        # Esta función HABILITA el modo escritura
        self.parent.confirm_action(
            self.tr("Confirmar Desactivación de Inmutabilidad"),
            self.tr("¿Está seguro que desea desactivar el modo inmutable?\n\n"
                "Esto hará que el directorio '/usr' sea escribible, permitiendo modificaciones en el sistema base.\n"
                "Esta acción requiere un reinicio del sistema para aplicar los cambios.\n\n"
                "Esta acción requiere privilegios de root."),
            "pkexec deepin-immutable-writable enable -d /usr -y", # Habilita la escritura
            show_console=True,
            requires_reboot=True  # Esta operación SÍ requiere reinicio
        )

    def enable_immutable_mode(self):
        # Esta función DESHABILITA el modo escritura
        self.parent.confirm_action(
            self.tr("Confirmar Activación de Inmutabilidad"),
            self.tr("¿Está seguro que desea activar el modo inmutable de nuevo?\n\n"
                "Esto hará que el directorio '/usr' vuelva a ser de solo lectura, protegiendo el sistema base.\n"
                "Esta acción requiere un reinicio del sistema para aplicar los cambios.\n\n"
                "Esta acción requiere privilegios de root."),
            "pkexec deepin-immutable-writable disable -y", # Deshabilita la escritura
            show_console=True,
            requires_reboot=True  # Esta operación SÍ requiere reinicio
        )