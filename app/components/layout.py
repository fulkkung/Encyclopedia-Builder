import reflex as rx


def sidebar_item(
    icon: str, label: str, href: str = "#", is_active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=rx.cond(is_active, "text-indigo-600", "text-gray-400"),
            size=20,
        ),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-3 py-2 rounded-lg bg-indigo-50 text-indigo-700 transition-colors",
            "flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.icon("library", class_name="text-indigo-600", size=28),
            rx.el.span(
                "Encyclopedia",
                class_name="text-xl font-bold text-gray-900 tracking-tight",
            ),
            class_name="flex items-center gap-3 px-6 h-16 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Discover",
                    class_name="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2",
                ),
                rx.el.nav(
                    sidebar_item("layout-grid", "Browse", "/"),
                    sidebar_item("sparkles", "New Arrivals"),
                    sidebar_item("bookmark", "Reading List"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.p(
                    "Library",
                    class_name="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2",
                ),
                rx.el.nav(
                    sidebar_item("book-open", "Books", "/", is_active=True),
                    sidebar_item("users", "Authors"),
                    sidebar_item("tag", "Categories"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            class_name="flex-1 overflow-y-auto py-6 px-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/avataaars/svg?seed=Felix",
                    class_name="size-8 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.p(
                        "Alex Reader", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p("Premium Member", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="p-4 border-t border-gray-100",
        ),
        class_name="hidden lg:flex flex-col w-64 border-r border-gray-200 bg-white h-screen sticky top-0 shrink-0 z-20",
    )


from app.states.book_state import BookState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    size=18,
                ),
                rx.el.input(
                    type="text",
                    placeholder="Search books, authors, content... (Cmd+K)",
                    on_change=BookState.set_search_query,
                    class_name="w-full pl-10 pr-4 py-2 bg-gray-50 border-transparent focus:bg-white focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 rounded-lg text-sm transition-all outline-none placeholder:text-gray-400",
                    default_value=BookState.search_query,
                ),
                class_name="relative w-full max-w-md",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", size=20),
                    class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors",
                ),
                rx.el.button(
                    rx.icon("circle_plus", size=20),
                    class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between h-16 px-8 border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0 z-10",
        )
    )


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(content, class_name="flex-1 p-8 overflow-x-hidden"),
            class_name="flex-1 flex flex-col min-w-0 min-h-screen bg-white",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-white",
    )