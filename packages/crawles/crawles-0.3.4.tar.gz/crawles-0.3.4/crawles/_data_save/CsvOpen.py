import csv


class CsvOpen:
    """csv文件存储"""

    def __init__(self, filename, mode='r', encoding='gbk', newline=''):
        self._filename = filename
        self._mode = mode
        self._encoding = encoding
        self._newline = newline
        self.head_writer = True

        self._csv_file = open(self._filename, self._mode, encoding=self._encoding, newline=self._newline)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._csv_file:
            self._csv_file.close()

    def head(self, head_list):
        """写入头数据，只运行一次"""
        if self.head_writer is True:
            if not isinstance(head_list, list):
                raise TypeError('head_list must be a list')
            self.writer(head_list)
            self.head_writer = False

    def writer(self, data):
        writer = csv.writer(self._csv_file)
        writer.writerow(data)

    def writerow(self, list_data):
        """写入一行数据"""
        if isinstance(list_data, list):
            self.writer(list_data)

        elif isinstance(list_data, dict):
            self.head([k for k, v in list_data.items()])
            self.writer([v for k, v in list_data.items()])

        else:
            raise TypeError('list_data must be a list/dict')

    def writerows(self, list_data):
        """一次写入多行数据"""
        if not isinstance(list_data, list) and not list_data:
            raise TypeError('list_data must be a list of lists')

        if isinstance(list_data[0], list):
            writer = csv.writer(self._csv_file)
            writer.writerows(list_data)

        if isinstance(list_data[0], dict):
            for row in list_data:
                self.writer([v for k, v in row.items()])


if __name__ == '__main__':
    pass

    # csv_obj = CsvOpen('data.csv', mode='w+')
    # csv_obj.head(['1', '2', '3', '4'])
    # csv_obj.writerow(['a', 'b', 'c', 'd'])
    # csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
    # csv_obj.writerow({'name':'小明','age':21})
    # csv_obj.writerows([{'name':'小明','age':22}, {'name':'小明','age':23}])
    # csv_obj.close()

    # with CsvOpen('data.csv', mode='w+') as csv_obj:
    #     csv_obj.head(['1', '2', '3', '4'])
    #     csv_obj.writerow(['a', 'b', 'c', 'd'])
    #     csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
    #     csv_obj.writerow({'name': '小明', 'age': 21})
    #     csv_obj.writerows([{'name': '小明', 'age': 22}, {'name': '小明', 'age': 23}])
