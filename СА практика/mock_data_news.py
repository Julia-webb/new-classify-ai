"""
Модуль с улучшенной имитацией ML-модели для NewsClassify AI
Теперь confidence разнообразный для ВСЕХ тем!
"""

import random
import re
from datetime import datetime
from collections import Counter


class MockMLClassifier:
    """Улучшенная имитация ML-модели с разнообразными confidence"""

    def __init__(self):
        # Расширенный словарь ключевых слов с весами
        self.topic_keywords = {
            "Политика": {
                "сильные": ["правительство", "выборы", "президент", "санкции", "законопроект", "депутат"],
                "средние": ["политика", "власть", "голосование", "реформа", "администрация"],
                "слабые": ["политик", "кампания", "переговоры", "дипломатия"]
            },
            "Экономика": {
                "сильные": ["экономика", "инвестиции", "инфляция", "рынок", "бирж", "криптовалют"],
                "средние": ["финансы", "бизнес", "валюта", "банк", "фондовый"],
                "слабые": ["деньги", "стоимость", "прибыль", "убыток", "доход"]
            },
            "Технологии": {
                "сильные": ["искусственный интеллект", "нейросеть", "квантовый", "программирование", "алгоритм"],
                "средние": ["технологии", "гаджет", "стартап", "инновации", "IT", "цифровой"],
                "слабые": ["компьютер", "смартфон", "приложение", "интернет", "софт"]
            },
            "Наука": {
                "сильные": ["научное открытие", "исследование", "эксперимент", "лаборатория", "гипотеза"],
                "средние": ["наука", "ученые", "публикация", "теория", "открытие"],
                "слабые": ["исследователь", "научный", "изучение", "анализ", "метод"]
            },
            "Медицина": {
                "сильные": ["медицина", "диагностика", "вакцина", "лекарство", "терапия", "онкология"],
                "средние": ["здоровье", "врач", "больница", "пациент", "лечение", "профилактика"],
                "слабые": ["медицинский", "клиника", "здоровье", "диагноз", "симптом"]
            },
            "Спорт": {
                "сильные": ["чемпионат", "олимпиада", "футбол", "матч", "победа", "рекорд"],
                "средние": ["спорт", "игрок", "соревнование", "тренировка", "команда"],
                "слабые": ["спортсмен", "игра", "турнир", "соревнования", "лига"]
            },
            "Культура": {
                "сильные": ["культура", "искусство", "музей", "театр", "выставка", "концерт"],
                "средние": ["фильм", "литература", "музыка", "артист", "художник"],
                "слабые": ["культурный", "творчество", "произведение", "исполнитель", "автор"]
            },
            "Образование": {
                "сильные": ["образование", "университет", "студент", "экзамен", "учебник", "курс"],
                "средние": ["школа", "обучение", "преподаватель", "программа", "диплом"],
                "слабые": ["учебный", "занятие", "урок", "лекция", "семинар"]
            }
        }

        # Веса для разных типов ключевых слов
        self.keyword_weights = {
            "сильные": 5.0,
            "средние": 3.0,
            "слабые": 1.0
        }

        # Базовые веса тем
        self.topic_weights = {
            "Политика": 1.0,
            "Экономика": 1.0,
            "Технологии": 1.0,
            "Наука": 1.0,
            "Медицина": 1.0,
            "Спорт": 1.0,
            "Культура": 1.0,
            "Образование": 1.0
        }

        self.training_history = []
        print("✅ Улучшенный ML-классификатор инициализирован")

    def predict_topic(self, title, content):
        """Предсказание темы с разнообразными confidence"""
        combined_text = (title + " " + content).lower()

        # Для каждой темы считаем score
        topic_scores = {}
        for topic, keyword_groups in self.topic_keywords.items():
            score = 0
            base_weight = self.topic_weights[topic]

            for keyword_type, keywords in keyword_groups.items():
                weight = self.keyword_weights[keyword_type]
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    matches = re.findall(pattern, combined_text)
                    if matches:
                        score += weight * len(matches)
                        if keyword in title.lower():
                            score += weight * 2

            score *= base_weight
            score *= random.uniform(0.8, 1.2)  # Вариация
            topic_scores[topic] = score

        # Выбираем лучшую тему
        best_topic = max(topic_scores, key=topic_scores.get)
        best_score = topic_scores[best_topic]

        # Вычисляем confidence
        confidence = self._calculate_confidence(best_score, topic_scores, combined_text, title, best_topic)

        print(f"🎯 ML: '{title[:30]}...' → {best_topic} ({confidence:.0%})")
        return best_topic, confidence

    def _calculate_confidence(self, best_score, all_scores, text, title, best_topic):
        """Расчет confidence с учетом темы"""
        # Отрыв от второй лучшей темы
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_scores) > 1:
            best_score = sorted_scores[0][1]
            second_best = sorted_scores[1][1]
            lead_ratio = (best_score - second_best) / best_score if best_score > 0 else 0
        else:
            lead_ratio = 0

        # Факторы для разных тем (имитируем разную сложность)
        topic_difficulty = {
            "Политика": 0.7,  # Часто междисциплинарная
            "Экономика": 0.6,  # Много цифр и терминов
            "Технологии": 0.8,  # Технические термины
            "Наука": 0.9,  # Сложные концепции
            "Медицина": 0.85,  # Специальная терминология
            "Спорт": 0.5,  # Обычно простая
            "Культура": 0.6,  # Средней сложности
            "Образование": 0.7  # Может быть сложной
        }

        # Базовый confidence на основе отрыва
        if lead_ratio > 0.5:
            base_confidence = 0.93
        elif lead_ratio > 0.3:
            base_confidence = 0.85
        elif lead_ratio > 0.1:
            base_confidence = 0.75
        else:
            base_confidence = 0.65

        # Учет сложности темы
        difficulty = topic_difficulty.get(best_topic, 0.7)
        difficulty_factor = 1.0 - (difficulty * 0.15)

        # Длина текста
        word_count = len(text.split())
        if word_count < 50:
            length_factor = 1.1
        elif word_count < 150:
            length_factor = 1.0
        else:
            length_factor = 0.9

        # Ключевые слова в заголовке
        title_has_keywords = any(
            keyword in title.lower()
            for keyword_group in self.topic_keywords[best_topic].values()
            for keyword in keyword_group
        )
        title_factor = 1.15 if title_has_keywords else 1.0

        # Итоговый confidence
        final_confidence = base_confidence * difficulty_factor * length_factor * title_factor
        final_confidence *= random.uniform(0.97, 1.03)

        # Ограничиваем и округляем
        final_confidence = max(0.6, min(0.98, final_confidence))
        return round(final_confidence, 2)

    def learn_from_correction(self, article_id, old_topic, new_topic):
        """Обучение на коррекции"""
        self.training_history.append({
            "article_id": article_id,
            "old_topic": old_topic,
            "new_topic": new_topic,
            "timestamp": datetime.now()
        })

        if new_topic in self.topic_weights:
            self.topic_weights[new_topic] = min(2.0, self.topic_weights[new_topic] + 0.07)

        if old_topic in self.topic_weights:
            self.topic_weights[old_topic] = max(0.5, self.topic_weights[old_topic] - 0.04)

        print(f"📚 ML обучение: {old_topic} → {new_topic}")


