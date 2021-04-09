from flask import Flask, jsonify, abort, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from redis_wrapper import RedisClient

app = Flask(__name__)
redis_client = RedisClient()
CORS(app)

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Flask-REST-Redis"
    }
)
app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/api/keys', methods=['GET', 'HEAD'])
def get_a_value():
    """
    Endpoint for checking value is exist or desired value for given key
    """
    key = request.args.get('key')

    if key is None:
        return jsonify({"error": "need a key paramater"}), 403
    if key == "":
        return jsonify({"error": "no empty key"}), 403
    try:
        if redis_client.exists(key):
            if request.method == "HEAD":
                return ''
            else:
                key_value = {
                    'key': key,
                    'value': redis_client.get(key)
                }

                return jsonify(key_value)
        else:
            abort(404)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 403

@app.route('/api/keys/', methods=['GET'])
def get_all_values():
    """
    Endpoint for listing all key value pairs
    """
    return jsonify(redis_client.get_all())


@app.route('/api/keys/', methods=['PUT'])
def set_a_value():
    """
    Endpoint for adding a new key value pair
    """
    if not request.json or 'key' not in request.json or 'value' not in request.json:
        abort(400)

    key = request.json['key']
    value = request.json['value']

    if len(key) == 0 or len(value) == 0:
        abort(400)

    key_value = {
        'key': key,
        'value': value
    }

    redis_client.set(key, value)

    return jsonify(key_value), 201


@app.route('/api/keys', methods=['DELETE'])
def delete_a_value(key):
    """
    Endpoint for deleting given key value pair
    """
    key = request.args.get('key')

    if key is None:
        return jsonify({"err": "need a key paramater"}), 403
    if key == "":
        return jsonify({"err": "no empty key"}), 403
    try:
        if redis_client.exists(key):
            redis_client.delete(key)
            return 'OK', 204
        else:
            abort(404)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 403


@app.route('/api/keys/', methods=['DELETE'])
def delete_all_values():
    """
    Endpoint for deleting all key value pairs in current db
    """
    redis_client.flush_db()
    return 'OK', 204


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
