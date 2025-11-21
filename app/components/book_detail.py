import reflex as rx
from app.states.book_state import BookState, Chapter, Book


def breadcrumb_item(
    label: str, href: str = None, is_last: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            href,
            rx.el.a(
                label,
                href=href,
                class_name="hover:text-indigo-600 transition-colors text-gray-500 font-medium",
            ),
            rx.el.span(
                label,
                class_name=rx.cond(
                    is_last, "text-gray-900 font-semibold", "text-gray-500"
                ),
            ),
        ),
        rx.cond(
            ~is_last, rx.icon("chevron-right", size=14, class_name="text-gray-400 mx-2")
        ),
        class_name="flex items-center text-sm",
    )


def book_header_section(book: Book) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            breadcrumb_item("Library", "/"),
            breadcrumb_item(book.category, "#"),
            breadcrumb_item(book.title, is_last=True),
            class_name="flex items-center mb-6 overflow-x-auto no-scrollbar whitespace-nowrap",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    book.title,
                    class_name="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 mb-6 tracking-tight leading-tight",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=book.cover_image,
                            class_name="size-12 rounded-full border-2 border-white shadow-sm bg-gray-100",
                        ),
                        rx.el.div(
                            rx.el.p(
                                book.author,
                                class_name="font-semibold text-gray-900 leading-tight",
                            ),
                            rx.el.p(
                                book.publish_date,
                                class_name="text-xs text-gray-500 font-medium",
                            ),
                            class_name="flex flex-col justify-center",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("clock", size=16, class_name="text-indigo-500"),
                            rx.el.span(
                                book.read_time,
                                class_name="text-sm text-gray-600 font-medium",
                            ),
                            class_name="flex items-center gap-2 bg-indigo-50 px-3 py-1 rounded-full",
                        ),
                        rx.el.button(
                            rx.icon("bookmark", size=18),
                            class_name="p-2 text-gray-400 hover:text-indigo-600 hover:bg-gray-100 rounded-full transition-all",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-8",
                ),
                class_name="flex-1",
            ),
            class_name="flex flex-col gap-6",
        ),
        class_name="mb-12",
    )


def chapter_content_block(chapter: Chapter, index: int) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"Chapter {index + 1}",
                    class_name="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-2 block",
                ),
                rx.el.h2(
                    chapter.title,
                    class_name="text-2xl md:text-3xl font-bold text-gray-900 mb-6 group flex items-center gap-2",
                ),
                id=chapter.id,
                class_name="scroll-mt-32",
            ),
            rx.el.div(
                rx.markdown(
                    chapter.content,
                    class_name="prose prose-indigo prose-lg max-w-none text-gray-600 leading-relaxed prose-headings:text-gray-900 prose-headings:font-bold prose-p:text-gray-600 prose-a:text-indigo-600 hover:prose-a:text-indigo-700",
                ),
                class_name="bg-white",
            ),
            class_name="mb-16 pb-10 border-b border-gray-100 last:border-0 last:pb-0 last:mb-0",
        ),
        id="section-" + chapter.id,
    )


def toc_sidebar_item(chapter: Chapter) -> rx.Component:
    return rx.el.a(
        rx.el.span(chapter.title, class_name="truncate"),
        href="#" + chapter.id,
        class_name="block py-2 text-sm text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-md px-3 transition-all",
    )


def sidebar_section(book: Book) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Table of Contents",
                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-3",
            ),
            rx.el.nav(
                rx.foreach(book.chapters, toc_sidebar_item),
                class_name="flex flex-col gap-0.5 mb-8",
            ),
            rx.el.div(
                rx.el.p(
                    "Actions",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-3",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("printer", size=16),
                        "Print Book",
                        on_click=BookState.print_book,
                        class_name="flex items-center gap-3 w-full px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors text-left",
                    ),
                    rx.el.button(
                        rx.icon("share-2", size=16),
                        "Share Link",
                        class_name="flex items-center gap-3 w-full px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors text-left",
                    ),
                    class_name="flex flex-col gap-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.p(
                    "Reading Progress",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 px-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            class_name="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-500 ease-out",
                            style={
                                "width": BookState.reading_progress.to_string() + "%"
                            },
                        ),
                        class_name="h-2 w-full bg-gray-100 rounded-full overflow-hidden",
                    ),
                    rx.el.p(
                        BookState.reading_progress.to_string() + "% completed",
                        class_name="text-xs text-gray-400 mt-2 text-right font-medium",
                    ),
                    class_name="p-4 bg-gray-50 rounded-xl border border-gray-100",
                ),
            ),
            class_name="sticky top-24 max-h-[calc(100vh-8rem)] overflow-y-auto pr-2",
        ),
        class_name="hidden lg:block col-span-1 lg:col-span-3 xl:col-span-3 pl-8 border-l border-gray-100",
    )


def book_content(book: Book) -> rx.Component:
    return rx.el.div(
        book_header_section(book),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    book.chapters,
                    lambda chapter, index: chapter_content_block(chapter, index),
                ),
                rx.el.div(
                    rx.el.h3(
                        "End of Book",
                        class_name="text-center text-sm font-bold text-gray-400 uppercase tracking-widest mb-4",
                    ),
                    rx.el.div(class_name="h-px w-full bg-gray-100"),
                    class_name="mt-24 pt-12 pb-12",
                ),
                class_name="col-span-1 lg:col-span-9 xl:col-span-9",
            ),
            sidebar_section(book),
            class_name="grid grid-cols-1 lg:grid-cols-12 gap-8",
        ),
        class_name="max-w-6xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
    )


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="w-32 h-4 bg-gray-200 rounded mb-6 animate-pulse"),
        rx.el.div(class_name="w-3/4 h-16 bg-gray-200 rounded-lg mb-8 animate-pulse"),
        rx.el.div(
            rx.el.div(class_name="size-12 rounded-full bg-gray-200 animate-pulse"),
            rx.el.div(
                rx.el.div(class_name="w-32 h-4 bg-gray-200 rounded animate-pulse"),
                rx.el.div(class_name="w-24 h-3 bg-gray-200 rounded animate-pulse"),
                class_name="space-y-2",
            ),
            class_name="flex gap-4 mb-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="w-full h-64 bg-gray-100 rounded-xl animate-pulse"
                ),
                rx.el.div(
                    class_name="w-full h-32 bg-gray-100 rounded-xl animate-pulse"
                ),
                rx.el.div(
                    class_name="w-full h-32 bg-gray-100 rounded-xl animate-pulse"
                ),
                class_name="col-span-1 lg:col-span-9 space-y-6",
            ),
            rx.el.div(
                rx.el.div(class_name="w-full h-8 bg-gray-200 rounded animate-pulse"),
                rx.el.div(class_name="w-full h-4 bg-gray-200 rounded animate-pulse"),
                rx.el.div(class_name="w-full h-4 bg-gray-200 rounded animate-pulse"),
                rx.el.div(class_name="w-full h-4 bg-gray-200 rounded animate-pulse"),
                class_name="hidden lg:block lg:col-span-3 space-y-4",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-12 gap-8",
        ),
        class_name="max-w-6xl mx-auto pt-8",
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
                    class_name="px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors font-medium text-sm shadow-sm hover:shadow-md",
                ),
                class_name="flex flex-col items-center justify-center py-32 bg-white rounded-2xl border border-gray-100 shadow-sm mx-auto max-w-2xl mt-12",
            ),
        ),
    )