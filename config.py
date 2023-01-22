import configparser


def get_configparser(path_to_conf: str):
    cfg = configparser.ConfigParser()
    cfg.read(path_to_conf)
    return cfg


settings = get_configparser('config.ini')

odoo_api_key = settings['XML-RPC']['odoo_api_key']
url = settings['XML-RPC']['url']
db = settings['XML-RPC']['db']
odoo_admin_username = settings['XML-RPC']['odoo_admin_username']
odoo_admin_password = settings['XML-RPC']['odoo_admin_password']
star_wars_people_image_url = settings['URLS']['star_wars_people_image_url']
star_wars_people_url = settings['URLS']['star_wars_people_url']
star_wars_planets_url = settings['URLS']['star_wars_planets_url']
