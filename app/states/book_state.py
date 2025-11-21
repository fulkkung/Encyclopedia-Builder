import reflex as rx
import asyncio
from typing import Optional
from pydantic import BaseModel


class Chapter(BaseModel):
    id: str
    title: str
    content: str
    read_time: str


class Book(BaseModel):
    id: str
    title: str
    author: str
    category: str
    publish_date: str
    read_time: str
    cover_image: str
    description: str
    chapters: list[Chapter]


class BookState(rx.State):
    current_book: Optional[Book] = None
    is_loading: bool = True
    reading_progress: int = 0
    active_section: str = ""
    search_query: str = ""
    _books_db: dict[str, Book] = {}
    all_books: list[Book] = []
    categories: list[str] = [
        "Design",
        "Technology",
        "Science",
        "Business",
        "Art",
        "Fiction",
    ]

    @rx.var
    def filtered_books(self) -> list[Book]:
        if not self.search_query:
            return self.all_books
        query = self.search_query.lower()
        return [
            book
            for book in self.all_books
            if query in book.title.lower()
            or query in book.author.lower()
            or query in book.category.lower()
        ]

    def _generate_mock_data(self):
        lorem = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, 
        eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
        """
        self._books_db["1"] = Book(
            id="1",
            title="The Future of Interface Design",
            author="Sarah Chen",
            category="Design",
            publish_date="Oct 14, 2023",
            read_time="15 min read",
            cover_image="https://api.dicebear.com/9.x/shapes/svg?seed=design",
            description="An in-depth look at how AI and spatial computing are reshaping the way we interact with digital products.",
            chapters=[
                Chapter(
                    id="intro",
                    title="Introduction",
                    content=f"The dawn of a new era in UI is upon us. {lorem}",
                    read_time="2 min",
                ),
                Chapter(
                    id="spatial",
                    title="Spatial Computing",
                    content=f"Moving beyond the screen. {lorem} {lorem}",
                    read_time="5 min",
                ),
                Chapter(
                    id="ai-ux",
                    title="AI-Driven UX",
                    content=f"Predictive interfaces are the future. {lorem}",
                    read_time="4 min",
                ),
                Chapter(
                    id="ethics",
                    title="Ethical Considerations",
                    content=f"With great power comes great responsibility. {lorem}",
                    read_time="3 min",
                ),
                Chapter(
                    id="conclusion",
                    title="Conclusion",
                    content=f"What lies ahead? {lorem}",
                    read_time="1 min",
                ),
            ],
        )
        self._books_db["2"] = Book(
            id="2",
            title="The Art of Clean Code",
            author="Robert C. Martin",
            category="Technology",
            publish_date="Aug 1, 2008",
            read_time="12 min read",
            cover_image="https://api.dicebear.com/9.x/shapes/svg?seed=tech",
            description="Even bad code can function. But if code isn't clean, it can bring a development organization to its knees.",
            chapters=[
                Chapter(
                    id="ch1",
                    title="Clean Code",
                    content=f"Code is clean if it can be understood easily. {lorem}",
                    read_time="3 min",
                ),
                Chapter(
                    id="ch2",
                    title="Meaningful Names",
                    content=f"Names are everywhere in software. {lorem}",
                    read_time="4 min",
                ),
            ],
        )
        self._books_db["3"] = Book(
            id="3",
            title="Space Exploration History",
            author="Dr. Neil Tyson",
            category="Science",
            publish_date="Jan 15, 2022",
            read_time="25 min read",
            cover_image="https://api.dicebear.com/9.x/shapes/svg?seed=science",
            description="A journey through the history of human spaceflight, from Vostok to Mars.",
            chapters=[
                Chapter(
                    id="ch1",
                    title="The Early Years",
                    content=f"It started with a dream. {lorem}",
                    read_time="5 min",
                )
            ],
        )
        self._update_public_list()

    def _update_public_list(self):
        self.all_books = list(self._books_db.values())

    @rx.event
    async def load_home_data(self):
        self.is_loading = True
        if not self._books_db:
            self._generate_mock_data()
        else:
            self._update_public_list()
        self.is_loading = False

    @rx.event(background=True)
    async def load_book(self):
        async with self:
            self.is_loading = True
            self.current_book = None
            if not self._books_db:
                self._generate_mock_data()
            else:
                self._update_public_list()
        await asyncio.sleep(0.3)
        async with self:
            params = self.router.page.params
            book_id = params.get("id")
            if isinstance(book_id, list):
                book_id = book_id[0] if book_id else ""
            if not book_id:
                path = self.router.page.path
                if "/book/" in path:
                    parts = path.split("/book/")
                    if len(parts) > 1:
                        book_id = parts[1].split("/")[0]
            book_id = str(book_id) if book_id else ""
            self.current_book = self._books_db.get(book_id)
            self.reading_progress = 0
            self.is_loading = False

    @rx.event
    def set_active_section(self, section_id: str):
        self.active_section = section_id

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def print_book(self):
        return rx.call_script("window.print()")

    @rx.event
    def save_book_to_db(self, book: Book):
        self._books_db[book.id] = book
        self._update_public_list()

    @rx.event
    def delete_book_from_db(self, book_id: str):
        if book_id in self._books_db:
            del self._books_db[book_id]
            self._update_public_list()

    @rx.event
    def add_category(self, category: str):
        if category not in self.categories:
            self.categories.append(category)