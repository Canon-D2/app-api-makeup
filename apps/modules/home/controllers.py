from .services import HomeService

class HomeController:
    def __init__(self):
        self.home_service = HomeService()
