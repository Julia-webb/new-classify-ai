from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QComboBox,
                             QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from mock_data_news import mock_data


class ArticleCard(QFrame):
    # Сигнал для обновления интерфейса
    article_corrected = pyqtSignal(int)  # Передает ID статьи

    def __init__(self, article_data):
        super().__init__()
        self.article_data = article_data
        self.is_corrected = False
        self.init_ui()

    def init_ui(self):
        self.setMinimumHeight(270)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setStyleSheet("""
            ArticleCard {
                background-color: white;
                border: 1px solid #dfe6e9;
                border-radius: 8px;
                margin: 8px 5px;
                padding: 15px;
            }
            ArticleCard:hover {
                border: 1px solid #3498db;
                box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Верхняя строка: заголовок
        title = QLabel(self.article_data["title"])
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        title.setWordWrap(True)
        title.setMinimumHeight(30)
        layout.addWidget(title)

        # Вторая строка: мета-информация
        meta_container = QWidget()
        meta_container.setFixedHeight(98)
        meta_layout = QHBoxLayout(meta_container)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(8)

        # Источник
        source_label = QLabel(f"📰 {self.article_data['source']}")
        source_label.setStyleSheet("""
            color: #636e72;
            font-size: 9pt;
            padding: 5px 8px;
            background-color: #f8f9fa;
            border-radius: 5px;
        """)
        meta_layout.addWidget(source_label)

        # Дата
        date_label = QLabel(f"📅 {self.article_data['date']}")
        date_label.setStyleSheet("""
            color: #636e72;
            font-size: 9pt;
            padding: 5px 8px;
            background-color: #f8f9fa;
            border-radius: 5px;
        """)
        meta_layout.addWidget(date_label)

        meta_layout.addStretch()

        # Тема с индикатором уверенности и ПРОЦЕНТАМИ С ПОДПИСЬЮ
        confidence = self.article_data["confidence"]
        confidence_percent = int(confidence * 100)

        if confidence > 0.9:
            color = "#27ae60"
            confidence_text = f"{confidence_percent}%\n🎯 Высокая"
        elif confidence > 0.8:
            color = "#f39c12"
            confidence_text = f"{confidence_percent}%\n📊 Средняя"
        else:
            color = "#e74c3c"
            confidence_text = f"{confidence_percent}%\n⚠️ Низкая"

        # Создаем контейнер для темы и уверенности
        topic_container = QWidget()
        topic_container.setFixedWidth(140)
        topic_layout = QVBoxLayout(topic_container)
        topic_layout.setSpacing(3)
        topic_layout.setContentsMargins(0, 0, 0, 0)

        # Название темы (цветной прямоугольник)
        self.topic_label = QLabel(self.article_data["predicted_topic"])
        self.topic_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-weight: bold;
                font-size: 11pt;
                background-color: {color};
                padding: 8px 12px;
                border-radius: 8px;
                border: 2px solid {color}80;
                qproperty-alignment: AlignCenter;
            }}
        """)
        self.topic_label.setFixedHeight(34)
        self.topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Процент уверенности с подписью - БОЛЬШОЙ прямоугольник
        self.confidence_label = QLabel(confidence_text)
        self.confidence_label.setFixedHeight(60)
        self.confidence_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 13pt;
                font-weight: bold;
                padding: 6px 12px 8px 12px;
                background-color: {color}20;
                border-radius: 10px;
                border: 2px solid {color}50;
                qproperty-alignment: AlignCenter;
                line-height: 1.2;
            }}
        """)
        self.confidence_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        topic_layout.addWidget(self.topic_label)
        topic_layout.addWidget(self.confidence_label)

        meta_layout.addWidget(topic_container)

        layout.addWidget(meta_container)

        # Третья строка: контент
        content_preview = self.article_data["content"]
        if len(content_preview) > 140:
            content_preview = content_preview[:140] + "..."

        content = QLabel(content_preview)
        content.setWordWrap(True)
        content.setStyleSheet("""
            color: #555;
            font-size: 10pt;
            line-height: 1.4;
            margin: 5px 0;
            padding: 8px;
            background-color: #fdfdfd;
            border-radius: 6px;
            border-left: 3px solid #3498db;
        """)
        content.setFixedHeight(55)
        layout.addWidget(content)

        # Четвертая строка: панель коррекции
        correction_panel = QWidget()
        correction_panel.setFixedHeight(45)
        correction_layout = QHBoxLayout(correction_panel)
        correction_layout.setContentsMargins(0, 0, 0, 0)
        correction_layout.setSpacing(6)

        # Метка
        correction_label = QLabel("Исправить:")
        correction_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 10pt;")
        correction_label.setFixedWidth(70)
        correction_layout.addWidget(correction_label)

        # Комбобокс
        self.correction_combo = QComboBox()
        self.correction_combo.addItem("-- Выберите --")
        self.correction_combo.addItems(mock_data.available_topics)
        self.correction_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                font-size: 9pt;
                color: #2c3e50;
                min-height: 30px;
            }
            QComboBox:hover {
                border: 1px solid #3498db;
            }
        """)
        self.correction_combo.setFixedWidth(120)
        self.correction_combo.currentIndexChanged.connect(self.on_combo_changed)
        correction_layout.addWidget(self.correction_combo)

        # Кнопка
        self.correct_btn = QPushButton("✅ Применить")
        self.correct_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 7pt;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.correct_btn.setFixedWidth(90)
        self.correct_btn.setEnabled(False)
        self.correct_btn.clicked.connect(self.on_correct_click)
        correction_layout.addWidget(self.correct_btn)

        correction_layout.addStretch()
        layout.addWidget(correction_panel)

    def update_topic_display(self):
        """Обновляет отображение темы и confidence с подписью"""
        confidence = self.article_data["confidence"]
        confidence_percent = int(confidence * 100)
        topic = self.article_data["predicted_topic"]

        # Определяем цвет на основе confidence
        if self.is_corrected or confidence == 1.0:
            color = "#27ae60"
            confidence_text = "100%\n✅ Исправлено"
        elif confidence > 0.9:
            color = "#27ae60"
            confidence_text = f"{confidence_percent}%\n🎯 Высокая"
        elif confidence > 0.8:
            color = "#f39c12"
            confidence_text = f"{confidence_percent}%\n📊 Средняя"
        else:
            color = "#e74c3c"
            confidence_text = f"{confidence_percent}%\n⚠️ Низкая"

        # Обновляем тему
        self.topic_label.setText(topic)
        self.topic_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-weight: bold;
                font-size: 11pt;
                background-color: {color};
                padding: 8px 12px;
                border-radius: 8px;
                border: 2px solid {color}80;
                qproperty-alignment: AlignCenter;
            }}
        """)

        # Обновляем confidence с подписью
        self.confidence_label.setText(confidence_text)
        self.confidence_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 13pt;
                font-weight: bold;
                padding: 6px 12px 8px 12px;
                background-color: {color}20;
                border-radius: 10px;
                border: 2px solid {color}50;
                qproperty-alignment: AlignCenter;
                line-height: 1.2;
            }}
        """)

    def on_combo_changed(self, index):
        self.correct_btn.setEnabled(index > 0)

    def on_correct_click(self):
        if self.is_corrected:
            return

        selected_topic = self.correction_combo.currentText()
        if selected_topic and selected_topic != "-- Выберите --":
            # Сохраняем старые значения для анимации
            old_confidence = self.article_data["confidence"]
            old_percent = int(old_confidence * 100)
            old_color = self.get_confidence_color(old_confidence)

            # Корректируем статью в данных
            success = mock_data.correct_article_topic(
                self.article_data["id"],
                selected_topic
            )

            if success:
                self.is_corrected = True
                self.correct_btn.setText("✅ Исправлено")
                self.correct_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #27ae60;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 12px;
                        font-size: 9pt;
                        font-weight: bold;
                    }
                """)
                self.correct_btn.setEnabled(False)
                self.correction_combo.setEnabled(False)

                # Обновляем данные статьи
                self.article_data["predicted_topic"] = selected_topic
                self.article_data["confidence"] = 1.0
                self.article_data["true_topic"] = selected_topic

                # Обновляем отображение темы
                self.update_topic_display()

                # Анимация изменения процентов (от старого к 100%)
                self.animate_percentage_increase(old_percent, 100, old_color, "#27ae60")

                # Сигнализируем об исправлении
                self.article_corrected.emit(self.article_data["id"])

                print(f"📝 Коррекция сохранена: статья {self.article_data['id']} → {selected_topic}")

    def get_confidence_color(self, confidence):
        """Возвращает цвет по уровню уверенности"""
        if confidence > 0.9:
            return "#27ae60"
        elif confidence > 0.8:
            return "#f39c12"
        else:
            return "#e74c3c"

    def animate_percentage_increase(self, start_percent, end_percent,
                                    start_color, end_color):
        """Анимация плавного увеличения процентов"""
        # Цветовые переходы
        start_r = int(start_color[1:3], 16)
        start_g = int(start_color[3:5], 16)
        start_b = int(start_color[5:7], 16)

        end_r = int(end_color[1:3], 16)
        end_g = int(end_color[3:5], 16)
        end_b = int(end_color[5:7], 16)

        # Начальный текст
        current_percent = start_percent

        # Определяем текст для анимации
        if start_percent > 0.9:
            base_text = "🎯 Высокая"
        elif start_percent > 0.8:
            base_text = "📊 Средняя"
        else:
            base_text = "⚠️ Низкая"

        self.confidence_label.setText(f"{current_percent}%\n{base_text}")

        # Анимация
        step = 1
        delay = 20
        total_steps = end_percent - start_percent

        for i in range(total_steps + 1):
            current_percent = start_percent + i

            # Плавный переход цвета
            if i < total_steps:
                progress = i / total_steps
                current_r = int(start_r + (end_r - start_r) * progress)
                current_g = int(start_g + (end_g - start_g) * progress)
                current_b = int(start_b + (end_b - start_b) * progress)
                current_color = f"#{current_r:02x}{current_g:02x}{current_b:02x}"
            else:
                current_color = end_color

            # Запланировать обновление
            QTimer.singleShot(i * delay,
                              lambda p=current_percent, c=current_color, final=(i == total_steps):
                              self.update_animation_label(p, c, final))

        # Финальный вид
        QTimer.singleShot(total_steps * delay + 500,
                          lambda: self.update_topic_display())

    def update_animation_label(self, percent, color, is_final=False):
        """Обновляет текст и цвет метки процентов с подписью"""
        if percent < 100:
            # Во время анимации показываем "Исправление..."
            if percent > 95:
                text = f"{percent}%\n📈 Почти готово"
            else:
                text = f"{percent}%\n📈 Исправление..."
            font_size = "12pt"
            padding = "6px 12px 8px 12px"
            background_color = f"{color}20"
            border_color = f"{color}50"
        else:
            text = "100%\n✅ Исправлено"
            color = "#27ae60"
            font_size = "13pt"
            padding = "6px 12px 8px 12px"
            background_color = "#e8f6f3"
            border_color = "#27ae60"

        self.confidence_label.setText(text)
        self.confidence_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: {font_size};
                font-weight: bold;
                padding: {padding};
                background-color: {background_color};
                border-radius: 10px;
                border: 2px solid {border_color};
                qproperty-alignment: AlignCenter;
                line-height: 1.2;
            }}
        """)