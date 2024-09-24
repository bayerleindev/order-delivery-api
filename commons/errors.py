ERROR_MESSAGES = {
    "UNEXPECTED_ERROR": {
        "pt": {
            "code": "0",
            "message": "Erro inesperado.",
            "details": "Erro inesperado.",
        }
    },
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
    "ORDER_WITHOUT_ITEM": {
        "pt": {
            "code": "4",
            "message": "Pedido não tem item adicionado.",
            "details": "Pedido não tem item adicionado.",
        }
    },
    "INVALID_CONSUMER": {
        "pt": {
            "code": "5",
            "message": "Consumidor inválido.",
            "details": "Consumidor inválido.",
        }
    },
    "INVALID_SELLER": {
        "pt": {
            "code": "6",
            "message": "Seller inválido.",
            "details": "Seller inválido.",
        }
    },
    "EMAIL_NOT_VERIFIED": {
        "pt": {
            "code": "7",
            "message": "E-mail não verificado.",
            "details": "E-mail não verificado.",
        }
    },
    "WRONG_VERIFICATION_CODE": {
        "pt": {
            "code": "8",
            "message": "Código de verificação errado.",
            "details": "Código de verificação errado.",
        }
    },
    "DOCUMENT_EXISTS": {
        "pt": {
            "code": "8",
            "message": "Documento já cadastrado.",
            "details": "Documento já cadastrado.",
        }
    },
}


def get_error(key: str, *args):
    error = ERROR_MESSAGES.get(key)["pt"]
    if args:
        error["message"] = error["message"].format(*args)
        error["details"] = error["details"].format(*args)
    return error
