import functools
import textwrap


class Query:
    keywords = [
        'SELECT',
        'FROM',
        'WHERE',
        'GROUP BY',
        'ORDER BY',
        'LIMIT',
        'OFFSET'
    ]

    def __init__(self):
        self.data = {k: [] for k in self.keywords}

    def add(self, keyword, arg: str):
        expression = self.data[keyword]
        expression.append(Query._clean_up(arg))
        return self

    def statement(self) -> str:
        return str(self)

    def __getattr__(self, name):
        if not name.isupper():
            return getattr(super(), name)
        return functools.partial(self.add, name.replace('_', ' '))

    def __str__(self):
        return ''.join(self._lines())

    def _lines(self):
        for keyword, expression in self.data.items():
            if not expression:
                continue

            yield f'{keyword} {expression[0]} '

    @staticmethod
    def _clean_up(thing: str) -> str:
        delete = thing.split(';')[0]
        res = delete.split()
        return textwrap.dedent(" ".join(res))
