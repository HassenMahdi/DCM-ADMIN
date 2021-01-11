import uuid
import datetime
from copy import copy

import xlrd

from app.datacheck.default.empty import EmptyCheck
from app.datacheck.default.ref import ReferenceCheck
from app.db.Models.connectors.connector import Connector
from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.flow_context import FlowContext
from app.db.Models.mapping import Mapping
from app.main.util.strings import camelCase


def save_connector(data):
    cn_id = data.get('id', None)

    cn = Connector()
    cn.id = cn_id

    original_cn = Connector().load(query={"_id": cn_id})
    if not original_cn.id:
        identifier = uuid.uuid4().hex.upper()
        cn = Connector(
            **{
                'id': identifier,
                'created_on': datetime.datetime.utcnow()
            })

    cn.name = data['name']
    cn.type = data['type']
    cn.password = data.get('password', None)
    cn.database = data.get('database', None)
    cn.user = data.get('user', None)
    cn.auth_with = data.get('auth_with', None)
    cn.sas_token = data.get('sas_token', None)
    cn.shared_access_key = data.get('shared_access_key', None)
    cn.url = data.get('url', None)
    cn.description = data.get('description', None)
    cn.port = int(data.get('port', 0))
    cn.conn_string = data.get('conn_string', None)
    cn.modified_on = datetime.datetime.utcnow()

    cn.save()

    return {"status":"success", "message":"Connector Saved"}, 200


def delete_connector(cn_id):
    cn = Connector().load(query={"_id":cn_id})

    if cn.id:
        cn.delete()
        return {"status":"success", "message": "Connector deleted."}, 200
    else:
        return {"status": "success", "message": "No Connector found."}, 404


def get_all_connectors():
    return Connector.get_all()


def test_connector(data=None, connector_id=None):
    pass
