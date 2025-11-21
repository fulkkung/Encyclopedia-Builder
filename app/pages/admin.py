import reflex as rx
from app.states.auth_state import AuthState
from app.states.admin_state import AdminState
from app.states.book_state import BookState, Book
from app.components.admin_layout import admin_layout


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Admin Access",
                class_name="text-2xl font-bold text-gray-900 mb-2 text-center",
            ),
            rx.el.p(
                "Please sign in to continue",
                class_name="text-gray-500 text-sm mb-8 text-center",
            ),
            rx.el.div(
                rx.el.label(
                    "Username",
                    class_name="text-sm font-medium text-gray-700 mb-1 block",
                ),
                rx.el.input(
                    placeholder="Enter username",
                    on_change=AuthState.set_username,
                    class_name="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                    default_value=AuthState.username,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-sm font-medium text-gray-700 mb-1 block",
                ),
                rx.el.input(
                    type="password",
                    placeholder="Enter password",
                    on_change=AuthState.set_password,
                    class_name="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                    default_value=AuthState.password,
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.error_message,
                rx.el.div(
                    rx.icon("circle-alert", size=16, class_name="text-red-600"),
                    AuthState.error_message,
                    class_name="mb-6 p-3 bg-red-50 text-red-600 text-sm rounded-lg flex items-center gap-2",
                ),
            ),
            rx.el.button(
                "Sign In",
                on_click=AuthState.login,
                class_name="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors shadow-sm",
            ),
            class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4",
    )


def stat_card(label: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=24, class_name=f"text-{color}-600"),
            class_name=f"p-3 bg-{color}-50 rounded-xl",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            stat_card(
                "Total Books",
                BookState.all_books.length().to_string(),
                "book",
                "indigo",
            ),
            stat_card(
                "Categories",
                BookState.categories.length().to_string(),
                "tag",
                "emerald",
            ),
            stat_card("Total Chapters", "12", "file-text", "amber"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3("Quick Actions", class_name="font-bold text-gray-900 mb-4"),
                rx.el.div(
                    rx.el.button(
                        rx.icon("plus", size=20),
                        "Add New Book",
                        on_click=AdminState.start_new_book,
                        class_name="flex flex-col items-center justify-center gap-2 p-6 bg-white border border-dashed border-gray-300 rounded-xl hover:border-indigo-500 hover:bg-indigo-50 hover:text-indigo-600 transition-all text-gray-500 font-medium h-32",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                ),
            ),
            class_name="mb-8",
        ),
    )


def admin_dashboard() -> rx.Component:
    return admin_layout(rx.el.div(dashboard_content(), class_name="p-8"))


def book_row(book: Book) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=book.cover_image,
                    class_name="size-10 rounded object-cover bg-gray-100",
                ),
                rx.el.span(book.title, class_name="font-medium text-gray-900"),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(book.author, class_name="px-6 py-4 text-gray-500"),
        rx.el.td(
            rx.el.span(
                book.category,
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", size=16),
                    on_click=lambda: AdminState.edit_book(book),
                    class_name="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16),
                    on_click=lambda: AdminState.delete_book(book.id),
                    class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-2 justify-end",
            ),
            class_name="px-6 py-4 text-right",
        ),
        class_name="border-b border-gray-50 hover:bg-gray-50/50 transition-colors",
    )


def books_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Books", class_name="text-2xl font-bold text-gray-900"),
            rx.el.button(
                rx.icon("plus", size=18),
                "Add Book",
                on_click=AdminState.start_new_book,
                class_name="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors text-sm shadow-sm",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Title",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Author",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Category",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(BookState.all_books, book_row),
                    class_name="bg-white divide-y divide-gray-100",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm",
        ),
    )


def admin_books_page() -> rx.Component:
    return admin_layout(rx.el.div(books_content(), class_name="p-8"))


def chapter_editor_item(chapter: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                f"Chapter {index + 1}",
                class_name="text-xs font-bold text-indigo-600 uppercase tracking-wide mb-2 block",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Chapter Title",
                    on_change=lambda val: AdminState.update_chapter_field(
                        index, "title", val
                    ),
                    class_name="w-full text-lg font-bold text-gray-900 border-none focus:ring-0 p-0 placeholder:text-gray-300 mb-2 bg-transparent",
                    default_value=chapter["title"],
                ),
                rx.el.textarea(
                    placeholder="Write chapter content here (Markdown supported)...",
                    on_change=lambda val: AdminState.update_chapter_field(
                        index, "content", val
                    ),
                    class_name="w-full min-h-[150px] text-gray-600 resize-y border-gray-100 focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100 rounded-md text-sm p-3 bg-gray-50",
                    default_value=chapter["content"],
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Read time (e.g. 5 min)",
                        on_change=lambda val: AdminState.update_chapter_field(
                            index, "read_time", val
                        ),
                        class_name="text-xs text-gray-400 border-none bg-transparent p-0 focus:ring-0 width-24",
                        default_value=chapter["read_time"],
                    ),
                    rx.el.button(
                        rx.icon("trash-2", size=14),
                        "Remove",
                        on_click=lambda: AdminState.remove_chapter(index),
                        class_name="text-xs text-red-400 hover:text-red-600 flex items-center gap-1 transition-colors",
                    ),
                    class_name="flex items-center justify-between mt-2",
                ),
            ),
            class_name="flex-1",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow group",
    )


def editor_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                rx.cond(AdminState.is_editing, "Edit Book", "New Book"),
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=rx.redirect("/admin/books"),
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg font-medium transition-colors text-sm",
                ),
                rx.el.button(
                    "Save Book",
                    on_click=AdminState.save_book,
                    class_name="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors text-sm shadow-sm",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Book Details",
                        class_name="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 block",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Title",
                            class_name="text-xs font-medium text-gray-500 mb-1 block",
                        ),
                        rx.el.input(
                            on_change=AdminState.set_form_title,
                            placeholder="Book Title",
                            class_name="w-full px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all mb-4",
                            default_value=AdminState.form_title,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Author",
                            class_name="text-xs font-medium text-gray-500 mb-1 block",
                        ),
                        rx.el.input(
                            on_change=AdminState.set_form_author,
                            placeholder="Author Name",
                            class_name="w-full px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all mb-4",
                            default_value=AdminState.form_author,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Category",
                            class_name="text-xs font-medium text-gray-500 mb-1 block",
                        ),
                        rx.el.select(
                            rx.foreach(
                                BookState.categories, lambda c: rx.el.option(c, value=c)
                            ),
                            value=AdminState.form_category,
                            on_change=AdminState.set_form_category,
                            class_name="w-full px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all mb-4 bg-white",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Description",
                            class_name="text-xs font-medium text-gray-500 mb-1 block",
                        ),
                        rx.el.textarea(
                            on_change=AdminState.set_form_description,
                            placeholder="Short description of the book...",
                            class_name="w-full px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all mb-4 h-24 resize-none",
                            default_value=AdminState.form_description,
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                ),
                class_name="col-span-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Chapters",
                        class_name="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 block",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AdminState.form_chapters,
                            lambda c, i: chapter_editor_item(c, i),
                        ),
                        class_name="space-y-4 mb-4",
                    ),
                    rx.el.button(
                        rx.icon("plus", size=16),
                        "Add Chapter",
                        on_click=AdminState.add_chapter,
                        class_name="w-full py-3 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 font-medium hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all flex items-center justify-center gap-2",
                    ),
                ),
                class_name="col-span-2",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
        ),
    )


def admin_editor_page() -> rx.Component:
    return admin_layout(rx.el.div(editor_content(), class_name="p-8"))