from flask_restplus import Api
from flask import Blueprint

from .main.controller.dom_controller  import api as doms_ns
from .main.controller.fields_controller  import api as flds_ns
from .main.controller.checks_controller  import api as chks_ns
from .main.controller.super_dom_controller  import api as super_ns
from .main.controller.reference_controller  import api as ref_ns
from .main.controller.connectors_controller  import api as cnn_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='DCM Admin service',
          version='2.0',
          )

api.add_namespace(doms_ns, path='/domain')
api.add_namespace(flds_ns, path='/domain')
api.add_namespace(chks_ns, path='/domain')
api.add_namespace(ref_ns, path='/reference')
api.add_namespace(super_ns, path='/domain/super')
api.add_namespace(cnn_ns, path='/connectors')