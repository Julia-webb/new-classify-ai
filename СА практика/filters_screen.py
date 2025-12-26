from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QListWidget, QListWidgetItem, QMessageBox,
                             QRadioButton, QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt
from mock_data_news import mock_data


class FiltersScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_filters()
        print("✅ Экран фильтров загружен")

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title = QLabel("⚙️ Управление тематическими фильтрами")
        title.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Основной контейнер
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setSpacing(20)

        # ЛЕВАЯ КОЛОНКА: Создание фильтра
        left_panel = QGroupBox("➕ Создать новый фильтр")
        left_panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding-top: 15px;
                background-color: white;
                min-width: 300px;
            }
        """)

        left_layout = QVBoxLayout(left_panel)

        # 1. Название фильтра
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        name_label.setFixedWidth(80)
        self.filter_name = QLineEdit()
        self.filter_name.setPlaceholderText("Например: Инвестиции")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.filter_name)
        left_layout.addLayout(name_layout)

        # 2. Тема фильтра
        topic_layout = QHBoxLayout()
        topic_label = QLabel("Тема:")
        topic_label.setFixedWidth(80)
        self.topic_combo = QComboBox()
        self.topic_combo.addItem("Любая тема")
        self.topic_combo.addItems(["Политика", "Экономика", "Технологии", "Наука",
                                   "Медицина", "Спорт", "Культура", "Образование"])
        self.topic_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                font-size: 10pt;
                color: #2c3e50;
            }
        """)
        topic_layout.addWidget(topic_label)
        topic_layout.addWidget(self.topic_combo)
        left_layout.addLayout(topic_layout)

        # 3. Логика фильтра
        logic_layout = QHBoxLayout()
        logic_label = QLabel("Логика:")
        logic_label.setFixedWidth(80)

        self.radio_or = QRadioButton("ИЛИ (любое слово)")
        self.radio_and = QRadioButton("И (все слова)")
        self.radio_or.setChecked(True)

        logic_group = QButtonGroup()
        logic_group.addButton(self.radio_or)
        logic_group.addButton(self.radio_and)

        logic_layout.addWidget(logic_label)
        logic_layout.addWidget(self.radio_or)
        logic_layout.addWidget(self.radio_and)
        left_layout.addLayout(logic_layout)

        # 4. Ключевые слова
        keywords_layout = QHBoxLayout()
        keywords_label = QLabel("Ключевые слова:")
        keywords_label.setFixedWidth(80)

        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("через запятую: стартап,инвестиции,технологии")

        keywords_layout.addWidget(keywords_label)
        keywords_layout.addWidget(self.keywords_input)
        left_layout.addLayout(keywords_layout)

        # 5. Подсказка по ключевым словам
        keywords_hint = QLabel("💡 Введите слова через запятую. Они будут искаться в заголовке и тексте статей.")
        keywords_hint.setStyleSheet("color: #7f8c8d; font-size: 9pt; padding: 5px;")
        left_layout.addWidget(keywords_hint)

        # 6. Кнопка создания
        self.create_btn = QPushButton("💾 Создать фильтр")
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.create_btn.clicked.connect(self.create_filter)
        left_layout.addWidget(self.create_btn)

        left_layout.addStretch()
        main_layout.addWidget(left_panel)

        # ПРАВАЯ КОЛОНКА: Список фильтров
        right_panel = QGroupBox("📂 Мои фильтры")
        right_panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                padding-top: 15px;
                background-color: white;
                min-width: 300px;
            }
        """)

        right_layout = QVBoxLayout(right_panel)

        # Список фильтров
        self.filters_list = QListWidget()
        self.filters_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-size: 10pt;
                min-height: 200px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.filters_list.itemClicked.connect(self.on_filter_selected)
        right_layout.addWidget(self.filters_list)

        # Панель кнопок
        btn_panel = QWidget()
        btn_layout = QHBoxLayout(btn_panel)
        btn_layout.setContentsMargins(0, 10, 0, 0)

        self.toggle_btn = QPushButton("🔘 Вкл/Выкл")
        self.toggle_btn.setEnabled(False)
        self.toggle_btn.clicked.connect(self.toggle_filter)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)

        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_filter)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)

        btn_layout.addWidget(self.toggle_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        right_layout.addWidget(btn_panel)

        # Счетчик фильтров
        self.filter_counter = QLabel("Всего фильтров: 0")
        self.filter_counter.setStyleSheet("""
            color: #7f8c8d;
            font-style: italic;
            padding-top: 10px;
        """)
        right_layout.addWidget(self.filter_counter)

        right_layout.addStretch()
        main_layout.addWidget(right_panel)

        layout.addWidget(main_container)

        # Подсказка
        hint = QLabel("💡 Создавайте фильтры для персонализации ленты новостей. "
                      "Фильтры ищут ключевые слова в заголовке и тексте статей.")
        hint.setStyleSheet("""
            color: #7f8c8d;
            padding: 12px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #3498db;
            margin-top: 15px;
        """)
        layout.addWidget(hint)

    def create_filter(self):
        """Создает новый фильтр"""
        print("=" * 50)
        print("🔄 СОЗДАНИЕ НОВОГО ФИЛЬТРА")

        # 1. Получаем данные
        name = self.filter_name.text().strip()
        print(f"📝 Название: '{name}'")

        if not name:
            print("❌ ОШИБКА: Пустое название!")
            QMessageBox.warning(self, "Ошибка", "Введите название фильтра!")
            return

        topic = self.topic_combo.currentText()
        if topic == "Любая тема":
            topic = None
        print(f"🎯 Тема: {topic}")

        logic = "OR" if self.radio_or.isChecked() else "AND"
        print(f"🔧 Логика: {logic}")

        # Получаем ключевые слова
        keywords_text = self.keywords_input.text().strip()
        keywords = []
        if keywords_text:
            keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
        print(f"🔑 Ключевые слова: {keywords}")

        # 2. Создаем фильтр
        try:
            # Используем метод из mock_data
            new_filter = mock_data.create_filter(name, topic, keywords, logic)
            print(f"✅ Фильтр создан: {new_filter}")

            # 3. Обновляем интерфейс
            self.load_filters()
            self.filter_name.clear()
            self.keywords_input.clear()

            # 4. Показываем сообщение об успехе
            QMessageBox.information(self, "✅ Успех",
                                    f"Фильтр '{name}' успешно создан!\n\n"
                                    f"📌 Тема: {topic or 'Любая'}\n"
                                    f"🔧 Логика: {logic}\n"
                                    f"🔑 Ключевые слова: {', '.join(keywords) if keywords else 'Нет'}\n"
                                    f"📊 Всего фильтров: {len(mock_data.user_filters)}")

            # 5. Обновляем фильтры в ленте
            self.update_feed_filters()

        except Exception as e:
            print(f"❌ ОШИБКА при создании фильтра: {e}")
            QMessageBox.critical(self, "❌ Ошибка",
                                 f"Не удалось создать фильтр:\n{str(e)}")

    def load_filters(self):
        """Загружает список фильтров"""
        print(f"📂 Загружаю {len(mock_data.user_filters)} фильтров")

        self.filters_list.clear()

        if not mock_data.user_filters:
            print("📭 Список фильтров пуст")
            item = QListWidgetItem("😔 Фильтров пока нет")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.filters_list.addItem(item)
        else:
            for filter_data in mock_data.user_filters:
                # Формируем текст
                status = "✅" if filter_data.get("active", True) else "⭕"
                topic = filter_data.get("topic") or "Любая тема"
                logic = {"OR": "ИЛИ", "AND": "И"}.get(filter_data.get("logic", "OR"), "ИЛИ")
                name = filter_data.get("name", "Без имени")
                keywords = filter_data.get("keywords", [])

                item_text = f"{status} {name}\n"
                item_text += f"   📍 Тема: {topic}\n"
                item_text += f"   🎯 Логика: {logic}\n"

                if keywords:
                    keywords_preview = ', '.join(keywords[:3])
                    if len(keywords) > 3:
                        keywords_preview += f"... (+{len(keywords) - 3})"
                    item_text += f"   🔑 Ключевые слова: {keywords_preview}"
                else:
                    item_text += "   🔑 Ключевые слова: Нет"

                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, filter_data)
                self.filters_list.addItem(item)

                print(f"   📌 Добавлен: {name}")

        self.filter_counter.setText(f"Всего фильтров: {len(mock_data.user_filters)}")
        print(f"✅ Список фильтров обновлен")

    def on_filter_selected(self, item):
        """Обрабатывает выбор фильтра"""
        if item.flags() & Qt.ItemFlag.ItemIsSelectable:
            item_text_lines = item.text().split('\n')
            print(f"🎯 Выбран фильтр: {item_text_lines[0]}")
            self.toggle_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.toggle_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

    def toggle_filter(self):
        """Включает/выключает фильтр"""
        current = self.filters_list.currentItem()
        if not current:
            return

        filter_data = current.data(Qt.ItemDataRole.UserRole)
        if not filter_data:
            return

        old_status = filter_data.get("active", True)
        filter_data["active"] = not old_status
        new_status = filter_data["active"]

        print(f"🔄 Фильтр '{filter_data.get('name')}': {old_status} → {new_status}")

        self.load_filters()
        self.toggle_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        # Обновляем фильтры в ленте
        self.update_feed_filters()

        status_text = "активирован" if new_status else "деактивирован"
        QMessageBox.information(self, "✅ Статус", f"Фильтр {status_text}")

    def delete_filter(self):
        """Удаляет фильтр"""
        current = self.filters_list.currentItem()
        if not current:
            return

        filter_data = current.data(Qt.ItemDataRole.UserRole)
        if not filter_data:
            return

        filter_name = filter_data.get("name", "этот фильтр")

        reply = QMessageBox.question(
            self, "❓ Подтверждение",
            f"Удалить фильтр '{filter_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Сохраняем ID для удаления
            filter_id = filter_data.get("id")

            # Удаляем фильтр
            mock_data.user_filters = [
                f for f in mock_data.user_filters
                if f.get("id") != filter_id
            ]

            print(f"🗑️ Удален фильтр: {filter_name}")
            print(f"   Осталось: {len(mock_data.user_filters)} фильтров")

            self.load_filters()
            self.toggle_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

            # Обновляем фильтры в ленте
            self.update_feed_filters()

            QMessageBox.information(self, "✅ Успех", f"Фильтр удален")

    def update_feed_filters(self):
        """Обновляет фильтры в ленте новостей"""
        try:
            # Получаем главное окно
            main_window = self.window()

            if hasattr(main_window, 'update_feed_filters'):
                main_window.update_feed_filters()
                print("✅ Фильтры в ленте обновлены")
            else:
                print("⚠️ Главное окно не имеет метода update_feed_filters")

        except Exception as e:
            print(f"⚠️ Не удалось обновить фильтры в ленте: {e}")