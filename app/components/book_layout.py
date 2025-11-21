import reflex as rx
from app.components.layout import sidebar, navbar


def book_reading_layout(content: rx.Component) -> rx.Component:
    """
    A dedicated layout for the book reading page.
    It includes the sidebar and navbar but offers a specialized container for reading content.
    """
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                content,
                class_name="flex-1 w-full bg-gray-50/50 min-h-screen p-4 md:p-8 overflow-x-hidden",
                id="book-main-content",
            ),
            class_name="flex-1 flex flex-col min-w-0 min-h-screen bg-white",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-white",
    )