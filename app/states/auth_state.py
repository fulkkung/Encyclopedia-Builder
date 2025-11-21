import reflex as rx


class AuthState(rx.State):
    is_authenticated: bool = False
    username: str = ""
    password: str = ""
    error_message: str = ""

    @rx.event
    def login(self):
        if self.username == "admin" and self.password == "admin":
            self.is_authenticated = True
            self.error_message = ""
            return rx.redirect("/admin")
        else:
            self.error_message = "Invalid credentials. Try admin/admin"

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")