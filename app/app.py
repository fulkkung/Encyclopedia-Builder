import reflex as rx
from app.pages.book_page import book_page
from app.pages.index import index_page
from app.states.book_state import BookState
from app.pages.admin import (
    login_page,
    admin_dashboard,
    admin_books_page,
    admin_editor_page,
)
from app.states.auth_state import AuthState
from app.states.admin_state import AdminState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.style("""
            html {
                scroll-behavior: smooth;
            }
            """),
    ],
)
app.add_page(index_page, route="/", on_load=BookState.load_home_data)
app.add_page(book_page, route="/book/[id]", on_load=BookState.load_book)
app.add_page(login_page, route="/login")
app.add_page(
    admin_dashboard,
    route="/admin",
    on_load=[AuthState.check_login, AdminState.load_data],
)
app.add_page(
    admin_books_page,
    route="/admin/books",
    on_load=[AuthState.check_login, AdminState.load_data],
)
app.add_page(
    admin_editor_page, route="/admin/books/editor", on_load=AuthState.check_login
)