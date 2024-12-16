"""
A book reading app
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class BookReader(toga.App):
    def startup(self):
        # Главное окно приложения
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Данные для приложения
        self.available_books = [
            ["Книга 1"],
            ["Книга 2"],
            ["Книга 3"]
        ]

        # Содержимое книг (может быть любым текстом)
        self.book_contents = {
            "Книга 1": "Это содержание Книги 1. Здесь может быть любой текст или история, которую вы хотите показать пользователю.",
            "Книга 2": "Это содержание Книги 2. Здесь представлен другой текст или рассказ.",
            "Книга 3": "Это содержание Книги 3. Здесь может быть еще один текст или информация."
        }

        # Отзывы о книгах
        self.book_reviews = {
            "Книга 1": "Отзыв о Книге 1: Эта книга просто потрясающая! Рекомендую всем к прочтению.",
            "Книга 2": "Отзыв о Книге 2: Очень увлекательный сюжет. Не могла оторваться!",
            "Книга 3": "Отзыв о Книге 3: Книга заставляет задуматься о многих вещах. Отличная работа автора."
        }

        self.favorites = []

        self.genres = [
            ["Фантастика"],
            ["Детектив"],
            ["Роман"]
        ]

        # Создаем таблицы
        self.available_books_table = toga.Table(
            headings=['Доступные книги'],
            data=self.available_books,
            on_select=self.on_available_book_select,
            style=Pack(flex=1)
        )

        self.favorites_table = toga.Table(
            headings=['Избранные книги'],
            data=self.favorites,
            on_select=self.on_favorite_book_select,
            style=Pack(flex=1)
        )

        self.genres_table = toga.Table(
            headings=['Жанры'],
            data=self.genres,
            on_select=self.on_genre_select,
            style=Pack(flex=1)
        )

        # Поле для отображения содержания книги
        self.book_content = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1)
        )

        # Блок с отзывами
        self.reviews_text = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1)
        )

        # Кнопки
        self.add_to_favorites_button = toga.Button(
            'Добавить в избранное',
            on_press=self.add_to_favorites,
            style=Pack(flex=1, padding=5)
        )
        self.read_book_button = toga.Button(
            'Читать книгу',
            on_press=self.read_book,
            style=Pack(flex=1, padding=5)
        )
        self.buttons_box = toga.Box(
            children=[self.add_to_favorites_button, self.read_book_button],
            style=Pack(direction=ROW, padding=5)
        )

        # Компоновка интерфейса
        self.left_box = toga.Box(
            children=[
  toga.Label('Доступные книги', style=Pack(padding=(0, 0, 5, 0))),
                self.available_books_table,
                self.buttons_box
            ],
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )

        self.middle_box = toga.Box(
            children=[
                toga.Label('Содержание книги', style=Pack(padding=(0, 0, 5, 0))),
                self.book_content  # Убрали ScrollContainer
            ],
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )

        self.right_box = toga.Box(
            children=[
                toga.Label('Отзывы', style=Pack(padding=(0, 0, 5, 0))),
                self.reviews_text  # Убрали ScrollContainer
            ],
            style=Pack(direction=COLUMN, padding=5, flex=1)
        )

        self.main_box = toga.Box(
            children=[self.left_box, self.middle_box, self.right_box],
            style=Pack(direction=ROW, flex=1)
        )

        self.main_window.content = self.main_box
        self.main_window.show()

    # Обработчики выбора книг
    def on_available_book_select(self, widget, row):
        if row:
            selected_book = row[0]
            # Отобразим отзыв о выбранной книге
            review = self.book_reviews.get(selected_book, "Отзыв отсутствует.")
            self.reviews_text.value = review

            # Очистим содержание книги при выборе другой книги
            self.book_content.value = ""
        else:
            self.reviews_text.value = ""
            self.book_content.value = ""

    def on_favorite_book_select(self, widget, row):
        if row:
            selected_book = row[0]
            # Здесь вы можете добавить функциональность для избранных книг
            self.main_window.info_dialog('Избранная книга', f'Вы выбрали "{selected_book}" из избранного.')

    def on_genre_select(self, widget, row):
        if row:
            selected_genre = row[0]
            # Здесь вы можете добавить функциональность фильтрации книг по жанру
            self.main_window.info_dialog('Выбранный жанр', f'Вы выбрали жанр "{selected_genre}".')

    # Обработчики кнопок
    def add_to_favorites(self, widget):
        selected_row = self.available_books_table.selection
        if selected_row:
            book_to_add = selected_row[0]
            # Проверяем, есть ли книга уже в избранном
            if [book_to_add] not in self.favorites:
                self.favorites.append([book_to_add])
                self.favorites_table.data = self.favorites
                self.main_window.info_dialog('Успех', f'Книга "{book_to_add}" добавлена в избранное.')
            else:
                self.main_window.error_dialog('Ошибка', f'Книга "{book_to_add}" уже есть в избранном.')
        else:
            self.main_window.error_dialog('Ошибка', 'Пожалуйста, выберите книгу для добавления в избранное.')

    def read_book(self, widget):
        selected_row = self.available_books_table.selection
        if selected_row:
            book_to_read = selected_row[0]
            # Отображаем содержание книги
            content = self.book_contents.get(book_to_read, "Содержание книги отсутствует.")
            self.book_content.value = content
        else:
            self.main_window.error_dialog('Ошибка', 'Пожалуйста, выберите книгу для чтения.')

def main():
    return BookReader()
