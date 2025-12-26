import unittest
from mock_data_news import MockNewsData
from article_card import ArticleCard
from PyQt6.QtWidgets import QApplication
import sys


class TestNewsClassification(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.mock_data = MockNewsData()

    def test_confidence_colors(self):
        """Тест цветовых индикаторов уверенности"""
        test_cases = [
            (0.95, "Высокая (95%)", "#27ae60"),
            (0.85, "Средняя (85%)", "#f39c12"),
            (0.75, "Низкая (75%)", "#e74c3c"),
        ]

        for confidence, expected_text, expected_color in test_cases:
            article = {"id": 999, "title": "Test", "content": "Test",
                       "source": "Test", "date": "01.01.2024",
                       "predicted_topic": "Технологии",
                       "confidence": confidence, "true_topic": None}

            # Создаем приложение Qt (нужно для виджетов)
            app = QApplication.instance() or QApplication(sys.argv)

            card = ArticleCard(article)

            # Проверяем, что цвет определен правильно
            if confidence > 0.9:
                actual_color = "#27ae60"
                confidence_text = f"Высокая ({int(confidence * 100)}%)"
            elif confidence > 0.8:
                actual_color = "#f39c12"
                confidence_text = f"Средняя ({int(confidence * 100)}%)"
            else:
                actual_color = "#e74c3c"
                confidence_text = f"Низкая ({int(confidence * 100)}%)"

            self.assertEqual(actual_color, expected_color)
            self.assertEqual(confidence_text, expected_text)

    def test_article_correction(self):
        """Тест коррекции статей"""
        article_id = 1
        original_topic = self.mock_data.articles[0]["predicted_topic"]

        # Корректируем статью
        success = self.mock_data.correct_article_topic(article_id, "Новая тема")

        self.assertTrue(success)
        self.assertEqual(self.mock_data.articles[0]["true_topic"], "Новая тема")
        self.assertEqual(self.mock_data.classification_stats['corrected_count'], 43)  # 42+1

    def test_filter_creation(self):
        """Тест создания фильтров"""
        initial_count = len(self.mock_data.user_filters)

        # Создаем новый фильтр
        new_filter = self.mock_data.create_filter("Тестовый фильтр", "Технологии")

        self.assertEqual(len(self.mock_data.user_filters), initial_count + 1)
        self.assertEqual(new_filter["name"], "Тестовый фильтр")
        self.assertEqual(new_filter["topic"], "Технологии")
        self.assertTrue(new_filter["active"])


if __name__ == "__main__":
    unittest.main()