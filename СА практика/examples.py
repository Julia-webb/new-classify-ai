"""
Примеры работы системы классификации новостей
"""


def show_examples():
    examples = [
        {
            "title": "Пример 1: Статья с высокой уверенностью",
            "input": {
                "title": "Новые меры поддержки бизнеса",
                "content": "Правительство анонсировало новые программы...",
                "confidence": 0.95
            },
            "output": {
                "predicted_topic": "Экономика",
                "color": "Зеленый (#27ae60)",
                "indicator": "Высокая (95%)"
            }
        },
        {
            "title": "Пример 2: Статья с низкой уверенностью",
            "input": {
                "title": "Новые санкции и их влияние",
                "content": "Эксперты оценивают последствия...",
                "confidence": 0.78
            },
            "output": {
                "predicted_topic": "Политика",
                "color": "Красный (#e74c3c)",
                "indicator": "Низкая (78%)"
            }
        },
        {
            "title": "Пример 3: После коррекции",
            "input": {
                "title": "Криптовалюты: новые регуляции",
                "content": "Центральные банки разрабатывают...",
                "confidence": 0.76,
                "corrected_to": "Экономика"
            },
            "output": {
                "predicted_topic": "Экономика",
                "color": "Зеленый (#27ae60)",
                "indicator": "✅ Исправлено (100%)"
            }
        }
    ]

    print("=" * 60)
    print("ПРИМЕРЫ РАБОТЫ СИСТЕМЫ КЛАССИФИКАЦИИ")
    print("=" * 60)

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   Входные данные:")
        print(f"     Заголовок: {example['input']['title']}")
        print(f"     Уверенность: {example['input']['confidence']}")

        if 'corrected_to' in example['input']:
            print(f"     Исправлена на: {example['input']['corrected_to']}")

        print(f"   Результат:")
        print(f"     Тема: {example['output']['predicted_topic']}")
        print(f"     Цвет индикатора: {example['output']['color']}")
        print(f"     Текст: {example['output']['indicator']}")
# Откройте examples.py и добавьте в КОНЕЦ файла:
if __name__ == "__main__":
    show_examples()