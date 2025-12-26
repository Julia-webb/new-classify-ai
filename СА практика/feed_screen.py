from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox,
                             QScrollArea, QFrame, QSizePolicy,
                             QMessageBox, QDialog, QVBoxLayout as QVBoxLayout2,
                             QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from mock_data_news import mock_data
from article_card import ArticleCard
from export_data import DataExporter


class FeedScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.current_filter = "Все темы"
        self.init_ui()
        self.load_articles()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Заголовок
        title = QLabel("📰 Новостная лента")
        title.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)

        # Панель фильтрации
        filter_panel = QFrame()
        filter_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #dfe6e9;
            }
        """)

        filter_layout = QHBoxLayout(filter_panel)

        filter_label = QLabel("Фильтр по теме:")
        filter_label.setStyleSheet("font-weight: bold;")

        self.filter_combo = QComboBox()

        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                min-width: 200px;
                font-size: 10pt;
                color: #2c3e50;
            }
            QComboBox QAbstractItemView {
                color: #2c3e50;
            }
        """)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)

        # Кнопка обновления фильтров
        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Обновить список фильтров")
        refresh_btn.setFixedSize(35, 35)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5f8a;
            }
        """)
        refresh_btn.clicked.connect(self.update_filter_list)

        # Кнопка экспорта
        export_btn = QPushButton("💾")
        export_btn.setToolTip("Экспорт отфильтрованных статей")
        export_btn.setFixedSize(35, 35)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        export_btn.clicked.connect(self.export_filtered_articles)

        # Счетчик статей
        self.article_count = QLabel(f"Статей: {len(mock_data.articles)}")
        self.article_count.setStyleSheet("color: #7f8c8d; font-weight: bold;")

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(refresh_btn)
        filter_layout.addWidget(export_btn)
        filter_layout.addWidget(self.article_count)
        filter_layout.addStretch()

        layout.addWidget(filter_panel)

        # Область прокрутки для статей
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Контейнер для статей
        self.scroll_widget = QWidget()
        self.articles_layout = QVBoxLayout(self.scroll_widget)
        self.articles_layout.setSpacing(10)
        self.articles_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area, 1)

        # Инициализируем список фильтров
        self.update_filter_list()

    def update_filter_list(self):
        """Обновляет список фильтров в выпадающем меню"""
        print("🔄 Обновление списка фильтров в ленте...")

        # Сохраняем текущий выбор
        current_text = self.filter_combo.currentText()

        # Очищаем комбобокс
        self.filter_combo.clear()

        # Добавляем основные темы
        self.filter_combo.addItem("Все темы")
        self.filter_combo.addItems(mock_data.available_topics)

        # Проверяем наличие пользовательских фильтров
        user_filters = getattr(mock_data, 'user_filters', [])

        if user_filters:
            # Добавляем разделитель
            self.filter_combo.addItem("─" * 20)
            self.filter_combo.addItem("📂 Мои фильтры:")

            active_filters_added = False

            for user_filter in user_filters:
                # Проверяем активен ли фильтр
                if user_filter.get("active", True):
                    filter_name = user_filter.get("name", "Без имени")
                    filter_topic = user_filter.get("topic", "Любая тема")
                    keywords = user_filter.get("keywords", [])

                    # Формируем отображаемый текст
                    if filter_topic:
                        display_text = f"   ⚙️ {filter_name} ({filter_topic})"
                    else:
                        display_text = f"   ⚙️ {filter_name} (Все темы)"

                    # Добавляем информацию о ключевых словах
                    if keywords:
                        keywords_preview = ', '.join(keywords[:2])
                        if len(keywords) > 2:
                            keywords_preview += "..."
                        display_text += f" - [{keywords_preview}]"

                    self.filter_combo.addItem(display_text)
                    active_filters_added = True
                    print(f"   ✅ Добавлен фильтр: {filter_name}")

            if not active_filters_added:
                self.filter_combo.addItem("   😔 Нет активных фильтров")

        # Восстанавливаем выбор, если он еще существует
        for i in range(self.filter_combo.count()):
            if self.filter_combo.itemText(i) == current_text:
                self.filter_combo.setCurrentIndex(i)
                print(f"✅ Восстановлен выбор: {current_text}")
                break
        else:
            # Если предыдущий выбор не найден, выбираем "Все темы"
            self.filter_combo.setCurrentIndex(0)
            print("✅ Установлен выбор: Все темы")

        print(f"✅ Список фильтров обновлен. Всего элементов: {self.filter_combo.count()}")

        # Обновляем счетчик статей
        self.update_article_count()

    def on_filter_changed(self, selected_text):
        """Обрабатывает изменение фильтра"""
        print(f"🎯 Выбран фильтр: {selected_text}")

        # Проверяем, выбран ли пользовательский фильтр
        if selected_text.startswith("   ⚙️"):
            # Извлекаем информацию о фильтре
            filter_text = selected_text.replace("   ⚙️ ", "")

            if "(" in filter_text and ")" in filter_text:
                filter_name = filter_text.split(" (")[0]
                filter_topic = filter_text.split(" (")[1].split(")")[0]

                print(f"   Применяем пользовательский фильтр: {filter_name}")
                print(f"   Тема фильтра: {filter_topic}")

                # Находим фильтр в списке
                for user_filter in mock_data.user_filters:
                    if user_filter.get("name") == filter_name:
                        # Получаем ключевые слова и логику из фильтра
                        keywords = user_filter.get("keywords", [])
                        logic = user_filter.get("logic", "OR")

                        # Если тема "Любая тема", то topic = None
                        topic = None if filter_topic == "Любая тема" else filter_topic

                        # Применяем фильтрацию по ключевым словам
                        if keywords:
                            articles = mock_data.get_articles_by_keywords(
                                keywords=keywords,
                                logic=logic,
                                topic=topic
                            )
                            print(f"   Найдено {len(articles)} статей по ключевым словам: {keywords}")
                            print(f"   Логика фильтрации: {logic}")
                            self.load_filtered_articles(articles, filter_name)
                        else:
                            # Если нет ключевых слов, фильтруем просто по теме
                            self.load_articles(filter_topic if topic else None)
                        break
                else:
                    self.load_articles()
            else:
                self.load_articles()

        elif selected_text == "Все темы":
            print("   Применен фильтр: Все темы")
            self.load_articles()

        elif selected_text in mock_data.available_topics:
            print(f"   Применен фильтр по теме: {selected_text}")
            self.load_articles(selected_text)

        else:
            # Игнорируем разделители и заголовки
            if selected_text != "─" * 20 and selected_text != "📂 Мои фильтры:":
                print(f"   Неизвестный фильтр, загружаем все темы")
                self.load_articles()

        # Обновляем текущий фильтр
        self.current_filter = selected_text

    def load_articles(self, filter_topic=None):
        """Загружает статьи с учетом фильтра"""
        print(f"📰 Загрузка статей. Фильтр: {filter_topic or 'Все темы'}")

        # Очищаем старые статьи
        for i in reversed(range(self.articles_layout.count())):
            item = self.articles_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Получаем отфильтрованные статьи
        articles = mock_data.get_articles_by_filter(filter_topic)

        # Добавляем новые статьи
        if articles:
            for article in articles:
                card = ArticleCard(article)
                # Подключаем сигнал об исправлении
                card.article_corrected.connect(self.on_article_corrected)
                self.articles_layout.insertWidget(0, card)

            print(f"✅ Загружено {len(articles)} статей")
        else:
            # Сообщение, если статей нет
            no_articles = QLabel("😔 Статей по выбранному фильтру не найдено")
            no_articles.setStyleSheet("""
                font-size: 14pt;
                color: #95a5a6;
                padding: 50px;
                text-align: center;
            """)
            no_articles.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.articles_layout.addWidget(no_articles)
            print("❌ Статей не найдено")

        # Обновляем счетчик статей
        self.update_article_count(filter_topic)

    def load_filtered_articles(self, articles, filter_name=None):
        """Загружает предварительно отфильтрованные статьи"""
        filter_info = f"фильтром '{filter_name}'" if filter_name else "ключевыми словами"
        print(f"📰 Загрузка статей, отфильтрованных {filter_info}")

        # Очищаем старые статьи
        for i in reversed(range(self.articles_layout.count())):
            item = self.articles_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Добавляем новые статьи
        if articles:
            for article in articles:
                card = ArticleCard(article)
                card.article_corrected.connect(self.on_article_corrected)
                self.articles_layout.insertWidget(0, card)

            print(f"✅ Загружено {len(articles)} статей")
        else:
            # Сообщение, если статей нет
            if filter_name:
                message = f"😔 Статей по фильтру '{filter_name}' не найдено"
            else:
                message = "😔 Статей по выбранным ключевым словам не найдено"

            no_articles = QLabel(message)
            no_articles.setStyleSheet("""
                font-size: 14pt;
                color: #95a5a6;
                padding: 50px;
                text-align: center;
            """)
            no_articles.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.articles_layout.addWidget(no_articles)
            print("❌ Статей не найдено")

        # Обновляем счетчик статей
        self.update_article_count_special(len(articles), filter_name)

    def on_article_corrected(self, article_id):
        """Обрабатывает исправление статьи"""
        print(f"🔄 Статья {article_id} исправлена, обновляю интерфейс...")

        # Можно добавить дополнительные действия:
        # 1. Обновить статистику
        # 2. Обновить фильтры
        # 3. Показать уведомление

        # Просто выводим сообщение
        print(f"✅ Интерфейс обновлен для статьи {article_id}")

    def update_article_count(self, filter_topic=None):
        """Обновляет счетчик статей"""
        try:
            articles = mock_data.get_articles_by_filter(filter_topic)
            count = len(articles)

            # Формируем текст счетчика
            if filter_topic:
                count_text = f"Статей по теме '{filter_topic}': {count}"
            else:
                count_text = f"Всего статей: {count}"

            # Проверяем, что article_count существует
            if hasattr(self, 'article_count') and self.article_count:
                self.article_count.setText(count_text)
                print(f"📊 {count_text}")
            else:
                print(f"⚠️ article_count не доступен. Статей: {count}")

        except Exception as e:
            print(f"❌ Ошибка обновления счетчика статей: {e}")

    def update_article_count_special(self, count, filter_name=None):
        """Обновляет счетчик для фильтрованных статей"""
        if hasattr(self, 'article_count') and self.article_count:
            if filter_name:
                self.article_count.setText(f"Найдено статей по фильтру '{filter_name}': {count}")
                print(f"📊 Найдено статей по фильтру '{filter_name}': {count}")
            else:
                self.article_count.setText(f"Найдено статей: {count}")
                print(f"📊 Найдено статей: {count}")

    def export_filtered_articles(self):
        """Экспорт отфильтрованных статей"""
        try:
            # Получаем текущие статьи
            current_text = self.filter_combo.currentText()
            articles = []
            filter_name = None

            if current_text.startswith("   ⚙️"):
                # Для пользовательских фильтров
                filter_text = current_text.replace("   ⚙️ ", "")
                if "(" in filter_text and ")" in filter_text:
                    filter_name = filter_text.split(" (")[0]

                    for user_filter in mock_data.user_filters:
                        if user_filter.get("name") == filter_name:
                            keywords = user_filter.get("keywords", [])
                            logic = user_filter.get("logic", "OR")
                            topic = user_filter.get("topic")

                            articles = mock_data.get_articles_by_keywords(
                                keywords=keywords,
                                logic=logic,
                                topic=topic
                            )
                            break
            elif current_text == "Все темы":
                filter_name = "Все темы"
                articles = mock_data.articles
            elif current_text in mock_data.available_topics:
                filter_name = f"Тема: {current_text}"
                articles = mock_data.get_articles_by_filter(current_text)
            else:
                # Если это разделитель или заголовок
                return

            if not articles:
                QMessageBox.warning(self, "⚠️ Предупреждение",
                                    "Нет статей для экспорта")
                return

            # Простой диалог выбора формата
            formats = ["JSON (*.json)", "CSV (*.csv)", "Excel (*.xlsx)"]
            format_choice, ok = QInputDialog.getItem(
                self, "💾 Экспорт статей",
                f"Выберите формат для экспорта {len(articles)} статей:",
                formats, 0, False
            )

            if not ok:
                return

            # Экспорт
            exporter = DataExporter(self)
            success = False

            if "JSON" in format_choice:
                success = exporter.export_articles_json(articles)
            elif "CSV" in format_choice:
                success = exporter.export_articles_csv(articles)
            elif "Excel" in format_choice:
                success = exporter.export_articles_excel(articles)

            if success:
                QMessageBox.information(self, "✅ Успех",
                                        f"Экспортировано {len(articles)} статей")
            else:
                QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать статьи")

        except ImportError as e:
            print(f"❌ Ошибка импорта модуля: {e}")
            QMessageBox.warning(self, "⚠️ Предупреждение",
                                "Модуль экспорта не найден. Установите pandas и openpyxl.")
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")
            QMessageBox.critical(self, "❌ Ошибка",
                                 f"Не удалось экспортировать статьи:\n{str(e)}")