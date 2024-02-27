def format_file_name(file_name: str) -> str:
    """
    将传入文件打包成一个压缩包（minio上传文件文件名有长度限制，官方文档中没写，经测试最长70个中文字符）
    @param file_name:
    @return:
    """
    split_list = file_name.split(".")
    split_len = len(split_list)
    if split_len > 1:
        name = "".join(split_list[0 : split_len - 1])
        extension = split_list[split_len - 1]
        name_max_len = 70 - len(extension)
        finally_name = name
        if len(name) > name_max_len:
            finally_name = name[0:name_max_len]
        file_name = f"{finally_name}.{extension}"

    return file_name


def handle_file_name(name: str) -> str:
    """
    处理文件名中特殊字符
    :param name:
    :return:
    """
    special_str_list = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", " ", "\n", "\r"]
    for special_str in special_str_list:
        name = name.replace(special_str, "")
    return format_file_name(name)
