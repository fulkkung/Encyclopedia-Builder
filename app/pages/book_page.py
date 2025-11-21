import reflex as rx
from app.components.book_detail import book_detail
from app.components.book_layout import book_reading_layout


def book_page() -> rx.Component:
    return book_reading_layout(book_detail())