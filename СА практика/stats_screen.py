from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QGroupBox,
                             QGridLayout, QProgressBar, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QScrollArea)  # ← ДОБАВИЛИ QScrollArea
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QFont
import random

from mock_data_news import mock_data


class StatsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_auto_refresh()
        self.update_stats()

    def init_ui(self):
        # СОЗДАЕМ ПРОКРУЧИВАЕМУЮ ОБЛАСТЬ
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f7fa;
            }
            QScrollBar:vertical {
                border: none;
                background: #ecf0f1;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #2980b9;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Основной виджет для контента
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("📊 Аналитика системы")
        title.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        """)
        self.layout.addWidget(title)

        # Четыре карточки с метриками
        self.metrics_layout = QGridLayout()
        self.metrics_layout.setSpacing(15)

        # СОЗДАЕМ КАРТОЧКИ КАК АТРИБУТЫ КЛАССА
        self.card1 = self.create_metric_card("🎯 Точность", "87.3%",
                                             "Средняя точность классификации", "#27ae60")
        self.metrics_layout.addWidget(self.card1, 0, 0)

        self.card2 = self.create_metric_card("📰 Статьи", str(len(mock_data.articles)),
                                             "Всего обработано", "#3498db")
        self.metrics_layout.addWidget(self.card2, 0, 1)

        self.card3 = self.create_metric_card("✏️ Исправления",
                                             str(mock_data.classification_stats['corrected_count']),
                                             "Коррекций пользователя", "#9b59b6")
        self.metrics_layout.addWidget(self.card3, 1, 0)

        self.card4 = self.create_metric_card("🛡️ Надежность", "99.8%",
                                             "Стабильность работы", "#e74c3c")
        self.metrics_layout.addWidget(self.card4, 1, 1)

        self.layout.addLayout(self.metrics_layout)

        # Точность по темам
        topics_group = QGroupBox("🎯 Точность по темам")
        topics_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3498db;
                border-radius: 8px;
                padding-top: 15px;
                background-color: white;
                margin-top: 10px;
            }
        """)

        topics_layout = QVBoxLayout(topics_group)

        self.topic_bars = {}
        for topic in mock_data.available_topics:
            topic_widget = QWidget()
            topic_widget.setFixedHeight(35)
            topic_layout = QHBoxLayout(topic_widget)
            topic_layout.setContentsMargins(5, 0, 5, 0)

            # Название темы
            name_label = QLabel(topic)
            name_label.setFixedWidth(100)

            # Прогресс-бар
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setTextVisible(False)
            bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #f5f5f5;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    border-radius: 4px;
                }
            """)

            # Значение
            value_label = QLabel("0%")
            value_label.setFixedWidth(40)

            topic_layout.addWidget(name_label)
            topic_layout.addWidget(bar)
            topic_layout.addWidget(value_label)

            topics_layout.addWidget(topic_widget)
            self.topic_bars[topic] = (bar, value_label)

        self.layout.addWidget(topics_group)

        # История коррекций
        history_group = QGroupBox("📝 Последние коррекции")
        history_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #9b59b6;
                border-radius: 8px;
                padding-top: 15px;
                background-color: white;
                margin-top: 10px;
            }
        """)

        history_layout = QVBoxLayout(history_group)

        # Таблица коррекций
        self.corrections_table = QTableWidget(5, 3)
        self.corrections_table.setHorizontalHeaderLabels(["Статья", "Было", "Стало"])

        # Устанавливаем ширину столбцов
        self.corrections_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.corrections_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.corrections_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.corrections_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)

        history_layout.addWidget(self.corrections_table)
        self.layout.addWidget(history_group)

        # Кнопка обновления
        self.refresh_btn = QPushButton("🔄 Обновить статистику")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.update_stats)
        self.layout.addWidget(self.refresh_btn)

        self.layout.addStretch()

        # Устанавливаем контент в прокручиваемую область
        scroll_area.setWidget(content_widget)

        # Основной layout для этого экрана
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(scroll_area)

    def create_metric_card(self, title, value, description, color):
        """Создает карточку с метрикой"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border: 2px solid {color};
                padding: 15px;
            }}
        """)

        card_layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        # СОХРАНЯЕМ value_label как атрибут для обновления
        value_label = QLabel(value)
        value_label.setObjectName(f"value_{title}")  # задаем имя для поиска
        value_label.setStyleSheet("font-size: 20pt; font-weight: bold;")

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #7f8c8d; font-size: 10pt;")

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addWidget(desc_label)

        return card

    def update_metric_card(self, card_index, new_value):
        """Обновляет значение в карточке метрики"""
        # Находим карточку
        if card_index == 0:  # Точность
            card = self.card1
        elif card_index == 1:  # Статьи
            card = self.card2
        elif card_index == 2:  # Исправления
            card = self.card3
        elif card_index == 3:  # Надежность
            card = self.card4
        else:
            return

        # Находим QLabel с значением внутри карточки
        value_label = card.findChild(QLabel, "value_")  # ищем по части имени
        if not value_label:
            # Ищем второй QLabel в карточке (первый - заголовок, второй - значение)
            labels = card.findChildren(QLabel)
            if len(labels) > 1:
                value_label = labels[1]  # второй QLabel это значение

        if value_label:
            value_label.setText(str(new_value))

    def setup_auto_refresh(self):
        """Настраивает автоматическое обновление статистики"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(30000)  # Обновление каждые 30 секунд

    def update_stats(self):
        """Обновляет отображение статистики"""
        # 1. Обновляем карточку со статьями
        self.update_metric_card(1, str(len(mock_data.articles)))

        # 2. Обновляем карточку с исправлениями
        self.update_metric_card(2, str(mock_data.classification_stats['corrected_count']))

        # 3. Обновляем прогресс-бары для тем
        for topic, (bar, label) in self.topic_bars.items():
            # Базовая точность + случайное изменение для реалистичности
            base_accuracy = mock_data.classification_stats['precision']
            variation = random.uniform(-0.08, 0.12)
            topic_accuracy = min(98, max(65, int((base_accuracy + variation) * 100)))

            bar.setValue(topic_accuracy)
            label.setText(f"{topic_accuracy}%")

            # Цвет текста в зависимости от точности
            if topic_accuracy > 85:
                label.setStyleSheet("font-weight: bold; color: #27ae60;")
            elif topic_accuracy > 75:
                label.setStyleSheet("font-weight: bold; color: #f39c12;")
            else:
                label.setStyleSheet("font-weight: bold; color: #e74c3c;")

        # 4. Обновляем таблицу коррекций
        self.corrections_table.setRowCount(0)

        # Берем последние 5 коррекций
        recent = mock_data.correction_history[-5:] if mock_data.correction_history else []

        for i, correction in enumerate(recent):
            self.corrections_table.insertRow(i)

            # Статья
            title_item = QTableWidgetItem(correction["title"])

            # Старая тема
            old_item = QTableWidgetItem(correction["old_topic"])
            old_item.setForeground(QColor("#e74c3c"))

            # Новая тема
            new_item = QTableWidgetItem(correction["new_topic"])
            new_item.setForeground(QColor("#27ae60"))

            self.corrections_table.setItem(i, 0, title_item)
            self.corrections_table.setItem(i, 1, old_item)
            self.corrections_table.setItem(i, 2, new_item)

            # 5. Анимация кнопки обновления
            self.refresh_btn.setText("🔄 Обновление...")
            self.refresh_btn.setEnabled(False)

            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self.refresh_btn.setText("🔄 Обновить статистику"))
            QTimer.singleShot(1000, lambda: self.refresh_btn.setEnabled(True))

            # ДОБАВЛЕНО: Обновляем живую статистику в навигации
            try:
                # Получаем главное окно
                parent = self.parent()
                while parent and not isinstance(parent, QMainWindow):
                    parent = parent.parent()

                if parent and hasattr(parent, 'update_live_stats'):
                    parent.update_live_stats()
            except Exception as e:
                print(f"⚠️ Не удалось обновить навигационную статистику: {e}")

            print(f"📊 Статистика обновлена: {len(mock_data.articles)} статей, "
                  f"{mock_data.classification_stats['corrected_count']} коррекций")