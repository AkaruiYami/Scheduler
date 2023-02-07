from tkinter import W


class Table:
    def __init__(self, headers=None):
        if headers is None:
            headers = []

        self.__headers = headers
        self.__dict__.update([header, []] for header in self.__headers)

    def add_header(self, header, values=None):
        if values is None:
            values = []
        self.__headers.append(header)
        self.__dict__[header] = values

    def add_headers(self, headers, values=None):
        already_exist = set(headers).intersection(self.__headers)
        if already_exist:
            raise ValueError(f"Header: {already_exist} already exist.")

        mx_val_len = len(headers)
        if values is None:
            values = [[]] * mx_val_len

        val_len = len(values)
        if val_len > mx_val_len:
            raise ValueError("Number of values must not exceed the number of headers.")
        elif val_len < mx_val_len:
            d = mx_val_len - val_len
            values.extend([[]] * d)

        for h, v in zip(headers, values):
            self.add_header(h, v)

    def add_data(self, key, value):
        assert key in self.__headers, "Key does not exist in headers"
        self.__dict__[key].append(value)

    def extend(self, keys, values):
        if isinstance(keys, str):
            keys = [keys]
        if len(keys) - len(values) != 0:
            raise ValueError("Keys and values must be the same length.")
        for key, value in zip(keys, values):
            self.__dict__[key].extend(value)
        d = set(self.__headers).difference(keys)
        self._insert_default(d)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        return self.__headers

    def items(self):
        return {header: self.__dict__[header] for header in self.__headers}

    def values(self):
        return [self.__dict__[header] for header in self.__headers]

    def t_values(self):
        v = self.values()
        return list(map(list, zip(*v)))

    def _insert_default(self, keys):
        mx_row = len(max(self.values(), key=len))
        for key in keys:
            to_add = mx_row - len(self.__dict__[key])
            self.__dict__[key].extend(["" for _ in range(to_add)])

    def __iter__(self):
        return self.items()

    def __contains__(self, key):
        return key in self.items()

    def __setitem__(self, key, value):
        if key not in self.__headers:
            raise KeyError("Key does not exist in headers")
        self.__dict__[key] = value

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.__dict__[key[0]][key[1]]
        return self.__dict__[key]

    def __str__(self):
        return f"Table({dict(self.items())})"


if __name__ == "__main__":
    a = Table(["A", "B", "C", "D", "E", "F"])
    a.add_data("A", 12)
    a.add_data("A", 25)
    a.extend(["B", "C"], [[1, 2], [3, 4]])
    a.extend(["B", "C"], [[12, 23], [34, 45]])
    print(a.items())
    print(a["B", 2])
