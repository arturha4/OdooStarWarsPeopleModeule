import logging


def set_logger():
    file_name = 'log.txt'
    logging.basicConfig(
        handlers=[logging.FileHandler(filename=file_name,
                                      encoding='utf-8', mode='a')],
        level=logging.INFO,
        format="{asctime} {levelname:} {message}",
        style='{',
    )
    return file_name
