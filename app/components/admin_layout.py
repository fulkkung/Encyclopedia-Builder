import reflex as rx
from app.states.auth_state import AuthState


def admin_sidebar_item(
    icon: str, label: str, href: str, is_active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon, size=18, class_name=rx.cond(is_active, "text-white", "text-gray-400")
        ),
        rx.el.span(label, class_name="font-medium text-sm"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-3 py-2 rounded-md bg-gray-800 text-white transition-colors",
            "flex items-center gap-3 px-3 py-2 rounded-md text-gray-400 hover:bg-gray-800 hover:text-white transition-colors",
        ),
    )


def admin_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.icon("shield", class_name="text-indigo-500", size=24),
            rx.el.span(
                "Admin Panel", class_name="text-lg font-bold text-white tracking-tight"
            ),
            class_name="flex items-center gap-3 px-6 h-16 border-b border-gray-800",
        ),
        rx.el.nav(
            admin_sidebar_item("layout-dashboard", "Dashboard", "/admin"),
            admin_sidebar_item("book-open", "Books", "/admin/books"),
            class_name="flex flex-col gap-1 p-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("log-out", size=18),
                "Logout",
                on_click=AuthState.logout,
                class_name="flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors w-full px-4 py-2",
            ),
            class_name="mt-auto p-4 border-t border-gray-800",
        ),
        class_name="flex flex-col w-64 bg-gray-900 h-screen sticky top-0 text-gray-300",
    )


def admin_layout(content: rx.Component) -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.div(
            admin_sidebar(),
            rx.el.main(
                content, class_name="flex-1 bg-gray-50 min-h-screen overflow-y-auto"
            ),
            class_name="flex min-h-screen w-full font-['Inter']",
        ),
        rx.el.div(
            rx.spinner(),
            class_name="flex items-center justify-center h-screen w-screen",
        ),
    )