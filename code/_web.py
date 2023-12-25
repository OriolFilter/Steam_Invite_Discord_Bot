# Proof of concept
import _web2 as test


class T:
    _x = 0

    @property
    def x(self):
        self._x += 1
        return self._x


t = T()
test.run(t=t)
