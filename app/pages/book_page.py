import reflex as rx
from app.components.book_layout import book_reading_layout
from app.components.book_detail import book_detail


def book_page() -> rx.Component:
    return book_reading_layout(book_detail())