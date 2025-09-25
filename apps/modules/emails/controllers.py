from .rabbitmq import RabbitMQHandler
from .exception import ErrorCode

class EmailController:
    def __init__(self):
        self.rabbitmq = RabbitMQHandler()

    async def send_producer(self, email: str, fullname: str, data: dict, mail_type: str):
        try:
            payload = {
                "email": email, "fullname": fullname, 
                "data": data, "mail_type": mail_type
            }
            await self.rabbitmq.producer(payload)
        except Exception:
            raise ErrorCode.InvalidEmailData()
