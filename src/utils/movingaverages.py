from dataclasses import dataclass, field, fields
from collections import deque


@dataclass
class MovingAverages:
    period: int = 30
    p: deque = field(init=False)
    v: deque = field(init=False)

    def __post_init__(self):
        if self.period > 0:
            self.p = deque(maxlen=self.period)
            self.v = deque(maxlen=self.period)
        else:
            self.p = deque()
            self.v = deque()

    @property
    def ma_price(self) -> float:
        return sum(self.p) / len(self.p) if self.p else 0.0

    @property
    def ma_vol(self) -> float:
        return sum(self.v) / len(self.v) if self.v else 0.0

    def reset(self):
        for f in fields(self):
            if f.name not in ('period', 'p', 'v'):
                setattr(self, f.name, 0.0)

    def update(self, p: float, v: float):
        self.p.append(p)
        self.v.append(v)


if __name__ == '__main__':
    ma = MovingAverages(period=30)
    print(ma)
