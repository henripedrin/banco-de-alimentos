from repository.user_repository import UserRepository

class AuthService:
    def login(self, username, password):
        userRepository = UserRepository
        if username == None or "":
            return None
        if password == None or "":
            return None
        credentials = userRepository.get_credentials(UserRepository(), username)
        if username == credentials[0] and password == credentials[1]:
            return {"mensagem": "Login efetuado com sucesso!", "usuario": username}
