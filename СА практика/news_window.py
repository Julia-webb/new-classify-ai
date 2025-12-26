import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QStackedWidget, QLabel, QMenuBar, QStatusBar,
                             QMessageBox, QDialog, QTextEdit, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont, QIcon, QTextCursor

from mock_data_news import mock_data
from feed_screen import FeedScreen
from filters_screen import FiltersScreen
from stats_screen import StatsScreen


class DocumentationDialog(QDialog):
    """Диалог с полной документацией"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📖 Руководство пользователя")
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("📖 Полное руководство пользователя")
        title.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)

        # Область прокрутки с текстом
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #dfe6e9;
                border-radius: 8px;
                background-color: white;
            }
        """)

        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)

        doc_text = QTextEdit()
        doc_text.setReadOnly(True)
        doc_text.setStyleSheet("""
            QTextEdit {
                border: none;
                font-size: 11pt;
                line-height: 1.5;
                padding: 15px;
            }
        """)

        # Полная документация в HTML
        documentation = """
        <html>
        <head>
        <style>
            body { font-family: Arial, sans-serif; color: #2c3e50; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #2980b9; margin-top: 25px; }
            h3 { color: #34495e; margin-top: 20px; }
            p { margin: 10px 0; line-height: 1.6; }
            ul { margin: 10px 0; padding-left: 20px; }
            li { margin: 8px 0; }
            .tip { background-color: #e8f4fc; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; margin: 15px 0; }
            .warning { background-color: #fde8e8; padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c; margin: 15px 0; }
            .success { background-color: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60; margin: 15px 0; }
            code { background-color: #f1f3f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
        </style>
        </head>
        <body>

        <h1>📚 NewsClassify AI - Руководство пользователя</h1>

        <div class="tip">
        <b>💡 Внимание!</b> Это прототип интеллектуальной системы классификации новостей. 
        Все данные хранятся локально, система обучается на ваших коррекциях.
        </div>

        <h2>🎯 Назначение системы</h2>
        <p><b>NewsClassify AI</b> - это интеллектуальная система для автоматической классификации новостных статей 
        с возможностью тонкой настройки тематических фильтров и активного обучения.</p>

        <h2>📱 Основные модули</h2>

        <h3>1. 📰 Лента новостей</h3>
        <p><b>Назначение:</b> Просмотр и классификация новостных статей.</p>
        <p><b>Как использовать:</b></p>
        <ul>
            <li><b>Фильтрация:</b> Используйте выпадающий список вверху для фильтрации по темам</li>
            <li><b>Просмотр:</b> Листайте ленту для просмотра всех статей</li>
            <li><b>Коррекция:</b> Если система ошиблась:
                <ul>
                    <li>Выберите правильную тему из выпадающего списка под статьей</li>
                    <li>Нажмите кнопку <code>✅ Применить</code></li>
                    <li>Система запомнит вашу коррекцию и будет учиться</li>
                </ul>
            </li>
            <li><b>Индикаторы:</b>
                <ul>
                    <li>🎯 Зеленый - высокая уверенность (>90%)</li>
                    <li>📊 Оранжевый - средняя уверенность (80-90%)</li>
                    <li>⚠️ Красный - низкая уверенность (<80%)</li>
                </ul>
            </li>
        </ul>

        <h3>2. ⚙️ Управление фильтрами</h3>
        <p><b>Назначение:</b> Создание и управление тематическими фильтрами.</p>
        <p><b>Как использовать:</b></p>
        <ul>
            <li><b>Создание фильтра:</b>
                <ol>
                    <li>Введите название фильтра</li>
                    <li>Выберите тему (или оставьте "Любая тема")</li>
                    <li>Выберите логику фильтрации:
                        <ul>
                            <li><code>ИЛИ</code> - статьи, содержащие ЛЮБОЕ из ключевых слов</li>
                            <li><code>И</code> - статьи, содержащие ВСЕ ключевые слова</li>
                        </ul>
                    </li>
                    <li>Введите ключевые слова через запятую</li>
                    <li>Нажмите <code>💾 Создать фильтр</code></li>
                </ol>
            </li>
            <li><b>Управление фильтрами:</b>
                <ul>
                    <li>Выберите фильтр в списке справа</li>
                    <li>Используйте кнопки для включения/выключения или удаления</li>
                </ul>
            </li>
        </ul>

        <div class="success">
        <b>🎯 Профессиональный совет:</b> Создавайте специализированные фильтры для точного поиска. 
        Например: "Технологические стартапы" = тема "Технологии" + ключевые слова ["стартап", "инвестиции", "инновации"]
        </div>

        <h3>3. 📊 Аналитика системы</h3>
        <p><b>Назначение:</b> Мониторинг работы системы классификации.</p>
        <p><b>Как использовать:</b></p>
        <ul>
            <li><b>Общая статистика:</b> Просматривайте ключевые метрики в карточках</li>
            <li><b>Точность по темам:</b> Анализируйте, по каким темам система работает лучше/хуже</li>
            <li><b>История коррекций:</b> Смотрите, какие исправления вы внесли</li>
            <li><b>Обновление:</b> Нажмите <code>🔄 Обновить статистику</code> для актуальных данных</li>
        </ul>

        <h2>⌨️ Горячие клавиши</h2>
        <ul>
            <li><code>Ctrl+1</code> - Перейти в Ленту новостей</li>
            <li><code>Ctrl+2</code> - Перейти в Управление фильтрами</li>
            <li><code>Ctrl+3</code> - Перейти в Аналитику системы</li>
            <li><code>F1</code> - Открыть документация</li>
            <li><code>F5</code> - Обновить текущий экран</li>
            <li><code>F11</code> - Полноэкранный режим</li>
            <li><code>Ctrl+Q</code> - Выход из программы</li>
        </ul>

        <h2>🎓 Активное обучение системы</h2>
        <p>Система использует активное обучение для улучшения точности классификации:</p>
        <ol>
            <li>Когда вы корректируете тему статьи, система запоминает это</li>
            <li>Накопленные коррекции используются для дообучения модели</li>
            <li>Чем больше вы корректируете, тем точнее становится система</li>
            <li>Статистика обучения отображается в разделе Аналитика</li>
        </ol>

        <div class="warning">
        <b>⚠️ Важно!</b> Все данные хранятся локально на вашем компьютере. 
        Для экспорта данных используйте меню <b>Файл → Экспорт данных</b>.
        </div>

        <h2>🔧 Системные требования</h2>
        <ul>
            <li>Операционная система: Windows 10/11, macOS 10.15+, Linux</li>
            <li>Память: не менее 512 МБ оперативной памяти</li>
            <li>Хранилище: около 50 МБ свободного места</li>
            <li>Python 3.8+ (для запуска исходного кода)</li>
        </ul>

        <h2>💾 Экспорт и импорт данных</h2>
        <p>Система поддерживает экспорт данных в различных форматах:</p>
        <ul>
            <li><b>JSON</b> - структурированный формат для программистов</li>
            <li><b>CSV</b> - табличный формат для Excel/Google Sheets</li>
            <li><b>Excel</b> - готовые таблицы с форматированием</li>
            <li><b>Полный экспорт</b> - все данные в одной папке</li>
        </ul>
        <p>Для экспорта используйте меню <b>Файл → Экспорт данных</b> или кнопку 💾 в ленте новостей.</p>

        <h2>📞 Поддержка</h2>
        <p>Если у вас возникли вопросы или проблемы:</p>
        <ul>
            <li>Обратитесь к разделу "О программе"</li>
            <li>Проверьте, все ли шаги из руководства выполнены</li>
            <li>Убедитесь, что система соответствует требованиям</li>
        </ul>

        <div class="tip">
        <b>💎 Итог:</b> NewsClassify AI - мощный инструмент для управления новостным потоком. 
        Регулярно корректируйте классификацию, создавайте точные фильтры и следите за статистикой 
        для получения максимальной пользы от системы.
        </div>

        <hr style="margin: 30px 0; border: 1px solid #ecf0f1;">

        <p style="text-align: center; color: #7f8c8d; font-style: italic;">
        Руководство пользователя • NewsClassify AI v1.0.0 • © 2024
        </p>

        </body>
        </html>
        """

        doc_text.setHtml(documentation)
        doc_text.moveCursor(QTextCursor.MoveOperation.Start)
        text_layout.addWidget(doc_text)

        scroll_area.setWidget(text_widget)
        layout.addWidget(scroll_area, 1)

        # Кнопка закрытия
        close_btn = QPushButton("✕ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-size: 12pt;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignCenter)


class AboutDialog(QDialog):
    """Диалог с информацией о программе"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ℹ️ О программе")
        self.setGeometry(300, 300, 600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Заголовок с иконкой
        header = QHBoxLayout()

        icon_label = QLabel("📰")
        icon_label.setStyleSheet("font-size: 32pt;")
        header.addWidget(icon_label)

        title_layout = QVBoxLayout()

        app_name = QLabel("NewsClassify AI")
        app_name.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
        """)

        version = QLabel("Версия 1.0.0 (Прототип)")
        version.setStyleSheet("""
            color: #7f8c8d;
            font-size: 11pt;
        """)

        title_layout.addWidget(app_name)
        title_layout.addWidget(version)
        header.addLayout(title_layout)

        header.addStretch()
        layout.addLayout(header)

        # Разделитель
        separator = QLabel("─" * 50)
        separator.setStyleSheet("color: #bdc3c7; margin: 10px 0;")
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)

        # Информация о системе
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                font-size: 11pt;
                line-height: 1.5;
            }
        """)

        info = f"""
        <html>
        <body style="color: #2c3e50;">

        <h3 style="color: #2980b9;">🎯 Назначение системы</h3>
        <p><b>NewsClassify AI</b> - интеллектуальная система для автоматической классификации 
        новостных статей с тематическими фильтрами и активным обучением.</p>

        <h3 style="color: #2980b9;">🔧 Технологии</h3>
        <ul>
            <li><b>Интерфейс:</b> PyQt6 (Python GUI Framework)</li>
            <li><b>Классификация:</b> Имитация BERT-модели</li>
            <li><b>Хранение данных:</b> Локальное (in-memory)</li>
            <li><b>Архитектура:</b> MVC (Model-View-Controller)</li>
            <li><b>Экспорт данных:</b> JSON, CSV, Excel (pandas)</li>
        </ul>

        <h3 style="color: #2980b9;">📊 Ключевые возможности</h3>
        <ul>
            <li>Автоматическая классификация новостей по 8 темам</li>
            <li>Создание сложных тематических фильтров (И/ИЛИ)</li>
            <li>Коррекция классификации с активным обучением</li>
            <li>Детальная аналитика работы системы</li>
            <li>Локальное хранение всех данных</li>
            <li>Экспорт данных в JSON, CSV, Excel форматах</li>
        </ul>

        <h3 style="color: #2980b9;">📈 Системные показатели</h3>
        <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1;">Точность классификации</td>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1; text-align: right; color: #27ae60; font-weight: bold;">87.3%</td>
        </tr>
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1;">Обработано статей</td>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1; text-align: right;">{len(mock_data.articles)}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1;">Коррекций пользователя</td>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1; text-align: right;">{mock_data.classification_stats['corrected_count']}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1;">Создано фильтров</td>
            <td style="padding: 8px; border-bottom: 1px solid #ecf0f1; text-align: right;">{len(mock_data.user_filters)}</td>
        </tr>
        <tr>
            <td style="padding: 8px;">Версия прототипа</td>
            <td style="padding: 8px; text-align: right;">1.0.0</td>
        </tr>
        </table>

        <h3 style="color: #2980b9;">💾 Экспорт данных</h3>
        <p>Система поддерживает экспорт в нескольких форматах:</p>
        <ul>
            <li><b>JSON</b> - для разработчиков и анализа</li>
            <li><b>CSV</b> - для табличных редакторов</li>
            <li><b>Excel</b> - готовые отчеты с форматированием</li>
            <li><b>Полный экспорт</b> - все данные системы</li>
        </ul>

        <div style="background-color: #e8f4fc; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db;">
        <b>💡 Прототип для демонстрации:</b><br>
        Это учебный прототип, демонстрирующий принципы работы интеллектуальной системы классификации. 
        Все данные генерируются автоматически.
        </div>

        <h3 style="color: #2980b9;">👥 Разработка</h3>
        <p>Разработано в рамках учебного проекта по курсу <b>"Системный анализ"</b>.</p>

        <h3 style="color: #2980b9;">📞 Контактная информация</h3>
        <p>Для обратной связи и вопросов:</p>
        <ul>
            <li><b>Поддержка:</b> support@newsclassify.ai</li>
            <li><b>Документация:</b> F1 или меню Помощь → Документация</li>
            <li><b>Исходный код:</b> Доступен для учебных целей</li>
        </ul>

        </body>
        </html>
        """

        info_text.setHtml(info)
        layout.addWidget(info_text, 1)

        # Кнопка закрытия
        close_btn = QPushButton("✕ Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignCenter)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NewsClassify AI - Прототип")
        self.setGeometry(100, 100, 1400, 800)

        # Стиль приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
        """)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Левая панель навигации
        self.nav_widget = self.create_navigation_panel()
        main_layout.addWidget(self.nav_widget)

        # Правая область
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)

        # Создаем экраны
        self.create_screens()

        # Создаем меню
        self.create_menu_bar()

        # Создаем статусбар
        self.create_status_bar()

        # Таймер для живой статистики
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_live_stats)
        self.stats_timer.start(5000)  # Обновление каждые 5 секунд

        # Показываем стартовый экран
        self.show_screen(0)

        # Устанавливаем горячую клавишу F1 для документации
        self.shortcut_doc = QAction(self)
        self.shortcut_doc.setShortcut("F1")
        self.shortcut_doc.triggered.connect(self.show_documentation)
        self.addAction(self.shortcut_doc)

        # Горячая клавиша F5 для обновления
        self.shortcut_refresh = QAction(self)
        self.shortcut_refresh.setShortcut("F5")
        self.shortcut_refresh.triggered.connect(self.refresh_current_screen)
        self.addAction(self.shortcut_refresh)

        # Первоначальное обновление статистики
        self.update_live_stats()

    def create_navigation_panel(self):
        nav_widget = QWidget()
        nav_widget.setFixedWidth(220)
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
        """)

        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setSpacing(0)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: #1a252f;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)

        app_name = QLabel("NewsClassify AI")
        app_name.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16pt;
                font-weight: bold;
            }
        """)

        app_subtitle = QLabel("v1.0.0 Prototype")
        app_subtitle.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 9pt;
            }
        """)

        header_layout.addWidget(app_name)
        header_layout.addWidget(app_subtitle)
        nav_layout.addWidget(header)

        # Кнопки навигации
        self.nav_buttons = []

        self.btn_feed = self.create_nav_button("📰", "Лента новостей", True)
        self.btn_filters = self.create_nav_button("⚙️", "Фильтры", False)
        self.btn_stats = self.create_nav_button("📊", "Аналитика", False)

        for btn in [self.btn_feed, self.btn_filters, self.btn_stats]:
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        nav_layout.addStretch()

        # Подсказка в навигации
        hint_card = QWidget()
        hint_card.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 10px;
                padding: 10px;
            }
        """)

        hint_layout = QVBoxLayout(hint_card)

        hint_title = QLabel("📊 Живая статистика")
        hint_title.setStyleSheet("color: #ecf0f1; font-size: 10pt; font-weight: bold;")
        hint_layout.addWidget(hint_title)

        # Создаем live_stats
        self.live_stats = QLabel("Статей: 0\nФильтров: 0")
        self.live_stats.setStyleSheet("""
            color: #bdc3c7;
            font-size: 9pt;
            line-height: 1.5;
        """)
        hint_layout.addWidget(self.live_stats)

        # Добавляем еще одну подсказку
        help_hint = QLabel("💡 F1 - Документация")
        help_hint.setStyleSheet("color: #95a5a6; font-size: 8pt; margin-top: 10px;")
        hint_layout.addWidget(help_hint)

        nav_layout.addWidget(hint_card)

        return nav_widget

    def create_nav_button(self, icon, text, active=False):
        btn = QPushButton(f"{icon}  {text}")
        btn.setFixedHeight(50)
        if active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 11pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ecf0f1;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #34495e;
                    color: white;
                }
            """)

        # Подключаем обработчик
        if text == "Лента новостей":
            btn.clicked.connect(lambda: self.show_screen(0))
        elif text == "Фильтры":
            btn.clicked.connect(lambda: self.show_screen(1))
        elif text == "Аналитика":
            btn.clicked.connect(lambda: self.show_screen(2))

        return btn

    def show_screen(self, index):
        """Показывает выбранный экран"""
        # Обновляем кнопки
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 11pt;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #ecf0f1;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        background-color: #34495e;
                        color: white;
                    }
                """)

        # Если показываем ленту новостей - обновляем фильтры
        if index == 0 and hasattr(self, 'feed_screen'):
            self.feed_screen.update_filter_list()

        self.content_stack.setCurrentIndex(index)

        # Обновляем заголовок окна
        if index == 0:
            self.setWindowTitle("NewsClassify AI - Лента новостей")
        elif index == 1:
            self.setWindowTitle("NewsClassify AI - Управление фильтрами")
        elif index == 2:
            self.setWindowTitle("NewsClassify AI - Аналитика системы")

    def create_screens(self):
        """Создает экраны приложения"""
        self.feed_screen = FeedScreen()
        self.filters_screen = FiltersScreen()
        self.stats_screen = StatsScreen()

        self.content_stack.addWidget(self.feed_screen)
        self.content_stack.addWidget(self.filters_screen)
        self.content_stack.addWidget(self.stats_screen)

    def create_menu_bar(self):
        """Создает меню приложения"""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        # Подменю Экспорт
        export_menu = file_menu.addMenu("📤 Экспорт данных")

        # Экспорт статей
        export_articles_menu = export_menu.addMenu("📰 Статьи")

        export_json_action = QAction("📄 Экспорт в JSON", self)
        export_json_action.triggered.connect(lambda: self.export_data('articles_json'))
        export_articles_menu.addAction(export_json_action)

        export_csv_action = QAction("📊 Экспорт в CSV", self)
        export_csv_action.triggered.connect(lambda: self.export_data('articles_csv'))
        export_articles_menu.addAction(export_csv_action)

        export_excel_action = QAction("📈 Экспорт в Excel", self)
        export_excel_action.triggered.connect(lambda: self.export_data('articles_excel'))
        export_articles_menu.addAction(export_excel_action)

        # Экспорт фильтров
        export_filters_action = QAction("⚙️ Фильтры (JSON)", self)
        export_filters_action.triggered.connect(lambda: self.export_data('filters_json'))
        export_menu.addAction(export_filters_action)

        # Экспорт статистики
        export_stats_action = QAction("📊 Статистика (JSON)", self)
        export_stats_action.triggered.connect(lambda: self.export_data('stats_json'))
        export_menu.addAction(export_stats_action)

        # Экспорт всех данных
        export_all_action = QAction("💾 Все данные", self)
        export_all_action.triggered.connect(lambda: self.export_data('all_data'))
        export_menu.addAction(export_all_action)

        file_menu.addSeparator()

        # Импорт данных
        import_action = QAction("📥 Импорт данных", self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction("🚪 Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Помощь
        help_menu = menubar.addMenu("Помощь")

        docs_action = QAction("📖 Документация", self)
        docs_action.setShortcut("F1")
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)

        about_action = QAction("ℹ️ О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """Создает статусбар"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Система загружена и готова к работе")

    def show_documentation(self):
        """Показывает документацию"""
        dialog = DocumentationDialog(self)
        dialog.exec()

    def show_about(self):
        """Показывает информацию о программе"""
        dialog = AboutDialog(self)
        dialog.exec()

    def export_data(self, export_type):
        """Экспорт данных системы"""
        try:
            from export_data import DataExporter
            from mock_data_news import mock_data

            exporter = DataExporter(self)

            if export_type == 'articles_json':
                success = exporter.export_articles_json(mock_data.articles)
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            f"Экспортировано {len(mock_data.articles)} статей в JSON")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать статьи")

            elif export_type == 'articles_csv':
                success = exporter.export_articles_csv(mock_data.articles)
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            f"Экспортировано {len(mock_data.articles)} статей в CSV")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать статьи")

            elif export_type == 'articles_excel':
                success = exporter.export_articles_excel(mock_data.articles)
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            f"Экспортировано {len(mock_data.articles)} статей в Excel")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать статьи")

            elif export_type == 'filters_json':
                success = exporter.export_filters_json(mock_data.user_filters)
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            f"Экспортировано {len(mock_data.user_filters)} фильтров")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать фильтры")

            elif export_type == 'stats_json':
                success = exporter.export_stats_json(
                    mock_data.classification_stats,
                    mock_data.correction_history
                )
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            "Статистика успешно экспортирована")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать статистику")

            elif export_type == 'all_data':
                success, folder = exporter.export_all_data(
                    mock_data.articles,
                    mock_data.user_filters,
                    mock_data.classification_stats,
                    mock_data.correction_history
                )
                if success:
                    QMessageBox.information(self, "✅ Успех",
                                            f"Все данные экспортированы в папку:\n{folder}")
                else:
                    QMessageBox.warning(self, "❌ Ошибка", "Не удалось экспортировать все данные")

        except ImportError as e:
            print(f"❌ Ошибка импорта модуля: {e}")
            QMessageBox.warning(self, "⚠️ Предупреждение",
                                "Модуль экспорта не найден. Установите pandas и openpyxl:\npip install pandas openpyxl")
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")
            QMessageBox.critical(self, "❌ Критическая ошибка",
                                 f"Ошибка при экспорте данных:\n{str(e)}")

    def import_data(self):
        """Импорт данных в систему"""
        try:
            from import_data import DataImporter
            importer = DataImporter(self)
            importer.show_import_dialog()
        except ImportError:
            QMessageBox.information(self, "📝 Импорт данных",
                                    "Функция импорта данных будет реализована в следующей версии.")
        except Exception as e:
            QMessageBox.critical(self, "❌ Ошибка",
                                 f"Ошибка при импорте данных:\n{str(e)}")

    def refresh_current_screen(self):
        """Обновляет текущий экран"""
        current_index = self.content_stack.currentIndex()

        if current_index == 0:  # Лента новостей
            if hasattr(self, 'feed_screen'):
                self.feed_screen.load_articles()
        elif current_index == 1:  # Фильтры
            if hasattr(self, 'filters_screen'):
                self.filters_screen.load_filters()
        elif current_index == 2:  # Аналитика
            if hasattr(self, 'stats_screen'):
                self.stats_screen.update_stats()

        # Обновляем живую статистику
        self.update_live_stats()

        print(f"🔄 Экран {current_index} обновлен")

    def update_live_stats(self):
        """Обновляет живую статистику в навигационной панели"""
        try:
            from mock_data_news import mock_data

            # Получаем актуальные данные
            articles_count = len(mock_data.articles)
            active_filters = len([f for f in mock_data.user_filters if f.get("active", True)])
            corrections_count = mock_data.classification_stats.get('corrected_count', 0)

            # Форматируем текст
            stats_text = f"""📰 Статей: {articles_count}
⚙️ Фильтров: {active_filters}
✏️ Исправлений: {corrections_count}"""

            # Обновляем виджет, если он существует
            if hasattr(self, 'live_stats') and self.live_stats:
                self.live_stats.setText(stats_text)

            # Также обновляем статусбар
            if hasattr(self, 'status_bar') and self.status_bar:
                self.status_bar.showMessage(
                    f"📊 Система активна | Статей: {articles_count} | Коррекций: {corrections_count}")

        except Exception as e:
            print(f"📊 Ошибка обновления статистики: {e}")

    def update_feed_filters(self):
        """Обновляет список фильтров в ленте новостей"""
        try:
            if hasattr(self, 'feed_screen'):
                self.feed_screen.update_filter_list()
                print("🔄 Список фильтров в ленте обновлен")
        except Exception as e:
            print(f"⚠️ Не удалось обновить фильтры в ленте: {e}")


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())