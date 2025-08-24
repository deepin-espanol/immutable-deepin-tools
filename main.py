#!/usr/bin/env python3

import os
import sys
import json
import importlib.util
from subprocess import Popen, PIPE
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QTabWidget, QGroupBox, QPushButton, QLabel, QTextEdit,
                              QMessageBox, QListWidget, QDialog, QFormLayout, QLineEdit,
                              QFrame, QSizePolicy, QMenu, QGraphicsDropShadowEffect, QInputDialog,
                              QStackedWidget, QGridLayout, QListWidgetItem)
from PySide6.QtGui import QIcon, QColor, QPalette, QPainter, QRegion, QCursor, QPainterPath, QDesktopServices, QTextCursor
from PySide6.QtCore import Qt, Signal, QObject, QPoint, QSize, QRect, QDir, QUrl, QTimer, QProcess

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    os.path.dirname(sys.executable), 'plugins'
)

class ConfigManager:
    @staticmethod
    def get_config_path():
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".config", "immutable-deepin-tools")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "config.json")

    @staticmethod
    def load_config():
        config_path = ConfigManager.get_config_path()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {"dark_mode": True}  # Default value

    @staticmethod
    def save_config(config):
        try:
            with open(ConfigManager.get_config_path(), 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

class ThemeManager:
    @staticmethod
    def dark_theme():
        return """
        /* General */
        * {
            font-family: 'Noto Sans', sans-serif;
            color: #BEBEBE;
        }

        /* Ventana principal */
        QMainWindow {
            background-color: #252525;
            color: #BEBEBE;
        }

        /* Barra de título principal */
        #title_bar {
            background-color: #262626;
            border-bottom: 1px solid #333333;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }

        /* Barra de título - texto */
        #title_label {
            color: #BEBEBE;
            font-size: 14px;
            font-weight: bold;
            padding-left: 8px;
        }

        /* Botones de la barra de título */
        #window_button {
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
            width: 24px;
            height: 24px;
            border-radius: 0px;
        }
        #window_button:hover {
            background-color: #4A4A4A;
        }
        #window_button:pressed {
            background-color: #323232;
        }
        #close_button:hover {
            background-color: #E81123;
        }
        #close_button:pressed {
            background-color: #8C0A1A;
        }

        /* Contenido principal de la ventana principal */
        #content_widget {
            background-color: #2D2D2D;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        /* Lista de navegación lateral */
        #nav_list {
            border: none;
            background-color: #252525;
            color: #BEBEBE;
            padding: 5px;
        }
        #nav_list::item {
            padding: 12px 15px;
            border-bottom: 1px solid #333333;
            background-color: transparent;
            border-radius: 5px;
            margin-bottom: 2px;
        }
        #nav_list::item:hover {
            background-color: #3A3A3A;
        }
        #nav_list::item:selected {
            background-color: #0081FF;
            color: #FFFFFF;
        }
        #nav_list::item:selected:hover {
            background-color: #006BB3; 
            color: #FFFFFF;
        }

        /* Grupos (QGroupBox) */
        QGroupBox {
            background-color: #3A3A3A;
            border: 1px solid #444444;
            border-radius: 10px;
            margin-top: 25px;
            padding-top: 25px;
            color: #BEBEBE;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            background-color: transparent;
            color: #BEBEBE;
            border-radius: 0px;
            font-weight: bold;
            font-size: 14px;
            top: 5px;
            margin-left: 10px;
            margin-right: 10px;
        }

        /* Botones generales */
        QPushButton {
            background-color: #2ca7f8;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            min-width: 120px;
            font-size: 13px;
            font-weight: bold;
            text-align: center;
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

        /* Botones de comandos comunes */
        #common_command_button {
            background-color: #E74C3C;
            min-width: 80px;
            padding: 8px;
            font-size: 12px;
        }
        #common_command_button:hover {
            background-color: #C0392B;
        }
        #common_command_button:pressed {
            background-color: #A93226;
        }

        /* Botones específicos para el tab de Snapshots */
        QPushButton#btn_create_snapshot {
            background-color: #2ECC71;
            min-width: 100px;
        }
        QPushButton#btn_create_snapshot:hover {
            background-color: #27AE60;
        }
        QPushButton#btn_create_snapshot:pressed {
            background-color: #1E8449;
        }

        QPushButton#btn_delete_snapshot {
            background-color: #E74C3C;
            min-width: 100px;
        }
        QPushButton#btn_delete_snapshot:hover {
            background-color: #C0392B;
        }
        QPushButton#btn_delete_snapshot:pressed {
            background-color: #A93226;
        }

        QPushButton#btn_modify_snapshot {
            background-color: #F39C12;
            min-width: 40px;
            max-width: 40px;
            padding: 8px;
        }
        QPushButton#btn_modify_snapshot:hover {
            background-color: #D68910;
        }
        QPushButton#btn_modify_snapshot:pressed {
            background-color: #B9770E;
        }

        QPushButton#btn_show_snapshot, QPushButton#btn_refresh_list {
            background-color: #0081FF;
            min-width: 40px;
            max-width: 40px;
            padding: 8px;
        }
        QPushButton#btn_show_snapshot:hover, QPushButton#btn_refresh_list:hover {
            background-color: #006BB3;
        }
        QPushButton#btn_show_snapshot:pressed, QPushButton#btn_refresh_list:pressed {
            background-color: #004A77;
        }

        /* Área de texto */
        QTextEdit {
            border: 1px solid #444444;
            border-radius: 8px;
            padding: 10px;
            background-color: #2D2D2D;
            color: #BEBEBE;
            font-family: 'Cascadia Code', 'Consolas', monospace;
            font-size: 12px;
        }

        /* Lista */
        QListWidget {
            border: 1px solid #444444;
            border-radius: 8px;
            background-color: #3A3A3A;
            color: #BEBEBE;
            padding: 5px;
        }
        QListWidget::item {
            padding: 10px;
            border-bottom: 1px solid #444444;
            background-color: #3A3A3A;
            border-radius: 5px;
            margin-bottom: 2px;
        }
        QListWidget::item:hover {
            background-color: #4A4A4A;
        }
        QListWidget::item:selected {
            background-color: #0081FF;
            color: #FFFFFF;
        }

        /* Campos de entrada */
        QLineEdit {
            border: 1px solid #444444;
            border-radius: 6px;
            padding: 8px;
            background-color: #2D2D2D;
            color: #BEBEBE;
        }

        /* Etiquetas de estado */
        QLabel#status_label {
            font-weight: bold;
            font-size: 15px;
            padding: 5px;
        }

        /* Enlaces */
        QLabel a {
            color: #66b3ff;
            text-decoration: underline;
        }
        QLabel a:hover {
            color: #0081FF;
        }

        /* Diálogos (Pop-ups) */
        QDialog {
            background-color: #2D2D2D;
            color: #BEBEBE;
        }
        QDialog QGroupBox {
            background-color: #3A3A3A;
            color: #BEBEBE;
        }
        QDialog QLabel {
            color: #BEBEBE;
        }
        QDialog QLineEdit {
            background-color: #2D2D2D;
            color: #BEBEBE;
        }
        QDialog QTextEdit {
            background-color: #2D2D2D;
            color: #BEBEBE;
        }
        /* Botón de cerrar en consola */
        QDialog #close_button {
            background-color: #0081FF;
            color: white;
            padding: 8px 16px;
            min-width: 80px;
            margin: 10px;
        }
        QDialog #close_button:hover {
            background-color: #006BB3;
        }
        QDialog #close_button:pressed {
            background-color: #004A77;
        }
        /* Botones de reinicio */
        QDialog #reboot_button {
            padding: 8px 16px;
            min-width: 120px;
            margin: 10px;
        }
        QDialog #reboot_button:nth-child(1) {  # Reiniciar Ahora
            background-color: #2ECC71;
            color: white;
        }
        QDialog #reboot_button:nth-child(1):hover {
            background-color: #27AE60;
        }
        QDialog #reboot_button:nth-child(1):pressed {
            background-color: #1E8449;
        }
        QDialog #reboot_button:nth-child(2) {  # Más Tarde
            background-color: #E74C3C;
            color: white;
        }
        QDialog #reboot_button:nth-child(2):hover {
            background-color: #C0392B;
        }
        QDialog #reboot_button:nth-child(2):pressed {
            background-color: #A93226;
        }
        /* Diálogo Acerca de */
        QDialog QLabel {
            margin: 5px;
        }
        QDialog QLabel[accessibleName="link"] {
            color: #0081FF;
        }
        QDialog QLabel[accessibleName="link"]:hover {
            color: #006BB3;
            text-decoration: underline;
        }
        QDialog QPushButton {
            min-width: 100px;
            padding: 8px;
            margin-top: 15px;
        }
        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #2a2a2a;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #4a4a4a;
            min-height: 30px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #5a5a5a;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            border: none;
            background: #2a2a2a;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background: #4a4a4a;
            min-width: 30px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #5a5a5a;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0;
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        /* Menú desplegable */
        QMenu {
            background-color: #3A3A3A;
            border: 1px solid #444444;
            border-radius: 6px;
            padding: 5px;
        }

        QMenu::item {
            background-color: transparent;
            padding: 8px 25px 8px 20px;
            margin: 2px;
            border-radius: 4px;
        }

        QMenu::item:selected {
            background-color: #0081FF;
            color: #FFFFFF;
        }

        QMenu::item:disabled {
            color: #777777;
        }

        QMenu::separator {
            height: 1px;
            background-color: #444444;
            margin: 5px 0;
        }
        """

    @staticmethod
    def light_theme():
        return """
        /* General */
        * {
            font-family: 'Noto Sans', sans-serif;
            color: #333333;
        }

        /* Ventana principal */
        QMainWindow {
            background-color: #F5F5F5;
            color: #333333;
        }

        /* Barra de título principal (Customizada) */

    /* Botones de la barra de título en tema claro */
        #window_button {
            color: #333333;
        }
        #window_button:hover {
            background-color: #E0E0E0;
            color: #333333;
        }
        #window_button:pressed {
            background-color: #D0D0D0;
        }
        #close_button:hover {
            background-color: #FF5C5C;
            color: white;
        }
        #close_button:pressed {
            background-color: #E04A4A;
        }

        /* Barra de título principal */
        #title_bar {
            background-color: #FFFFFF;
            border-bottom: 1px solid #DDDDDD;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }

        /* Barra de título - texto */
        #title_label {
            color: #333333;
            font-size: 14px;
            font-weight: bold;
            padding-left: 8px;
        }

        /* Botones de la barra de título */
        #window_button {
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
            width: 24px;
            height: 24px;
            border-radius: 0px;
        }
        #window_button:hover {
            background-color: #E0E0E0;
        }
        #window_button:pressed {
            background-color: #D0D0D0;
        }
        #close_button:hover {
            background-color: #FF5C5C;
        }
        #close_button:pressed {
            background-color: #E04A4A;
        }

        /* Contenido principal de la ventana principal */
        #content_widget {
            background-color: #FFFFFF;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        /* Lista de navegación lateral */
        #nav_list {
            border: none;
            background-color: #F0F0F0;
            color: #333333;
            padding: 5px;
        }
        #nav_list::item {
            padding: 12px 15px;
            border-bottom: 1px solid #E0E0E0;
            background-color: transparent;
            border-radius: 5px;
            margin-bottom: 2px;
        }
        #nav_list::item:hover {
            background-color: #E5E5E5;
        }
        #nav_list::item:selected {
            background-color: #2ca7f8;
            color: #FFFFFF;
        }
        #nav_list::item:selected:hover {
            background-color: #1d8dd8;  /* Un azul más oscuro para el hover en seleccionado */
            color: #FFFFFF;
        }

        /* Grupos */
        QGroupBox {
            background-color: #F0F0F0;
            border: 1px solid #E0E0E0;
            border-radius: 10px;
            margin-top: 25px;
            padding-top: 25px;
            color: #333333;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            background-color: transparent;
            color: #333333;
            border-radius: 0px;
            font-weight: bold;
            font-size: 14px;
            top: 5px;
            margin-left: 10px;
            margin-right: 10px;
        }

        /* Botones generales */
        QPushButton {
            background-color: #2ca7f8;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            min-width: 120px;
            font-size: 13px;
            font-weight: bold;
            text-align: center;
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

        /* Botones de comandos comunes */
        #common_command_button {
            background-color: #E74C3C;
            min-width: 80px;
            padding: 8px;
            font-size: 12px;
        }
        #common_command_button:hover {
            background-color: #C0392B;
        }
        #common_command_button:pressed {
            background-color: #A93226;
        }

        /* Botones específicos para el tab de Snapshots */
        QPushButton#btn_create_snapshot {
            background-color: #2ECC71;
            min-width: 100px;
        }
        QPushButton#btn_create_snapshot:hover {
            background-color: #27AE60;
        }
        QPushButton#btn_create_snapshot:pressed {
            background-color: #1E8449;
        }

        QPushButton#btn_delete_snapshot {
            background-color: #E74C3C;
            min-width: 100px;
        }
        QPushButton#btn_delete_snapshot:hover {
            background-color: #C0392B;
        }
        QPushButton#btn_delete_snapshot:pressed {
            background-color: #A93226;
        }

        QPushButton#btn_modify_snapshot {
            background-color: #F39C12;
            min-width: 40px;
            max-width: 40px;
            padding: 8px;
        }
        QPushButton#btn_modify_snapshot:hover {
            background-color: #D68910;
        }
        QPushButton#btn_modify_snapshot:pressed {
            background-color: #B9770E;
        }

        QPushButton#btn_show_snapshot, QPushButton#btn_refresh_list {
            background-color: #2ca7f8;
            min-width: 40px;
            max-width: 40px;
            padding: 8px;
        }
        QPushButton#btn_show_snapshot:hover, QPushButton#btn_refresh_list:hover {
            background-color: #1d8dd8;
        }
        QPushButton#btn_show_snapshot:pressed, QPushButton#btn_refresh_list:pressed {
            background-color: #0a70b9;
        }

        /* Área de texto */
        QTextEdit {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 10px;
            background-color: #FFFFFF;
            color: #333333;
            font-family: 'Cascadia Code', 'Consolas', monospace;
            font-size: 12px;
        }

        /* Lista */
        QListWidget {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            background-color: #FFFFFF;
            color: #333333;
            padding: 5px;
        }
        QListWidget::item {
            padding: 10px;
            border-bottom: 1px solid #F0F0F0;
            background-color: #FFFFFF;
            border-radius: 5px;
            margin-bottom: 2px;
        }
        QListWidget::item:hover {
            background-color: #A6A6A6;
        }
        QListWidget::item:selected {
            background-color: #2ca7f8;
            color: #FFFFFF;
        }

        /* Campos de entrada */
        QLineEdit {
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 8px;
            background-color: #FFFFFF;
            color: #333333;
        }

        /* Etiquetas de estado */
        QLabel#status_label {
            font-weight: bold;
            font-size: 15px;
            padding: 5px;
        }

        /* Enlaces */
        QLabel a {
            color: #2ca7f8;
            text-decoration: underline;
        }
        QLabel a:hover {
            color: #1d8dd8;
        }

        /* Diálogos (Pop-ups) */
        QDialog {
            background-color: #F5F5F5;
            color: #333333;
        }
        QDialog QGroupBox {
            background-color: #FFFFFF;
            color: #333333;
        }
        QDialog QLabel {
            color: #333333;
        }
        QDialog QLineEdit {
            background-color: #FFFFFF;
            color: #333333;
        }
        QDialog QTextEdit {
            background-color: #FFFFFF;
            color: #333333;
        }
        /* Botón de cerrar en consola */
        QDialog #close_button {
            background-color: #0081FF;
            color: white;
            padding: 8px 16px;
            min-width: 80px;
            margin: 10px;
        }
        QDialog #close_button:hover {
            background-color: #006BB3;
        }
        QDialog #close_button:pressed {
            background-color: #004A77;
        }
        /* Botones de reinicio */
        QDialog #reboot_button {
            padding: 8px 16px;
            min-width: 120px;
            margin: 10px;
        }
        QDialog #reboot_button:nth-child(1) {  # Reiniciar Ahora
            background-color: #2ECC71;
            color: white;
        }
        QDialog #reboot_button:nth-child(1):hover {
            background-color: #27AE60;
        }
        QDialog #reboot_button:nth-child(1):pressed {
            background-color: #1E8449;
        }
        QDialog #reboot_button:nth-child(2) {  # Más Tarde
            background-color: #E74C3C;
            color: white;
        }
        QDialog #reboot_button:nth-child(2):hover {
            background-color: #C0392B;
        }
        QDialog #reboot_button:nth-child(2):pressed {
            background-color: #A93226;
        }
        /* Diálogo Acerca de */
        QDialog QLabel {
            margin: 5px;
        }
        QDialog QLabel[accessibleName="link"] {
            color: #0081FF;
        }
        QDialog QLabel[accessibleName="link"]:hover {
            color: #006BB3;
            text-decoration: underline;
        }
        QDialog QPushButton {
            min-width: 100px;
            padding: 8px;
            margin-top: 15px;
        }
        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 30px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            border: none;
            background: #f0f0f0;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background: #c0c0c0;
            min-width: 30px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #a0a0a0;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0;
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        /* Menú desplegable */
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 5px;
        }

        QMenu::item {
            background-color: transparent;
            padding: 8px 25px 8px 20px;
            margin: 2px;
            border-radius: 4px;
            color: #333333;
        }

        QMenu::item:selected {
            background-color: #2ca7f8;
            color: #FFFFFF;
        }

        QMenu::item:disabled {
            color: #AAAAAA;
        }

        QMenu::separator {
            height: 1px;
            background-color: #E0E0E0;
            margin: 5px 0;
        }
        """

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("title_bar")
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 5, 5)
        layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "resources", "icon.png")
        if os.path.exists(icon_path):
            self.icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            self.icon_label.setPixmap(QIcon.fromTheme("system-run").pixmap(24, 24))
        layout.addWidget(self.icon_label)

        self.title = QLabel("Immutable Deepin Tools")
        self.title.setObjectName("title_label")
        layout.addWidget(self.title, 1, Qt.AlignLeft | Qt.AlignVCenter)

        self.theme_button = QPushButton()
        self.theme_button.setObjectName("window_button")
        self.theme_button.setFixedSize(24, 24)
        
        self.update_theme_icon()
        
        self.theme_button.setToolTip("Cambiar tema claro/oscuro")
        self.theme_button.clicked.connect(self.parent.toggle_theme)
        layout.addWidget(self.theme_button, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setObjectName("window_button")
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.setStyleSheet("""
            font-size: 16px;
            padding: 0;
            margin: 0;
        """)
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.minimize_btn, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("window_button")
        self.close_btn.setProperty("id", "close_button")
        self.close_btn.setStyleSheet("""
            font-size: 16px;
            padding: 0;
            margin: 0;
        """)
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.parent.close)
        layout.addWidget(self.close_btn, 0, Qt.AlignRight | Qt.AlignVCenter)

    def update_theme_icon(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if hasattr(self.parent, 'dark_mode') and self.parent.dark_mode:
            icon_path = os.path.join(current_dir, "resources", "sun-mode.png")  
        else:
            icon_path = os.path.join(current_dir, "resources", "black-mode.png") 
        
        if os.path.exists(icon_path):
            self.theme_button.setIcon(QIcon(icon_path))
        else:
            if hasattr(self.parent, 'dark_mode') and self.parent.dark_mode:
                self.theme_button.setIcon(QIcon.fromTheme("weather-clear"))
            else:
                self.theme_button.setIcon(QIcon.fromTheme("weather-clear-night"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self.parent, 'drag_position'):
            self.parent.move(event.globalPosition().toPoint() - self.parent.drag_position)
            event.accept()

class RoundedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(900, 600)

        self.setWindowTitle("Immutable Deepin Tools")
        
        self.setProperty("WM_CLASS", "immutable-deepin-tools") 

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "resources", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            self.setWindowIcon(QIcon.fromTheme("system-run"))

        self.main_widget = QWidget()
        self.main_widget.setObjectName("main_widget")
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("content_widget")
        self.main_layout.addWidget(self.content_widget, 1)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 8, 8)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        super().resizeEvent(event)

class ConsoleOutputDialog(QDialog):
    def __init__(self, parent=None, title_text="Salida de Comandos", controller=None):
        super().__init__(parent)
        self.setWindowTitle(title_text)
        self.setFixedSize(600, 500)  
        
        self.requires_reboot = False
        self.current_command = ""
        self.controller = controller  # Guardamos la referencia al controlador
        
        layout = QVBoxLayout(self)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area, 1)

        self.clear_output()

        self.button_box = QWidget()
        self.button_layout = QHBoxLayout(self.button_box)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.close)
        self.close_button.hide()
        self.button_layout.addWidget(self.close_button)
        
        self.reboot_now_button = QPushButton("Reiniciar Ahora")
        self.reboot_now_button.setObjectName("reboot_button")
        self.reboot_now_button.clicked.connect(self.reboot_system)
        self.reboot_now_button.hide()
        self.button_layout.addWidget(self.reboot_now_button)
        
        self.reboot_later_button = QPushButton("Más Tarde")
        self.reboot_later_button.setObjectName("reboot_button")
        self.reboot_later_button.clicked.connect(self.close)
        self.reboot_later_button.hide()
        self.button_layout.addWidget(self.reboot_later_button)
        
        layout.addWidget(self.button_box)

    def clear_output(self):
        self.output_area.clear()

    def append_output(self, text):
        if text == "":  
            self.clear_output()
            return
            
        self.output_area.append(text)
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.output_area.setTextCursor(cursor)
        self.output_area.ensureCursorVisible()

    def command_finished(self, exit_code):
        if exit_code == 0:
            self.append_output("\n✅ Comando ejecutado con éxito")
        else:
            self.append_output(f"\n❌ Comando terminado con código de error: {exit_code}")
        
        if self.requires_reboot:
            self.append_output("\n⚠️ Se requiere reinicio del sistema para aplicar los cambios")
            self.reboot_now_button.show()
            self.reboot_later_button.show()
            self.close_button.hide()  
        else:
            self.close_button.show()
            self.reboot_now_button.hide()
            self.reboot_later_button.hide()
        
        if not self.isVisible():
            self.show()
            self.raise_()

    def reboot_system(self):
        self.append_output("\n🔄 Iniciando reinicio del sistema...")
        QTimer.singleShot(1000, lambda: self.controller.execute_command("systemctl reboot", show_in_console=False))
        self.close()

