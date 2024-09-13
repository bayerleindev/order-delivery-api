from consumer.model import ConsumerModel


class Input:
    document: str
    name: str
    email: str
    phone: str

    def __init__(self, document: str, name: str, email: str, phone: str) -> None:
        self.document = document
        self.name = name
        self.email = email
        self.phone = phone


class CreateUser:
    def execute(self, input: Input):
        consumer = ConsumerModel(
            document=input.document,
            name=input.name,
            email=input.email,
            phone=input.phone,
        )
        print(consumer.to_json())
