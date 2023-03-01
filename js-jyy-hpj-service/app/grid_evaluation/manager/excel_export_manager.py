import base64


class ExcelExport:

    @staticmethod
    def base64_to_photo(file_data, file_name):
        """
        file_data: base64数据
        file_name: 文件名称
        """
        if file_data:
            b64_data = file_data.split(';base64,')[1]
            data = base64.b64decode(b64_data)
            with open(file_name, "wb") as f:
                f.write(data)


if __name__ == '__main__':
    pass
