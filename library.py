import uuid
import json
import os


class Book:
    def __init__(self, id=None, title=None, author=None, year=None, status="в наличии"):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )

    def __str__(self):
        return f"ID: {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтатус: {self.status}\n"


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def add_book(self, title, author, year):
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book.id}.\n")

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.\n")
                return
        print(f"Книга с ID {book_id} не найдена.\n")

    def search_books(self, query, field):
        results = []
        for book in self.books:
            if field == "title" and query.lower() in book.title.lower():
                results.append(book)
            elif field == "author" and query.lower() in book.author.lower():
                results.append(book)
            elif field == "year" and query == book.year:
                results.append(book)
        return results

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.\n")
        else:
            for book in self.books:
                print(book)

    def change_status(self, book_id, new_status):
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    print(f"Статус книги с ID {book_id} изменён на '{new_status}'.\n")
                else:
                    print("Некорректный статус. Используйте 'в наличии' или 'выдана'.\n")
                return
        print(f"Книга с ID {book_id} не найдена.\n")

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        return []


def main():
    library = Library()

    while True:
        print("Меню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            library.remove_book(book_id)
        elif choice == "3":
            print("Поиск книги:")
            field = input("Введите поле для поиска (title, author, year): ").lower()
            query = input("Введите значение для поиска: ")
            results = library.search_books(query, field)
            if results:
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.\n")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.\n")


if __name__ == "__main__":
    main()
