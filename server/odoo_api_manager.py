import xmlrpc.client
import logging

logging.getLogger(__name__)


class OdooApiManager:
    def __init__(self, db, username, password, url):
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.db = db
        self.username = username
        self.password = password
        uid_auth = self.common.authenticate(db, username, password, {})
        if uid_auth:
            self.uid = uid_auth
            print('Authentication success')
        else:
            print('Authentication failed')
            raise ValueError('Неверные данные')
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    def create_odoo_object(self, model_name: str, fields: dict, api_id):
        try:
            response = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [fields])
            logging.info(
                f"Успешно создано - сущность: {model_name}, имя: {fields['name']}, id в в удаленной системе: {api_id}, id idoo: {response}")
            return response
        except Exception as e:
            logging.info(
                f"Ошибка создания: {e}, cущность: {model_name}, имя: {fields['name']}, id в удаленной системе: {api_id}")

    def create_many_odoo_object(self, model_name: str, fields: list):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [fields])

    def read_odoo_objects(self, model_name: str, objects_id: [], fields: list = None):
        if not fields:
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'read', [objects_id])
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'read', [objects_id], {'fields': fields})

    def get_objects_id(self, model_name: str, obj_filter: [] = None):
        if not obj_filter:
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search', [[]])
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search', [[obj_filter]])
