import reflex as rx
from app.components.layout import dashboard_layout
from app.components.book_detail import book_detail


def book_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(book_detail(), class_name="w-full bg-gray-50 min-h-screen")
    )