#!/usr/bin/env python3

import os
import sys
import json
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
            background-color: #0081FF;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            min-width: 120px;
            font-size: 13px;
            font-weight: bold;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #006BB3;
        }
        QPushButton:pressed {
            background-color: #004A77;
        }
        QPushButton:disabled {
            background-color: #333333;
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

        /* Grupos */
        QGroupBox {
            background-color: #FFFFFF;
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
            background-color: #F5F5F5;
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
    def __init__(self, parent=None, title_text="Salida de Comandos"):
        super().__init__(parent)
        self.setWindowTitle(title_text)
        self.setFixedSize(600, 500)  
        
        self.requires_reboot = False
        self.current_command = ""
        
        layout = QVBoxLayout(self)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area, 1)
        
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

    def append_output(self, text):
        self.output_area.append(text)
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.output_area.setTextCursor(cursor)
        self.output_area.ensureCursorVisible()
        
        if not self.isVisible():
            self.show()
            self.raise_()

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
        QTimer.singleShot(1000, lambda: self.controller.execute_command("pkexec systemctl reboot", show_in_console=False))
        self.close()

class ImmutableController(QObject):
    commandStarted = Signal(str)  
    commandOutput = Signal(str)   
    commandFinished = Signal(int) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.current_command = ""

    def execute_command(self, command, show_in_console=True):
        try:
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
                    
            # Comandos que SIEMPRE usan deepin-immutable-ctl admin exec
            if "deepin-immutable-ctl admin exec" in command:
                needs_root = True
                command = command.replace("pkexec ", "")

            if needs_root and not command.startswith("pkexec"):
                full_command = f"pkexec {command}"
            else:
                full_command = command

            if not show_in_console:
                process = Popen(full_command, shell=True, stdout=PIPE, stderr=PIPE)
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
            
            if show_in_console:
                self.commandStarted.emit(f"$ {full_command}\n")
            
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

        self.dark_mode = True
        self.apply_theme(ThemeManager.dark_theme())

        self.console_dialog = ConsoleOutputDialog(self)
        self.controller.commandStarted.connect(self.console_dialog.append_output)
        self.controller.commandOutput.connect(self.console_dialog.append_output)
        self.controller.commandFinished.connect(self.console_dialog.command_finished)

        self.create_ui()
        self.refresh_snapshots()
        self.check_immutable_status()

        self.status_timer = QTimer(self)
        self.status_timer.setInterval(10000)
        self.status_timer.timeout.connect(self.check_immutable_status)
        self.status_timer.start()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_theme(ThemeManager.dark_theme())
        else:
            self.apply_theme(ThemeManager.light_theme())
        
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

    def refresh_snapshots(self):
        self.snapshot_list.clear()
        output = self.controller.execute_command("deepin-immutable-ctl snapshot list", show_in_console=False)

        lines = output.split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        snapshot_id = parts[0]
                        name = parts[1]
                        time = ' '.join(parts[2:4]) if len(parts) >= 4 else ''
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

    def confirm_deploy(self):
        self.confirm_action(
            "Confirmar Despliegue",
            "¿Está seguro que desea desplegar los cambios al sistema? Esto requiere un reinicio.",
            "pkexec deepin-immutable-ctl admin deploy",
            show_console=True
        )

    def confirm_finalize(self):
        self.confirm_action(
            "Confirmar Finalización",
            "¿Está seguro que desea finalizar el despliegue actual?\nEsto eliminará las modificaciones sobre el sistema base y requiere un reinicio.",
            "pkexec deepin-immutable-ctl admin deploy --finalize",
            show_console=True
        )

    def confirm_rollback(self):
        self.confirm_action(
            "Confirmar Reversión",
            "¿Está seguro que desea revertir al sistema anterior? Esto requiere un reinicio.",
            "pkexec deepin-immutable-ctl admin rollback",
            show_console=True
        )

    def confirm_delete_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                "Confirmar Eliminación",
                f"¿Está seguro que desea eliminar el snapshot {snapshot_id}?",
                f'pkexec deepin-immutable-ctl snapshot delete "{snapshot_id}"',
                show_console=True
            )

    def confirm_revert_snapshot(self):
        snapshot_id = self.get_selected_snapshot_id()
        if snapshot_id:
            self.confirm_action(
                "Confirmar Reversión de Snapshot",
                f"¡ADVERTENCIA!\n\nAl revertir al snapshot '{snapshot_id}', se perderán todos los cambios realizados en el sistema después de la creación de ese snapshot.\n\nEsta operación NO se puede deshacer y requerirá un reinicio inmediato del equipo para aplicar los cambios.\n\n¿Desea continuar?",
                f'pkexec deepin-immutable-ctl snapshot rollback "{snapshot_id}"',
                show_console=True
            )

    def show_create_snapshot_dialog(self):
        text, ok = QInputDialog.getText(self, "Crear Snapshot",
                                     "Introduce un nombre para el snapshot (opcional):",
                                     QLineEdit.Normal, "")
        if ok:
            description, ok_desc = QInputDialog.getText(self, "Crear Snapshot",
                                                     "Introduce una descripción (opcional):",
                                                     QLineEdit.Normal, "")
            if ok_desc:
                command = "pkexec deepin-immutable-ctl snapshot create"
                if text:
                    command += f' --name="{text}"'
                if description:
                    command += f' --description="{description}"'
                self.confirm_action("Confirmar Creación de Snapshot",
                                    f"¿Está seguro que desea crear un snapshot con nombre '{text}' y descripción '{description}'?",
                                    command,
                                    show_console=True)

    def show_modify_snapshot_dialog(self):
        snapshot_id = self.get_selected_snapshot_id()
        if not snapshot_id:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un snapshot para modificar.")
            return

        name, ok_name = QInputDialog.getText(self, "Modificar Snapshot",
                                           f"Nuevo nombre para el snapshot {snapshot_id} (dejar en blanco para no cambiar):",
                                           QLineEdit.Normal, "")
        if ok_name:
            description, ok_desc = QInputDialog.getText(self, "Modificar Snapshot",
                                                       f"Nueva descripción para el snapshot {snapshot_id} (dejar en blanco para no cambiar):",
                                                       QLineEdit.Normal, "")
            if ok_desc:
                command_parts = [f'pkexec deepin-immutable-ctl snapshot modify "{snapshot_id}"']
                if name:
                    command_parts.append(f'--set-name="{name}"')
                if description:
                    command_parts.append(f'--set-description="{description}"')

                if len(command_parts) > 1:
                    self.confirm_action("Confirmar Modificación de Snapshot",
                                        f"¿Está seguro que desea modificar el snapshot {snapshot_id}?",
                                        " ".join(command_parts),
                                        show_console=True)
                else:
                    QMessageBox.information(self, "Información", "No se especificaron cambios para el snapshot.")

    def show_exec_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ejecutar Comando (admin)")
        dialog.setFixedSize(600, 450)

        layout = QVBoxLayout(dialog)

        form = QFormLayout()
        cmd_input = QLineEdit()
        cmd_input.setPlaceholderText("ej: apt update && apt upgrade -y")
        form.addRow("Comando:", cmd_input)
        layout.addLayout(form)

        common_commands_group = QGroupBox("Comandos comunes")
        common_commands_layout = QGridLayout(common_commands_group)
        
        common_commands = [
            ("apt update", "apt update"),
            ("apt upgrade", "apt upgrade -y"),
            ("apt install", "apt install "),
            ("apt remove", "apt remove "),
            ("apt autoremove", "apt autoremove -y"),
            ("apt clean", "apt clean")
        ]
        
        row, col = 0, 0
        for text, command in common_commands:
            btn = QPushButton(text)
            btn.setObjectName("common_command_button")
            btn.clicked.connect(lambda _, cmd=command: cmd_input.setText(cmd))
            common_commands_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        layout.addWidget(common_commands_group)

        buttons = QHBoxLayout()
        btn_ok = QPushButton("Ejecutar")
        btn_ok.clicked.connect(lambda: self.confirm_action(
            "Confirmar Ejecución",
            f"¿Está seguro que desea ejecutar el comando:\n\n{cmd_input.text()}?",
            f"deepin-immutable-ctl admin exec -- {cmd_input.text()}",
            show_console=True
        ))
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(dialog.reject)
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        dialog.exec()

    def show_file_op_dialog(self):
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
        self.create_admin_page()
        self.create_snapshot_page()
        self.create_about_page()

        self.nav_list.currentRowChanged.connect(self.content_stack.setCurrentIndex)

    def add_nav_item(self, text, icon_name):
        item = QListWidgetItem(text)
        
        icon_path = os.path.join(self.current_dir, "resources", icon_name)
        
        # Establecer el icono si existe, o usar uno por defecto
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

        # Contenedor para el icono y título
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Obtener el icono de la aplicación
        icon_path = os.path.join(self.current_dir, "resources", "icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(64, 64))
            header_layout.addWidget(icon_label)
        else:
            # Si no existe el icono, usar uno por defecto
            icon_label = QLabel()
            icon_label.setPixmap(QIcon.fromTheme("system-run").pixmap(64, 64))
            header_layout.addWidget(icon_label)
        
        # Contenedor vertical para el título y subtítulo
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # Título principal
        title = QLabel("Immutable Deepin Tools")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(title, 0, Qt.AlignVCenter)
        
        # Subtítulo con color diferente
        subtitle = QLabel("Herramienta no oficial del equipo de deepin, desarrollado por la comunidad.")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: bold;
                color: #3D60E3;
            }
        """)
        subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(subtitle, 0, Qt.AlignVCenter)
        
        # Añadir espacio flexible para centrar verticalmente
        title_layout.addStretch()
        
        header_layout.addWidget(title_container)
        header_layout.addStretch(1)
        
        layout.addLayout(header_layout)
        
        version = QLabel("Versión: 1.0.1")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        layout.addWidget(self.create_separator())
        
        maintainers = QLabel("""
            <b>Mantenedores:</b><br>
            krafairus - <a href="https://xn--deepinenespaol-1nb.org/participant/krafairus">https://xn--deepinenespaol-1nb.org/participant/krafairus</a>
        """)
        maintainers.setOpenExternalLinks(True)
        maintainers.setWordWrap(True)
        layout.addWidget(maintainers)
        
        community = QLabel("""
            <b>Comunidad deepin en español:</b><br>
            <a href="https://xn--deepinenespaol-1nb.org">https://xn--deepinenespaol-1nb.org</a>
        """)
        community.setOpenExternalLinks(True)
        community.setWordWrap(True)
        layout.addWidget(community)
        
        repo = QLabel("""
            <b>Repositorio:</b><br>
            <a href="https://github.com/krafairus/immutable-deepin-tools">https://github.com/krafairus/immutable-deepin-tools</a>
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

    def create_admin_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        admin_group_actions = QGroupBox("Acciones de Administración")
        admin_group_layout = QVBoxLayout(admin_group_actions)

        btn_deploy = QPushButton("Desplegar Cambios")
        btn_deploy.clicked.connect(self.confirm_deploy)
        admin_group_layout.addWidget(btn_deploy)

        btn_finalize = QPushButton("Finalizar Despliegue")
        btn_finalize.clicked.connect(self.confirm_finalize)
        admin_group_layout.addWidget(btn_finalize)

        btn_rollback = QPushButton("Revertir al Anterior")
        btn_rollback.clicked.connect(self.confirm_rollback)
        admin_group_layout.addWidget(btn_rollback)

        admin_group_layout.addWidget(self.create_separator())

        btn_exec_command = QPushButton("Ejecutar Comando (admin)")
        btn_exec_command.clicked.connect(self.show_exec_dialog)
        admin_group_layout.addWidget(btn_exec_command)

        btn_file_op = QPushButton("Operación de Archivos (admin)")
        btn_file_op.clicked.connect(self.show_file_op_dialog)
        admin_group_layout.addWidget(btn_file_op)

        layout.addWidget(admin_group_actions)
        layout.addStretch(1)

        self.content_stack.addWidget(page)

    def create_snapshot_page(self):
        page = QWidget()
        snapshot_main_layout = QHBoxLayout(page)
        snapshot_main_layout.setContentsMargins(20, 20, 20, 20)
        snapshot_main_layout.setSpacing(15)

        snapshot_list_container = QGroupBox("Gestión de Snapshots")
        snapshot_list_layout = QVBoxLayout(snapshot_list_container)

        self.snapshot_list = QListWidget()
        self.snapshot_list.itemSelectionChanged.connect(self.enable_snapshot_buttons)
        snapshot_list_layout.addWidget(self.snapshot_list)

        snapshot_action_buttons_layout = QHBoxLayout()
        snapshot_action_buttons_layout.setSpacing(10)

        btn_create = QPushButton("Crear")
        btn_create.setObjectName("btn_create_snapshot")
        btn_create.clicked.connect(self.show_create_snapshot_dialog)
        snapshot_action_buttons_layout.addWidget(btn_create)

        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.setObjectName("btn_delete_snapshot")
        self.btn_delete.clicked.connect(self.confirm_delete_snapshot)
        self.btn_delete.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_delete)

        self.btn_show = QPushButton("")
        self.btn_show.setObjectName("btn_show_snapshot")
        show_icon_path = os.path.join(self.current_dir, "resources", "info.png")
        if os.path.exists(show_icon_path):
            self.btn_show.setIcon(QIcon(show_icon_path))
        else:
            self.btn_show.setText("Info")
        self.btn_show.setToolTip("Mostrar Información del Snapshot")
        self.btn_show.clicked.connect(lambda: self.run_command(f'deepin-immutable-ctl snapshot show "{self.get_selected_snapshot_id()}"', show_in_console=True) if self.get_selected_snapshot_id() else None)
        self.btn_show.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_show)

        self.btn_modify = QPushButton("")
        self.btn_modify.setObjectName("btn_modify_snapshot")
        modify_icon_path = os.path.join(self.current_dir, "resources", "edit.png")
        if os.path.exists(modify_icon_path):
            self.btn_modify.setIcon(QIcon(modify_icon_path))
        else:
            self.btn_modify.setText("Mod.")
        self.btn_modify.setToolTip("Modificar Snapshot")
        self.btn_modify.clicked.connect(self.show_modify_snapshot_dialog)
        self.btn_modify.setEnabled(False)
        snapshot_action_buttons_layout.addWidget(self.btn_modify)

        btn_refresh = QPushButton()
        btn_refresh.setObjectName("btn_refresh_list")
        btn_refresh.setFixedSize(32, 32)  
        btn_refresh.setIconSize(QSize(24, 24))  
        
        refresh_icon_path = os.path.join(self.current_dir, "resources", "refresh.png")
        if os.path.exists(refresh_icon_path):
            btn_refresh.setIcon(QIcon(refresh_icon_path))
        else:
            btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        btn_refresh.setToolTip("Refrescar Lista de Snapshots")
        btn_refresh.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        btn_refresh.clicked.connect(self.refresh_snapshots)
        snapshot_action_buttons_layout.addWidget(btn_refresh)

        snapshot_list_layout.addLayout(snapshot_action_buttons_layout)
        snapshot_main_layout.addWidget(snapshot_list_container, 2)

        revert_group = QGroupBox("Revertir Sistema a Snapshot")
        revert_layout = QVBoxLayout(revert_group)
        revert_layout.setSpacing(10)

        self.btn_revert = QPushButton("Revertir Ahora")
        self.btn_revert.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 15px 25px;
                min-width: 150px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #AAAAAA;
            }
        """)
        self.btn_revert.clicked.connect(self.confirm_revert_snapshot)
        self.btn_revert.setEnabled(False)
        revert_layout.addWidget(self.btn_revert, alignment=Qt.AlignCenter)

        revert_explanation = QLabel(
            "Revertir el sistema a un snapshot restaurará el estado del sistema al momento en que se creó ese snapshot. "
            "Esto eliminará permanentemente todos los cambios realizados posteriormente. "
            "Esta operación es irreversible y requerirá un reinicio inmediato del equipo."
        )
        revert_explanation.setWordWrap(True)
        revert_explanation.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        revert_layout.addWidget(revert_explanation)

        info_link = QLabel('<a href="https://bbs.deepin.org/en/post/289441">Más información sobre el sistema inmutable</a>')
        info_link.setOpenExternalLinks(True)
        info_link.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        revert_layout.addWidget(info_link)

        revert_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        revert_group.setMinimumWidth(280)
        snapshot_main_layout.addWidget(revert_group, 1)

        self.content_stack.addWidget(page)

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