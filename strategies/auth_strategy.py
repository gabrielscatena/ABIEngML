# strategies/auth_strategy.py

from abc import ABC, abstractmethod


class AuthStrategy(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str):
        pass

    @abstractmethod
    def login(self, user):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def get_current_user(self):
        pass

    @abstractmethod
    def admin_required(self, f):
        pass

