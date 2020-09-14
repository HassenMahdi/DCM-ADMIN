from ...db.Models.user import User


class Auth:

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                user = User().load({'_id':resp})
                # TODO CHANGE THIS
                response_object = {
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'email': user.email,
                        'last_name': user.last_name,
                        'first_name': user.first_name,
                        'admin': user.admin,
                        'created_on': str(user.created_on),
                        'roles': user.roles
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def get_logged_in_user_rights(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                user = User().load({'_id': resp})
                response_object = {
                    'admin': user.admin,
                    'domain_ids': [domain_access['domain_id'] for domain_access in (user.roles or [])]
                }
                # TODO CHANGE THIS
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