class ImmutableController(QObject):
    commandStarted = Signal(str)  
    commandOutput = Signal(str)   
    commandFinished = Signal(int) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.current_command = ""

    def execute_command(self, command, show_in_console=True, env=None):
        try:
            if show_in_console:
                self.commandOutput.emit("") 
                self.commandOutput.emit(f"$ {command}\n")
                self.commandOutput.emit("="*80 + "\n")

            no_root_commands = [
                "deepin-immutable-ctl --immutable-status",
                "deepin-immutable-ctl snapshot list",
                "deepin-immutable-ctl snapshot show"
            ]
            
            needs_root = True
            for cmd in no_root_commands:
                if cmd in command:
                    needs_root = False
                    break
                    
            if needs_root and not command.startswith("pkexec"):
                full_command = f"pkexec {command}"
            else:
                full_command = command

            if not show_in_console:
                process_env = os.environ.copy()
                if env:
                    process_env.update(env)
                    
                process = Popen(full_command, shell=True, stdout=PIPE, stderr=PIPE, env=process_env)
                stdout, stderr = process.communicate()
                output = stdout.decode('utf-8')
                error = stderr.decode('utf-8')

                if error:
                    output += "\n\nERROR:\n" + error
                return output

            self.current_command = full_command
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.handle_finished)
            
            if env:
                process_env = self.process.processEnvironment()
                for key, value in env.items():
                    process_env.insert(key, value)
                self.process.setProcessEnvironment(process_env)
            
            self.process.start("/bin/bash", ["-c", full_command])
            return ""

        except Exception as e:
            error_msg = f"Error ejecutando comando: {str(e)}"
            if show_in_console:
                self.commandOutput.emit(error_msg)
            return error_msg

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.commandOutput.emit(stdout.strip())

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.commandOutput.emit(f"ERROR: {stderr.strip()}")

    def handle_finished(self, exit_code):
        self.commandOutput.emit("\n" + "="*80 + "\n")
        self.commandFinished.emit(exit_code)
        self.process = None

