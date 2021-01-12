import uuid
import datetime
from app.db.Models.connectors.connector import Connector


def save_connector(data):
    cn_id = data.get('id', None)

    cn = Connector(**data)

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


def get_all_connectors(type=None, projection=["_id", "name", "type", "created_on", "modified_on", "description"]):
    query = {}
    if type:
        query.setdefault("type", type)
    return Connector.get_all(query=query ,projection=projection)


def get_connector(cn_id):
    return Connector().load(query={"_id": cn_id})


def test_connector(data=None, connector_id=None):
    pass