class MockNewsData:
    def __init__(self):
        self.ml_classifier = MockMLClassifier()
        self.available_topics = list(self.ml_classifier.topic_keywords.keys())
        self.articles = self._generate_diverse_articles()
        self.user_filters = []
        self.classification_stats = self._calculate_stats()
        self.correction_history = []

        # Добавляем тестовые фильтры
        self._add_test_filters()

        print(f"✅ Сгенерировано {len(self.articles)} статей")
        print(f"📊 Статьи распределены по confidence:")
        self._show_confidence_distribution()

    def _add_test_filters(self):
        """Добавляет тестовые фильтры для демонстрации"""
        print("\n🔧 Создание тестовых фильтров...")

        # Фильтр 1: ИИ в медицине
        self.create_filter(
            name="ИИ в медицине",
            topic="Медицина",
            keywords=["искусственный интеллект", "диагностика", "нейросеть"],
            logic="OR"
        )

        # Фильтр 2: Крипто-инвестиции
        self.create_filter(
            name="Крипто-инвестиции",
            topic="Экономика",
            keywords=["криптовалют", "биткоин", "инвестици"],
            logic="OR"
        )

        # Фильтр 3: Высокие технологии
        self.create_filter(
            name="Высокие технологии",
            topic="Технологии",
            keywords=["квантовый", "искусственный интеллект", "нейросеть"],
            logic="OR"
        )

        # Фильтр 4: Строгий фильтр (И логика)
        self.create_filter(
            name="Сложные мед исследования",
            topic="Медицина",
            keywords=["исследование", "ученые", "вакцин"],
            logic="AND"
        )

        # Фильтр 5: Фильтр без темы
        self.create_filter(
            name="Инвестиции и стартапы",
            topic=None,
            keywords=["инвестиции", "стартап", "финансирование"],
            logic="OR"
        )

        print(f"✅ Создано {len(self.user_filters)} тестовых фильтров")

    def _generate_diverse_articles(self):
        """Генерирует статьи с РАЗНООБРАЗНЫМИ confidence для всех тем"""
        article_templates = [
            # ВЫСОКИЙ CONFIDENCE (>90%) - разные темы
            {"title": "Президент подписал новый закон о выборах",
             "content": "Документ вносит изменения в избирательное законодательство.",
             "source": "Ведомости", "date": "10.01.2024", "target_confidence": "high"},

            {"title": "Фондовый рынок показал рекордный рост",
             "content": "Основные индексы выросли на 3-5% за торговую сессию.",
             "source": "РБК", "date": "15.01.2024", "target_confidence": "high"},

            {"title": "Новый квантовый компьютер установил рекорд",
             "content": "Ученые представили процессор с 512 кубитами.",
             "source": "Хабр", "date": "14.01.2024", "target_confidence": "high"},

            {"title": "Утверждена вакцина от сезонного гриппа",
             "content": "Минздрав одобрил препарат с эффективностью 95%.",
             "source": "Медпортал", "date": "13.01.2024", "target_confidence": "high"},

            {"title": "Финальный матч чемпионата мира по футболу",
             "content": "Сборная Аргентины обыграла Бразилию со счетом 3:2.",
             "source": "Спорт-Экспресс", "date": "07.01.2024", "target_confidence": "high"},

            # СРЕДНИЙ CONFIDENCE (80-90%) - разные темы
            {"title": "Экономические реформы и их влияние",
             "content": "Эксперты обсуждают последствия изменений в налоговом кодексе.",
             "source": "Ведомости", "date": "09.01.2024", "target_confidence": "medium"},

            {"title": "Кибербезопасность в современном мире",
             "content": "Специалисты обсуждают методы защиты от кибератак.",
             "source": "SecurityLab", "date": "08.01.2024", "target_confidence": "medium"},

            {"title": "Климатические исследования и их значение",
             "content": "Ученые представили данные о глобальном потеплении.",
             "source": "Nature", "date": "06.01.2024", "target_confidence": "medium"},

            {"title": "Дистанционное обучение: преимущества и недостатки",
             "content": "Исследование показало результаты онлайн-образования.",
             "source": "Education Week", "date": "05.01.2024", "target_confidence": "medium"},

            {"title": "Цифровое искусство в современных музеях",
             "content": "Музеи начинают приобретать цифровые произведения.",
             "source": "ArtNews", "date": "04.01.2024", "target_confidence": "medium"},

            # НИЗКИЙ CONFIDENCE (60-80%) - разные темы
            {"title": "Искусственный интеллект в медицинской диагностике",
             "content": "Нейросети помогают врачам в анализе медицинских снимков.",
             "source": "N+1", "date": "11.01.2024", "target_confidence": "low"},

            {"title": "Цифровизация образовательной системы",
             "content": "Технологии меняют подход к обучению в школах и вузах.",
             "source": "Коммерсант", "date": "12.01.2024", "target_confidence": "low"},

            {"title": "Научные исследования в области биотехнологий",
             "content": "Ученые работают над созданием новых сортов растений.",
             "source": "AgroNews", "date": "03.01.2024", "target_confidence": "low"},

            {"title": "Финансирование технологических стартапов",
             "content": "Инвесторы вкладывают средства в перспективные проекты.",
             "source": "Bloomberg", "date": "02.01.2024", "target_confidence": "low"},

            {"title": "Спортивная аналитика и использование данных",
             "content": "Команды применяют big data для анализа выступлений.",
             "source": "SportsTech", "date": "01.01.2024", "target_confidence": "low"},

            # Дополнительные статьи для баланса
            {"title": "Разработка программного обеспечения для науки",
             "content": "IT-компании создают софт для исследовательских задач.",
             "source": "Хабр", "date": "31.12.2023", "target_confidence": "medium"},

            {"title": "Музейные технологии и виртуальная реальность",
             "content": "Экспозиции становятся интерактивными с помощью VR.",
             "source": "Культура.рф", "date": "30.12.2023", "target_confidence": "medium"},

            {"title": "Экономика и экология: поиск баланса",
             "content": "Предприятия внедряют зеленые технологии.",
             "source": "ЭкоНовости", "date": "29.12.2023", "target_confidence": "low"},

            {"title": "Медицинские исследования и этика",
             "content": "Ученые обсуждают вопросы биоэтики в экспериментах.",
             "source": "Медновости", "date": "28.12.2023", "target_confidence": "low"},

            {"title": "Политика и международные отношения",
             "content": "Страны обсуждают новые форматы сотрудничества.",
             "source": "Euronews", "date": "27.12.2023", "target_confidence": "medium"},

            # Статьи специально для тестирования фильтров
            {"title": "Искусственный интеллект в диагностике рака",
             "content": "Нейросети показали высокую точность в обнаружении опухолей на ранних стадиях.",
             "source": "Медновости", "date": "16.01.2024", "target_confidence": "high"},

            {"title": "Инвестиции в криптовалюты достигли рекордного уровня",
             "content": "Биткоин привлек более 10 млрд долларов инвестиций в этом году.",
             "source": "РБК", "date": "17.01.2024", "target_confidence": "high"},

            {"title": "Квантовый компьютер для медицинских исследований",
             "content": "Ученые используют квантовые вычисления для разработки новых лекарств.",
             "source": "Хабр", "date": "18.01.2024", "target_confidence": "medium"},
        ]

        articles = []

        for i, template in enumerate(article_templates, 1):
            # Получаем предсказание от ML
            predicted_topic, confidence = self.ml_classifier.predict_topic(
                template["title"], template["content"]
            )

            # Корректируем confidence для соответствия целевой группе
            if template["target_confidence"] == "high":
                # Увеличиваем confidence для высоких
                confidence = min(0.98, confidence * 1.1)
            elif template["target_confidence"] == "low":
                # Уменьшаем для низких
                confidence = max(0.6, confidence * 0.85)
            # Для medium оставляем как есть (80-90%)

            confidence = round(confidence, 2)

            article = {
                "id": i,
                "title": template["title"],
                "content": template["content"],
                "source": template["source"],
                "date": template["date"],
                "predicted_topic": predicted_topic,
                "confidence": confidence,
                "true_topic": None
            }

            articles.append(article)

        return articles

    def _show_confidence_distribution(self):
        """Показывает распределение confidence по темам"""
        print("\n📊 РАСПРЕДЕЛЕНИЕ CONFIDENCE ПО ТЕМАМ:")
        print("-" * 50)

        for topic in self.available_topics:
            topic_articles = [a for a in self.articles if a["predicted_topic"] == topic]
            if topic_articles:
                confidences = [a["confidence"] for a in topic_articles]
                avg_conf = sum(confidences) / len(confidences)

                # Количество в каждой группе
                high = len([c for c in confidences if c > 0.9])
                medium = len([c for c in confidences if 0.8 <= c <= 0.9])
                low = len([c for c in confidences if c < 0.8])

                print(f"\n{topic}:")
                print(f"  📈 Средний confidence: {avg_conf:.1%}")
                print(f"  🟢 Высокая: {high} статей")
                print(f"  🟠 Средняя: {medium} статей")
                print(f"  🔴 Низкая: {low} статей")

    def _calculate_stats(self):
        """Вычисляет статистику"""
        total = len(self.articles)

        high = len([a for a in self.articles if a["confidence"] > 0.9])
        medium = len([a for a in self.articles if 0.8 <= a["confidence"] <= 0.9])
        low = len([a for a in self.articles if a["confidence"] < 0.8])

        return {
            "precision": 0.87,
            "recall": 0.82,
            "f1_score": 0.85,
            "total_articles": total,
            "corrected_count": 0,
            "high_confidence": high,
            "medium_confidence": medium,
            "low_confidence": low,
            "avg_confidence": sum(a["confidence"] for a in self.articles) / total if total > 0 else 0
        }

    def get_articles_by_filter(self, filter_topic=None):
        if not filter_topic or filter_topic == "Все темы":
            return self.articles

        return [article for article in self.articles
                if article["predicted_topic"] == filter_topic]

    def get_articles_by_keywords(self, keywords, logic="OR", topic=None):
        """Фильтрует статьи по ключевым словам с указанной логикой"""
        if not keywords:
            return []

        filtered_articles = []

        for article in self.articles:
            # Если указана тема, сначала проверяем её
            if topic and article["predicted_topic"] != topic:
                continue

            combined_text = (article["title"] + " " + article["content"]).lower()

            if logic == "OR":
                # Статья должна содержать ХОТЯ БЫ ОДНО из ключевых слов
                for keyword in keywords:
                    if keyword.lower() in combined_text:
                        filtered_articles.append(article)
                        break
            elif logic == "AND":
                # Статья должна содержать ВСЕ ключевые слова
                all_present = True
                for keyword in keywords:
                    if keyword.lower() not in combined_text:
                        all_present = False
                        break
                if all_present:
                    filtered_articles.append(article)

        return filtered_articles

    def correct_article_topic(self, article_id, correct_topic):
        """Корректирует тему статьи"""
        for article in self.articles:
            if article["id"] == article_id:
                old_topic = article["predicted_topic"]
                old_confidence = article["confidence"]

                article["predicted_topic"] = correct_topic
                article["confidence"] = 1.0
                article["true_topic"] = correct_topic

                self.ml_classifier.learn_from_correction(article_id, old_topic, correct_topic)

                self.correction_history.append({
                    "article_id": article_id,
                    "old_topic": old_topic,
                    "new_topic": correct_topic,
                    "old_confidence": old_confidence,
                    "new_confidence": 1.0,
                    "date": article["date"],
                    "title": article["title"][:30] + "..."
                })

                self.classification_stats['corrected_count'] += 1

                if self.classification_stats['corrected_count'] % 5 == 0:
                    self.classification_stats['precision'] = min(
                        0.98, self.classification_stats['precision'] + 0.01
                    )

                print(f"✅ Статья {article_id} исправлена: {old_topic} → {correct_topic}")
                return True

        return False

    def create_filter(self, name, topic=None, keywords=None, logic="OR"):
        """Создает фильтр с ключевыми словами"""
        new_filter = {
            "id": len(self.user_filters) + 1,
            "name": name,
            "topic": topic,
            "keywords": keywords or [],
            "logic": logic,
            "active": True,
            "created": "2024-01-15"
        }
        self.user_filters.append(new_filter)

        # Тестовый вывод для отладки
        if keywords:
            print(f"🔍 Создан фильтр с ключевыми словами: {keywords}")
            # Проверим сразу, сколько статей подходит под этот фильтр
            test_articles = self.get_articles_by_keywords(keywords, logic, topic)
            print(f"🔍 Тест: найдено {len(test_articles)} статей для фильтра '{name}'")

        return new_filter

    def get_active_filters(self):
        return [f for f in self.user_filters if f["active"]]


# Глобальный экземпляр
mock_data = MockNewsData()