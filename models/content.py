from dataclasses import dataclass


@dataclass
class Content:
    title: str
    description: str = ""

    def get(self):
        return self.title + "\n" + self.description

    @property
    def is_empty(self):
        return self.title == "" and self.description == ""