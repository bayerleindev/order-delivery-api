ERROR_MESSAGES = {
    "USER_EXISTS": {
        "pt": {
            "code": "1",
            "message": "E-mail ou usuário já cadastrado.",
            "details": "E-mail ou usuário já cadastrado.",
        }
    },
    "ORDER_NOT_FOUND": {
        "pt": {
            "code": "2",
            "message": "Pedido '{}' não encontrado.",
            "details": "Pedido '{}' não encontrado.",
        }
    },
    "STATUS_NOT_ALLOWED": {
        "pt": {
            "code": "3",
            "message": "Status '{}' não permitido.",
            "details": "Status '{}' não permitido.",
        }
    },
}


def get_error(key: str, *args):
    error = ERROR_MESSAGES.get(key)["pt"]
    if args:
        error["message"] = error["message"].format(*args)
        error["details"] = error["details"].format(*args)
    return error
