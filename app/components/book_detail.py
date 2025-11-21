import reflex as rx
from app.states.book_state import BookState, Chapter, Book


def breadcrumb_item(
    label: str, href: str = None, is_last: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            href,
            rx.el.a(
                label, href=href, class_name="hover:text-indigo-600 transition-colors"
            ),
            rx.el.span(
                label, class_name=rx.cond(is_last, "text-gray-900 font-medium", "")
            ),
        ),
        rx.cond(
            ~is_last, rx.icon("chevron-right", size=14, class_name="text-gray-400 mx-2")
        ),
        class_name="flex items-center text-sm text-gray-500",
    )


def related_book_card(i: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="aspect-[2/3] w-full bg-indigo-50 rounded-md mb-3"),
        rx.el.p("Related Book Title", class_name="font-medium text-gray-900 truncate"),
        rx.el.p("Author Name", class_name="text-xs text-gray-500"),
        class_name="group cursor-pointer hover:-translate-y-1 transition-transform duration-300",
    )


def chapter_view(chapter: Chapter, index: int) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                chapter.title,
                id=chapter.id,
                class_name="text-2xl font-bold text-gray-900 mb-4 scroll-mt-24 group flex items-center gap-2",
            ),
            rx.markdown(
                chapter.content,
                class_name="prose prose-indigo prose-lg max-w-none text-gray-600 leading-relaxed",
            ),
            class_name="mb-12 pb-8 border-b border-gray-100 last:border-0",
        ),
        id="section-" + chapter.id,
    )


def toc_item(chapter: Chapter) -> rx.Component:
    return rx.el.a(
        rx.el.span(chapter.title, class_name="truncate"),
        href="#" + chapter.id,
        class_name="block py-1.5 text-sm text-gray-500 hover:text-indigo-600 hover:pl-1 transition-all border-l-2 border-transparent hover:border-indigo-200 pl-4",
    )


def book_content(book: Book) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                breadcrumb_item("Library", "/"),
                breadcrumb_item(book.category, "#"),
                breadcrumb_item(book.title, is_last=True),
                class_name="flex items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        book.title,
                        class_name="text-4xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=book.cover_image,
                                class_name="size-10 rounded-full border-2 border-white shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    book.author, class_name="font-medium text-gray-900"
                                ),
                                rx.el.p(
                                    book.publish_date,
                                    class_name="text-xs text-gray-500",
                                ),
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        rx.el.div(
                            rx.el.span("•", class_name="text-gray-300"),
                            rx.icon("clock", size=16, class_name="text-gray-400"),
                            rx.el.span(
                                book.read_time,
                                class_name="text-sm text-gray-600 font-medium",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex flex-wrap items-center gap-4",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("printer", size=18),
                        "Print",
                        on_click=BookState.print_book,
                        class_name="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors font-medium text-sm",
                    ),
                    rx.el.button(
                        rx.icon("share-2", size=18),
                        "Share",
                        class_name="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm hover:shadow transition-all font-medium text-sm",
                    ),
                    class_name="flex items-center gap-3 mt-4 md:mt-0",
                ),
                class_name="flex flex-col md:flex-row md:items-start justify-between gap-4",
            ),
            class_name="mb-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    book.chapters, lambda chapter, index: chapter_view(chapter, index)
                ),
                rx.el.div(
                    rx.el.h3(
                        "You might also like",
                        class_name="text-xl font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(range(0, 4), related_book_card),
                        class_name="grid grid-cols-2 md:grid-cols-4 gap-6",
                    ),
                    class_name="mt-16 pt-12 border-t border-gray-100",
                ),
                class_name="col-span-1 lg:col-span-8 lg:pr-12",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "On this page",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4",
                    ),
                    rx.el.nav(
                        rx.foreach(book.chapters, toc_item),
                        class_name="flex flex-col gap-1 border-l border-gray-100",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Reading Progress",
                            class_name="text-xs font-medium text-gray-500 mb-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-full bg-indigo-600 rounded-full transition-all duration-500 ease-out",
                                style={
                                    "width": BookState.reading_progress.to_string()
                                    + "%"
                                },
                            ),
                            class_name="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden",
                        ),
                        rx.el.p(
                            BookState.reading_progress.to_string() + "% completed",
                            class_name="text-xs text-gray-400 mt-2 text-right",
                        ),
                        class_name="mt-8 p-4 bg-gray-50 rounded-xl",
                    ),
                    class_name="sticky top-24",
                ),
                class_name="hidden lg:block col-span-4",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-12",
        ),
        class_name="max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
    )


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-8 w-1/3 bg-gray-200 rounded-md mb-4 animate-pulse"),
        rx.el.div(class_name="h-96 w-full bg-gray-100 rounded-xl mb-8 animate-pulse"),
        rx.el.div(
            rx.foreach(
                range(0, 3),
                lambda i: rx.el.div(
                    class_name="h-4 w-full bg-gray-100 rounded mb-3 animate-pulse"
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="max-w-4xl mx-auto pt-12",
    )


def book_detail() -> rx.Component:
    return rx.cond(
        BookState.is_loading,
        skeleton_loader(),
        rx.cond(
            BookState.current_book,
            book_content(BookState.current_book),
            rx.el.div(
                rx.icon("book-x", size=48, class_name="text-gray-300 mb-4"),
                rx.el.h3(
                    "Book not found", class_name="text-lg font-medium text-gray-900"
                ),
                rx.el.p(
                    "The book you are looking for does not exist or has been removed.",
                    class_name="text-gray-500 mb-6",
                ),
                rx.el.a(
                    "Return to Library",
                    href="/",
                    class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm",
                ),
                class_name="flex flex-col items-center justify-center py-32 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
        ),
    )