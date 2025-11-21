import reflex as rx
import uuid
from typing import Optional
from app.states.book_state import BookState, Book, Chapter
from app.states.auth_state import AuthState
import datetime


class AdminState(rx.State):
    is_editing: bool = False
    form_id: str = ""
    form_title: str = ""
    form_author: str = ""
    form_category: str = ""
    form_description: str = ""
    form_cover_image: str = ""
    form_chapters: list[Chapter] = []
    editing_chapter_index: int = -1
    new_category_name: str = ""

    @rx.var
    def total_books_count(self) -> int:
        return len(self.all_books_list)

    @rx.var
    def all_books_list(self) -> list[Book]:
        return []

    @rx.event
    async def load_data(self):
        bs = await self.get_state(BookState)
        if not bs._books_db:
            bs._generate_mock_data()

    @rx.event
    def start_new_book(self):
        self.is_editing = False
        self.form_id = str(uuid.uuid4())
        self.form_title = ""
        self.form_author = ""
        self.form_category = "Design"
        self.form_description = ""
        self.form_cover_image = (
            f"https://api.dicebear.com/9.x/shapes/svg?seed={self.form_id}"
        )
        self.form_chapters = []
        return rx.redirect("/admin/books/editor")

    @rx.event
    def edit_book(self, book: Book):
        self.is_editing = True
        self.form_id = book.id
        self.form_title = book.title
        self.form_author = book.author
        self.form_category = book.category
        self.form_description = book.description
        self.form_cover_image = book.cover_image
        self.form_chapters = book.chapters
        return rx.redirect(f"/admin/books/editor")

    @rx.event
    async def save_book(self):
        if not self.form_title or not self.form_author:
            return rx.window_alert("Title and Author are required.")
        new_book = Book(
            id=self.form_id,
            title=self.form_title,
            author=self.form_author,
            category=self.form_category,
            description=self.form_description,
            cover_image=self.form_cover_image,
            publish_date=datetime.datetime.now().strftime("%b %d, %Y"),
            read_time="10 min read",
            chapters=self.form_chapters,
        )
        bs = await self.get_state(BookState)
        bs.save_book_to_db(new_book)
        return rx.redirect("/admin/books")

    @rx.event
    async def delete_book(self, book_id: str):
        bs = await self.get_state(BookState)
        bs.delete_book_from_db(book_id)

    @rx.event
    def add_chapter(self):
        new_id = str(uuid.uuid4())[:8]
        self.form_chapters.append(
            Chapter(
                id=new_id,
                title="New Chapter",
                content="Write your content here...",
                read_time="5 min",
            )
        )

    @rx.event
    def update_chapter_field(self, index: int, field: str, value: str):
        if 0 <= index < len(self.form_chapters):
            old_chapter = self.form_chapters[index]
            data = {
                "id": old_chapter.id,
                "title": old_chapter.title,
                "content": old_chapter.content,
                "read_time": old_chapter.read_time,
            }
            data[field] = value
            self.form_chapters[index] = Chapter(**data)

    @rx.event
    def remove_chapter(self, index: int):
        if 0 <= index < len(self.form_chapters):
            self.form_chapters.pop(index)

    @rx.event
    async def create_category(self):
        if self.new_category_name:
            bs = await self.get_state(BookState)
            bs.add_category(self.new_category_name)
            self.new_category_name = ""