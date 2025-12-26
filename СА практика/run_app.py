import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from news_window import MainWindow


def check_dependencies():
    """Проверяет и устанавливает необходимые зависимости"""
    required_packages = ['pandas', 'openpyxl']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("🔍 Обнаружены отсутствующие зависимости...")
        print(f"📦 Установка: {', '.join(missing_packages)}")

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Зависимости успешно установлены!")
        except subprocess.CalledProcessError:
            print("❌ Не удалось установить зависимости.")
            print("💡 Установите вручную: pip install pandas openpyxl")
            return False

    return True


def main():
    print("=" * 60)
    print("🚀 ЗАПУСК NEWS CLASSIFY AI")
    print("=" * 60)
    print("📋 Основные функции:")
    print("  1. 📰 Автоматическая классификация новостей")
    print("  2. ⚙️ Тематические фильтры (И/ИЛИ)")
    print("  3. ✏️ Коррекция классификации")
    print("  4. 📊 Аналитика работы системы")
    print("  5. 💾 Экспорт данных (JSON, CSV, Excel)")
    print("=" * 60)
    print("🔑 ФИЛЬТРАЦИЯ ПО КЛЮЧЕВЫМ СЛОВАМ:")
    print("  - Теперь фильтры работают по содержимому статей")
    print("  - Можно фильтровать по теме и ключевым словам")
    print("  - Логика ИЛИ: статья содержит любое из слов")
    print("  - Логика И: статья содержит все слова")
    print("=" * 60)

    # Проверяем зависимости
    if not check_dependencies():
        print("⚠️ Запуск без поддержки экспорта в Excel...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()