from manim import Scene
from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def get_data(self, time: int):
        pass

    @abstractmethod
    def push_data(self, data, time: int):
        pass


class DataScene(Scene):
    provider: Provider

    def __init__(self, **kwargs):
        if not hasattr(self, 'provider') or not self.provider:
            raise Exception(f'''Provider not set. You must set {
                            self.__class__.__name__}.provider to a Provider instance.''')
        super().__init__(**kwargs)
        self.push_data(0)
        self.data = self.provider.get_data(0)

    def update_to_time(self, t: float):
        if self.provider:
            self.push_data(int(self.renderer.time * self.camera.frame_rate))
            self.data = self.provider.get_data(
                int(self.renderer.time * self.camera.frame_rate))
        super().update_to_time(t)

    def push_data(self, time: int):
        pass
