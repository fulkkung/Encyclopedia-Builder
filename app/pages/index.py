import reflex as rx
from app.components.layout import dashboard_layout
from app.states.book_state import BookState, Book


def book_card(book: Book) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=book.cover_image,
                    class_name="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105",
                ),
                class_name="aspect-[2/3] w-full bg-gray-100 rounded-md mb-3 overflow-hidden shadow-sm",
            ),
            rx.el.h3(
                book.title,
                class_name="font-bold text-gray-900 mb-1 truncate group-hover:text-indigo-600 transition-colors",
            ),
            rx.el.p(book.author, class_name="text-sm text-gray-500"),
            class_name="group cursor-pointer hover:-translate-y-1 transition-all duration-300",
        ),
        href=f"/book/{book.id}",
    )


def home_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Library", class_name="text-3xl font-bold text-gray-900"),
            rx.el.p(
                "Explore our curated collection of knowledge.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            BookState.is_loading,
            rx.el.div(
                rx.foreach(
                    range(5),
                    lambda i: rx.el.div(
                        class_name="aspect-[2/3] bg-gray-100 rounded-md animate-pulse"
                    ),
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8",
            ),
            rx.el.div(
                rx.cond(
                    BookState.filtered_books.length() > 0,
                    rx.el.div(
                        rx.foreach(BookState.filtered_books, book_card),
                        class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8",
                    ),
                    rx.el.div(
                        rx.icon("search-x", size=48, class_name="text-gray-300 mb-4"),
                        rx.el.h3(
                            "No books found",
                            class_name="text-lg font-medium text-gray-900",
                        ),
                        rx.el.p(
                            "Try adjusting your search query",
                            class_name="text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center py-20 col-span-full",
                    ),
                )
            ),
        ),
    )


def index_page() -> rx.Component:
    return dashboard_layout(home_content())