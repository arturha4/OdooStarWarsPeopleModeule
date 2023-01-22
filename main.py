import config
import os
import logger
from argparser import get_path_arg
from server.odoo_api_manager import OdooApiManager
from server.requester import ImageRequester, StarWarsRequester, StarWarsPlanetRequester


def create_odoo_multiple_objects(app):
    planets = StarWarsPlanetRequester(config.star_wars_planets_url).get_all_objects()
    for item in planets:
        odoo_id = app.create_odoo_object('res.planet', {'name': item['name'],
                                                        'diameter': item['diameter'],
                                                        'rotation_period': item['rotation_period'],
                                                        'orbital_period': item['orbital_period'],
                                                        'population': item['population']}, item['planet_url_pk'])
        item['odoo_id'] = odoo_id
    planets = StarWarsPlanetRequester.get_objects_with_url_pk(planets)
    people = StarWarsRequester(config.star_wars_people_url).get_all_objects()
    for person in people:
        app.create_odoo_object('res.partner', {'name': person['name'],
                                               'image_1920': ImageRequester(config.star_wars_people_image_url,
                                                                            person['image_pk']).encoded_image,
                                               'planet': planets[person['planet_url_pk']]['odoo_id']},
                               person['image_pk'])



if __name__ == "__main__":
    cfg_path = get_path_arg()
    print('starting...')
    log_name = logger.set_logger()
    if not os.path.exists(log_name):
        f = open(log_name, "w")
    print('start creation')
    create_odoo_multiple_objects(
        OdooApiManager(config.db, config.odoo_admin_username, config.odoo_admin_password, config.url))
    print('creation complete')
