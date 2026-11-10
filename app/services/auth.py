from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from app import db
from app.models import Usuario
hasher = PasswordHasher()
def criar_usuario(nome, senha):
    if not nome or len(nome.strip()) < 3: raise ValueError("Usuário deve ter ao menos 3 caracteres.")
    if not senha or len(senha) < 10: raise ValueError("Senha deve ter ao menos 10 caracteres.")
    user = Usuario(nome_acesso=nome.strip(), hash_senha=hasher.hash(senha))
    db.session.add(user); db.session.commit()
    return user
def verificar_senha(user, senha):
    try: return hasher.verify(user.hash_senha, senha)
    except (VerifyMismatchError, InvalidHashError): return False
