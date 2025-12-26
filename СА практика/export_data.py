"""
Модуль для экспорта данных из системы
"""

import json
import csv
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import os


class DataExporter:
    """Класс для экспорта данных системы"""

    def __init__(self, parent_window=None):
        self.parent = parent_window

    def export_articles_json(self, articles):
        """Экспорт статей в JSON"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Экспорт статей в JSON",
                f"news_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json)"
            )

            if not filename:
                return False

            # Подготовка данных
            export_data = {
                "export_date": datetime.now().isoformat(),
                "total_articles": len(articles),
                "articles": []
            }

            for article in articles:
                article_data = {
                    "id": article["id"],
                    "title": article["title"],
                    "content": article["content"],
                    "source": article["source"],
                    "date": article["date"],
                    "predicted_topic": article["predicted_topic"],
                    "confidence": article["confidence"],
                    "true_topic": article.get("true_topic", ""),
                    "is_corrected": article.get("true_topic") is not None
                }
                export_data["articles"].append(article_data)

            # Сохранение в файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"❌ Ошибка экспорта JSON: {e}")
            return False

    def export_articles_csv(self, articles):
        """Экспорт статей в CSV"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Экспорт статей в CSV",
                f"news_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv)"
            )

            if not filename:
                return False

            # Определяем поля
            fields = ['id', 'title', 'content', 'source', 'date',
                      'predicted_topic', 'confidence', 'true_topic', 'is_corrected']

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()

                for article in articles:
                    row = {
                        'id': article["id"],
                        'title': article["title"],
                        'content': article["content"],
                        'source': article["source"],
                        'date': article["date"],
                        'predicted_topic': article["predicted_topic"],
                        'confidence': article["confidence"],
                        'true_topic': article.get("true_topic", ""),
                        'is_corrected': "Да" if article.get("true_topic") else "Нет"
                    }
                    writer.writerow(row)

            return True

        except Exception as e:
            print(f"❌ Ошибка экспорта CSV: {e}")
            return False

    def export_articles_excel(self, articles):
        """Экспорт статей в Excel"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Экспорт статей в Excel",
                f"news_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )

            if not filename:
                return False

            # Подготовка данных
            data = []
            for article in articles:
                data.append({
                    'ID': article["id"],
                    'Заголовок': article["title"],
                    'Содержание': article["content"],
                    'Источник': article["source"],
                    'Дата': article["date"],
                    'Предсказанная тема': article["predicted_topic"],
                    'Уверенность (%)': article["confidence"] * 100,
                    'Исправленная тема': article.get("true_topic", ""),
                    'Исправлена': "Да" if article.get("true_topic") else "Нет"
                })

            # Создание DataFrame и сохранение
            df = pd.DataFrame(data)
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Статьи', index=False)

                # Автоматическая ширина столбцов
                worksheet = writer.sheets['Статьи']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

            return True

        except Exception as e:
            print(f"❌ Ошибка экспорта Excel: {e}")
            return False

    def export_filters_json(self, filters):
        """Экспорт фильтров в JSON"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Экспорт фильтров в JSON",
                f"news_filters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json)"
            )

            if not filename:
                return False

            export_data = {
                "export_date": datetime.now().isoformat(),
                "total_filters": len(filters),
                "filters": filters
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"❌ Ошибка экспорта фильтров JSON: {e}")
            return False

    def export_stats_json(self, stats, correction_history):
        """Экспорт статистики в JSON"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.parent, "Экспорт статистики в JSON",
                f"news_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json)"
            )

            if not filename:
                return False

            export_data = {
                "export_date": datetime.now().isoformat(),
                "statistics": stats,
                "correction_history": correction_history,
                "summary": {
                    "total_corrections": len(correction_history),
                    "avg_confidence": stats.get("avg_confidence", 0),
                    "precision": stats.get("precision", 0)
                }
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"❌ Ошибка экспорта статистики JSON: {e}")
            return False

    def export_all_data(self, articles, filters, stats, correction_history):
        """Экспорт всех данных в один архив (папку с файлами)"""
        try:
            # Запрашиваем папку для сохранения
            folder = QFileDialog.getExistingDirectory(
                self.parent, "Выберите папку для экспорта всех данных"
            )

            if not folder:
                return False

            # Создаем подпапку с временной меткой
            export_folder = os.path.join(folder, f"NewsClassify_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            os.makedirs(export_folder, exist_ok=True)

            # Экспорт статей
            articles_filename = os.path.join(export_folder, "articles.json")
            articles_data = {
                "export_date": datetime.now().isoformat(),
                "total_articles": len(articles),
                "articles": articles
            }
            with open(articles_filename, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, ensure_ascii=False, indent=2)

            # Экспорт фильтров
            filters_filename = os.path.join(export_folder, "filters.json")
            filters_data = {
                "export_date": datetime.now().isoformat(),
                "total_filters": len(filters),
                "filters": filters
            }
            with open(filters_filename, 'w', encoding='utf-8') as f:
                json.dump(filters_data, f, ensure_ascii=False, indent=2)

            # Экспорт статистики
            stats_filename = os.path.join(export_folder, "statistics.json")
            stats_data = {
                "export_date": datetime.now().isoformat(),
                "statistics": stats,
                "correction_history": correction_history
            }
            with open(stats_filename, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)

            # Создание README файла
            readme_filename = os.path.join(export_folder, "README.txt")
            readme_content = f"""
NewsClassify AI - Экспорт данных
================================

Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Содержимое папки:
1. articles.json    - Все новостные статьи
2. filters.json     - Пользовательские фильтры
3. statistics.json  - Статистика системы и история коррекций

Описание файлов:
----------------
1. articles.json:
   - articles: Массив статей
     - id: Уникальный идентификатор
     - title: Заголовок статьи
     - content: Текст статьи
     - source: Источник
     - date: Дата публикации
     - predicted_topic: Предсказанная тема
     - confidence: Уверенность классификации (0-1)
     - true_topic: Исправленная тема (если есть)

2. filters.json:
   - filters: Массив фильтров
     - name: Название фильтра
     - topic: Тема фильтра
     - keywords: Ключевые слова
     - logic: Логика (OR/AND)
     - active: Активен ли фильтр

3. statistics.json:
   - statistics: Основная статистика
     - precision: Точность классификации
     - corrected_count: Количество коррекций
     - avg_confidence: Средняя уверенность
   - correction_history: История исправлений

Для импорта данных обратно в систему используйте меню "Файл → Импорт данных".

© NewsClassify AI v1.0.0
"""

            with open(readme_filename, 'w', encoding='utf-8') as f:
                f.write(readme_content)

            return True, export_folder

        except Exception as e:
            print(f"❌ Ошибка полного экспорта: {e}")
            return False, ""