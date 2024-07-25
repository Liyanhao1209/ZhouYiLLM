from abc import abstractmethod


class abRule:
    @abstractmethod
    def split(self, file_path: str) -> list:
        pass

    @abstractmethod
    def save(self, target_path: str, articles: list):
        pass