class MainWindow(RoundedWindow):
    def __init__(self):
        super().__init__()
        self.controller = ImmutableController()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        config = ConfigManager.load_config()
        self.dark_mode = config.get("dark_mode", True)
        
        if self.dark_mode:
            self.apply_theme(ThemeManager.dark_theme())
        else:
            self.apply_theme(ThemeManager.light_theme())

        self.console_dialog = ConsoleOutputDialog(self, title_text="Salida de Comandos", controller=self.controller)
        self.controller.commandStarted.connect(lambda x: None)
        self.controller.commandOutput.connect(self.console_dialog.append_output)
        self.controller.commandFinished.connect(self.console_dialog.command_finished)

        self.create_ui()
        self.check_immutable_status()

        self.status_timer = QTimer(self)
        self.status_timer.setInterval(10000)
        self.status_timer.timeout.connect(self.check_immutable_status)
        self.status_timer.start()

    def add_nav_item(self, text, icon_name):
        item = QListWidgetItem(text)
        
        icon_path = os.path.join(self.current_dir, "resources", icon_name)
        
        if os.path.exists(icon_path):
            item.setIcon(QIcon(icon_path))
        else:
            icon_mapping = {
                "Estado": "dialog-information",
                "Administración": "system-run",
                "Snapshots": "document-save",
                "Acerca de": "help-about"
            }
            default_icon = icon_mapping.get(text, "")
            if default_icon:
                item.setIcon(QIcon.fromTheme(default_icon))
        
        self.nav_list.addItem(item)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_theme(ThemeManager.dark_theme())
        else:
            self.apply_theme(ThemeManager.light_theme())
        
        ConfigManager.save_config({"dark_mode": self.dark_mode})
        
        if hasattr(self, 'title_bar') and hasattr(self.title_bar, 'update_theme_icon'):
            self.title_bar.update_theme_icon()
    def apply_theme(self, stylesheet):
        self.setStyleSheet(stylesheet)
        QApplication.instance().setStyleSheet(stylesheet)
        
        if self.dark_mode:
            self.main_widget.setStyleSheet("""
                #main_widget {
                    background-color: #2D2D2D;
                    border-radius: 8px;
                }
                QListWidget::item {
                    padding: 8px 15px;
                }
            """)
        else:
            self.main_widget.setStyleSheet("""
                #main_widget {
                    background-color: #FFFFFF;
                    border-radius: 8px;
                }
                QListWidget::item {
                    padding: 8px 15px;
                }
            """)

    def check_immutable_status(self):
        output = self.controller.execute_command("deepin-immutable-ctl --immutable-status", show_in_console=False)
        is_immutable = "true" in output.lower()

        if is_immutable:
            self.status_label.setText("✔ Sistema en modo inmutable")
            self.status_label.setStyleSheet("color: #2ECC71;")
            self.btn_disable_immutable.setEnabled(True)
            self.btn_enable_immutable.setEnabled(False)
        else:
            self.status_label.setText("✖ Sistema NO está en modo inmutable")
            self.status_label.setStyleSheet("color: #E74C3C;")
            self.btn_disable_immutable.setEnabled(False)
            self.btn_enable_immutable.setEnabled(True)

    def disable_immutable_mode(self):
        self.confirm_action(
            "Confirmar Desactivación de Inmutabilidad",
            "¿Está seguro que desea desactivar el modo inmutable?\n\n"
            "Esto hará que el directorio '/usr' sea escribible, permitiendo modificaciones en el sistema base.\n"
            "Esta acción requiere un reinicio del sistema para aplicar los cambios.\n\n"
            "Esta acción requiere privilegios de root.",
            "pkexec deepin-immutable-writable enable -d /usr -y",
            show_console=True,
            requires_reboot=True
        )

    def enable_immutable_mode(self):
        self.confirm_action(
            "Confirmar Activación de Inmutabilidad",
            "¿Está seguro que desea activar el modo inmutable de nuevo?\n\n"
            "Esto hará que el directorio '/usr' vuelva a ser de solo lectura, protegiendo el sistema base.\n"
            "Esta acción requiere un reinicio del sistema para aplicar los cambios.\n\n"
            "Esta acción requiere privilegios de root.",
            "pkexec deepin-immutable-writable disable -y",
            show_console=True,
            requires_reboot=True
        )

    def run_command(self, command, show_in_console=True):
        self.controller.execute_command(command, show_in_console=show_in_console)

    def confirm_action(self, title, message, command, show_console=True, requires_reboot=False):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setButtonText(QMessageBox.Yes, "Sí")
        msg_box.setButtonText(QMessageBox.No, "No")
        
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setStyleSheet(QApplication.instance().styleSheet())

        reply = msg_box.exec()

        if reply == QMessageBox.Yes:
            if show_console:
                self.console_dialog.requires_reboot = requires_reboot
                self.console_dialog.current_command = command
                self.run_command(command, show_in_console=show_console)
            else:
                output = self.controller.execute_command(command, show_in_console=False)
                
            if "snapshot" in command:
                self.refresh_snapshots()
            elif "immutable-status" not in command and ("deploy" in command or "rollback" in command):
                self.check_immutable_status()
            elif "immutable-writable" in command:
                self.check_immutable_status()

    def create_ui(self):
        main_content_layout = QHBoxLayout(self.content_widget)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(0)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("nav_list")
        self.nav_list.setFixedWidth(200)
        
        self.add_nav_item("Estado", "status.png")
        self.add_nav_item("Administración", "admin.png")
        self.add_nav_item("Snapshots", "snapshot.png")
        self.add_nav_item("Acerca de", "about.png")
        self.nav_list.setCurrentRow(0)
        main_content_layout.addWidget(self.nav_list)

        self.content_stack = QStackedWidget()
        main_content_layout.addWidget(self.content_stack, 1)

        self.create_status_page()
        self.load_admin_tab()
        self.load_snapshots_tab()
        self.create_about_page()

        self.nav_list.currentRowChanged.connect(self.content_stack.setCurrentIndex)

    def add_nav_item(self, text, icon_name):
        item = QListWidgetItem(text)
        
        icon_path = os.path.join(self.current_dir, "resources", icon_name)
        
        if os.path.exists(icon_path):
            item.setIcon(QIcon(icon_path))
        else:
            icon_mapping = {
                "Estado": "dialog-information",
                "Administración": "system-run",
                "Snapshots": "document-save"
            }
            default_icon = icon_mapping.get(text, "")
            if default_icon:
                item.setIcon(QIcon.fromTheme(default_icon))
        
        self.nav_list.addItem(item)

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        icon_path = os.path.join(self.current_dir, "resources", "icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(64, 64))
            header_layout.addWidget(icon_label)
        else:
            icon_label = QLabel()
            icon_label.setPixmap(QIcon.fromTheme("system-run").pixmap(64, 64))
            header_layout.addWidget(icon_label)
        
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        title = QLabel("Immutable Deepin Tools")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(title, 0, Qt.AlignVCenter)
        
        subtitle = QLabel("Desarrollado por la comunidad de Deepin en Español.")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: bold;
                color: #3D60E3;
            }
        """)
        subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(subtitle, 0, Qt.AlignVCenter)
        
        title_layout.addStretch()
        
        header_layout.addWidget(title_container)
        header_layout.addStretch(1)
        
        layout.addLayout(header_layout)
        
        version = QLabel("Versión: 1.0.3")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        layout.addWidget(self.create_separator())
        
        link_style = "style='color:#2ECC71; text-decoration:none;'"
        hover_style = "onmouseover=\"this.style.color='#27AE60'; this.style.textDecoration='underline'\" " \
                    "onmouseout=\"this.style.color='#2ECC71'; this.style.textDecoration='none'\""

        developer = QLabel(f"""
            <b>Desarrollador:</b><br>
            krafairus - <a href='https://xn--deepinenespaol-1nb.org/participant/krafairus' {link_style} {hover_style}>deepines.com/participant/krafairus</a>
        """)
        developer.setOpenExternalLinks(True)
        developer.setWordWrap(True)
        layout.addWidget(developer)
        
        link_style = "style='color:#2ECC71; text-decoration:none;'"
        hover_style = "onmouseover=\"this.style.color='#27AE60'; this.style.textDecoration='underline'\" " \
                    "onmouseout=\"this.style.color='#2ECC71'; this.style.textDecoration='none'\""

        beta_testers = QLabel(f"""
            <b>Beta Testers:</b><br>
            Guysho2112 - <a href='https://xn--deepinenespaol-1nb.org/participant/Guysho2112/' {link_style} {hover_style}>deepines.com/participant/Guysho2112/</a>
        """)
        beta_testers.setOpenExternalLinks(True)
        beta_testers.setWordWrap(True)
        layout.addWidget(beta_testers)

        community = QLabel(f"""
            <b>Comunidad deepin en español:</b><br>
            <a href='https://xn--deepinenespaol-1nb.org' {link_style} {hover_style}>www.deepines.com</a>
        """)
        community.setOpenExternalLinks(True)
        community.setWordWrap(True)
        layout.addWidget(community)
        
        repo = QLabel(f"""
            <b>Repositorio:</b><br>
            <a href='https://github.com/krafairus/immutable-deepin-tools' {link_style} {hover_style}>https://github.com/krafairus/immutable-deepin-tools</a>
        """)
        repo.setOpenExternalLinks(True)
        repo.setWordWrap(True)
        layout.addWidget(repo)
        
        layout.addStretch(1)
        self.content_stack.addWidget(page)

    def create_status_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        status_group = QGroupBox("Estado Actual del Sistema Inmutable")
        status_group_layout = QVBoxLayout(status_group)
        self.status_label = QLabel("Cargando estado...")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_group_layout.addWidget(self.status_label)

        btn_check_status = QPushButton("Actualizar Estado")
        btn_check_status.clicked.connect(self.check_immutable_status)
        status_group_layout.addWidget(btn_check_status, alignment=Qt.AlignCenter)

        status_group_layout.addWidget(self.create_separator())

        immutable_toggle_layout = QHBoxLayout()
        self.btn_disable_immutable = QPushButton("Desactivar Inmutabilidad")
        self.btn_disable_immutable.setStyleSheet("""
            QPushButton { background-color: #E74C3C; color: white; }
            QPushButton:hover { background-color: #C0392B; }
            QPushButton:pressed { background-color: #A93226; }
            QPushButton:disabled { background-color: #555555; color: #777777; }
        """)
        self.btn_disable_immutable.clicked.connect(self.disable_immutable_mode)
        immutable_toggle_layout.addWidget(self.btn_disable_immutable)

        self.btn_enable_immutable = QPushButton("Activar Inmutabilidad")
        self.btn_enable_immutable.setStyleSheet("""
            QPushButton { background-color: #2ECC71; color: white; }
            QPushButton:hover { background-color: #27AE60; }
            QPushButton:pressed { background-color: #1E8449; }
            QPushButton:disabled { background-color: #555555; color: #777777; }
        """)
        self.btn_enable_immutable.clicked.connect(self.enable_immutable_mode)
        immutable_toggle_layout.addWidget(self.btn_enable_immutable)

        status_group_layout.addLayout(immutable_toggle_layout)

        immutable_info_label = QLabel(
            "Al desactivar la inmutabilidad, el directorio `/usr` se vuelve escribible, permitiendo la instalación de software y modificaciones directas en el sistema base. "
            "Esto es útil para desarrolladores o usuarios avanzados, pero reduce la seguridad y estabilidad del sistema inmutable."
            "<br><br>"
            "Al activar la inmutabilidad, `/usr` vuelve a ser de solo lectura, protegiendo el sistema base de cambios no deseados."
        )
        immutable_info_label.setWordWrap(True)
        status_group_layout.addWidget(immutable_info_label)

        layout.addWidget(status_group)
        layout.addStretch(1)

        self.content_stack.addWidget(page)

    def load_admin_tab(self):
        """Carga dinámicamente la pestaña de administración desde el módulo externo"""
        try:
            admin_path = os.path.join(self.current_dir, "resources", "admin.py")
            
            if os.path.exists(admin_path):
                spec = importlib.util.spec_from_file_location("admin", admin_path)
                admin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(admin_module)
                
                admin_tab = admin_module.AdminTab(self.controller, self)
                self.content_stack.addWidget(admin_tab)
            else:
                print(f"Advertencia: No se encontró el módulo admin.py en {admin_path}")
                placeholder = QLabel("Módulo de administración no encontrado")
                placeholder.setAlignment(Qt.AlignCenter)
                self.content_stack.addWidget(placeholder)
        except Exception as e:
            print(f"Error al cargar el módulo de administración: {str(e)}")
            error_widget = QLabel(f"Error al cargar la administración:\n{str(e)}")
            error_widget.setAlignment(Qt.AlignCenter)
            self.content_stack.addWidget(error_widget)

    def load_snapshots_tab(self):
        try:
            snapshots_path = os.path.join(self.current_dir, "resources", "snapshots.py")
            
            if os.path.exists(snapshots_path):
                spec = importlib.util.spec_from_file_location("snapshots", snapshots_path)
                snapshots_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(snapshots_module)
                
                snapshots_tab = snapshots_module.SnapshotsTab(self.controller, self)
                self.content_stack.addWidget(snapshots_tab)  
            else:
                print(f"Advertencia: No se encontró el módulo snapshots.py en {snapshots_path}")
                placeholder = QLabel("Módulo de Snapshots no encontrado")
                placeholder.setAlignment(Qt.AlignCenter)
                self.content_stack.addWidget(placeholder)
        except Exception as e:
            print(f"Error al cargar el módulo de Snapshots: {str(e)}")
            error_widget = QLabel(f"Error al cargar Snapshots:\n{str(e)}")
            error_widget.setAlignment(Qt.AlignCenter)
            self.content_stack.addWidget(error_widget)

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedHeight(2)
        if self.dark_mode:
            separator.setStyleSheet("background-color: #444444; border: none;")
        else:
            separator.setStyleSheet("background-color: #DDDDDD; border: none;")
        return separator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
