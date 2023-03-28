from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        # Aquí puedes validar si el usuario está autenticado en tu sistema de autenticación.
        return True

    def is_active(self):
        # Aquí puedes validar si el usuario está activo en tu sistema.
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # Aquí puedes retornar el ID del usuario, por ejemplo su username o su ID en la base de datos.
        return self.username
