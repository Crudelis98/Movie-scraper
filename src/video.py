from dataclasses import dataclass, field
import re


@dataclass
class Video:
    title: str
    year: str
    id: str
    imgUrl: str
    avDate: str
    dir_name: str = field(init=False)
    seasons: list

    def __post_init__(self):
        self.dir_name = re.sub(r'[\/:*?"><|]+', "", self.title) + " ({})".format(self.year)
