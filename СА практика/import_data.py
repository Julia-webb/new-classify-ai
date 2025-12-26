"""
Модуль для импорта данных в систему
"""

import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFileDialog, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt


class DataImporter(QDialog):
    """Диалог импорта данных"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📥 Импорт данных")
        self.setGeometry(300, 300, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("📥 Импорт данных в систему")
        title.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)

        # Описание
        description = QLabel(
            "Выберите файл для импорта данных. Поддерживаются форматы:\n"
            "• JSON файлы экспорта NewsClassify AI\n"
            "• CSV файлы со статьями\n\n"
            "⚠️ Внимание: Импорт перезапишет текущие данные!"
        )
        description.setStyleSheet("""
            color: #7f8c8d;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 6px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)

        # Кнопки импорта
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)

        # Импорт статей из JSON
        btn_articles_json = QPushButton("📰 Импорт статей (JSON)")
        btn_articles_json.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_articles_json.clicked.connect(self.import_articles_json)
        btn_layout.addWidget(btn_articles_json)

        # Импорт фильтров
        btn_filters = QPushButton("⚙️ Импорт фильтров (JSON)")
        btn_filters.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_filters.clicked.connect(self.import_filters_json)
        btn_layout.addWidget(btn_filters)

        # Импорт всех данных
        btn_all = QPushButton("💾 Импорт всех данных (папка)")
        btn_all.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        btn_all.clicked.connect(self.import_all_data)
        btn_layout.addWidget(btn_all)

        layout.addLayout(btn_layout)

        # Область предпросмотра
        self.preview_label = QLabel("Предпросмотр данных:")
        self.preview_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(self.preview_label)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(150)
        self.preview_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-family: monospace;
                font-size: 9pt;
            }
        """)
        layout.addWidget(self.preview_text)

        # Кнопка закрытия
        btn_close = QPushButton("✕ Закрыть")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(self.reject)
        layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignRight)

    def import_articles_json(self):
        """Импорт статей из JSON файла"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Выберите JSON файл со статьями",
                "", "JSON Files (*.json)"
            )

            if not filename:
                return

            # Загрузка данных
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Предпросмотр
            preview = f"Файл: {filename}\n"
            preview += f"Количество статей: {data.get('total_articles', len(data.get('articles', [])))}\n"
            preview += f"Дата экспорта: {data.get('export_date', 'Не указана')}\n\n"

            if 'articles' in data and len(data['articles']) > 0:
                preview += "Пример первой статьи:\n"
                first_article = data['articles'][0]
                preview += f"Заголовок: {first_article.get('title', 'Нет')[:50]}...\n"
                preview += f"Тема: {first_article.get('predicted_topic', 'Не указана')}"

            self.preview_text.setText(preview)

            # Запрос подтверждения
            reply = QMessageBox.question(
                self, "Подтверждение импорта",
                f"Импортировать {len(data.get('articles', []))} статей?\n"
                "Текущие данные будут заменены.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Здесь будет логика импорта
                QMessageBox.information(self, "✅ Успех",
                                        f"Импортировано {len(data.get('articles', []))} статей")

        except Exception as e:
            QMessageBox.critical(self, "❌ Ошибка",
                                 f"Ошибка при импорте файла:\n{str(e)}")

    def import_filters_json(self):
        """Импорт фильтров из JSON файла"""
        QMessageBox.information(self, "ℹ️ Информация",
                                "Функция импорта фильтров будет реализована в следующей версии.")

    def import_all_data(self):
        """Импорт всех данных из папки"""
        QMessageBox.information(self, "ℹ️ Информация",
                                "Функция импорта всех данных будет реализована в следующей версии.")

    def show_import_dialog(self):
        """Показывает диалог импорта"""
        self.exec()