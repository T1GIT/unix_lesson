from flask import jsonify, make_response, abort, request
from flask_login import login_required, current_user

from routes import app


def id_inc():
    _id = 0
    while True:
        yield _id
        _id += 1


task_id_gen = id_inc()


@app.route('/todo', methods=['GET'])
@login_required
def get_tasks():
    return jsonify({
        "tasks": [
            {"id": id, "text": text}
            for id, text in current_user.tasks.items()
        ]
    })


@app.route("/todo", methods=['POST'])
@login_required
def add_task():
    if not request.json:
        abort(400)
    id = next(task_id_gen)
    text = request.json["text"]
    current_user.tasks[id] = text
    return jsonify({"id": id, "text": text})


@app.route("/todo", methods=['PUT'])
@login_required
def update_task():
    if not request.json:
        abort(400)
    id = int(request.args["id"])
    text = request.json["text"]
    if id not in current_user.tasks:
        abort(404)
    current_user.tasks[id] = text
    return jsonify({"id": id, "text": text})


@app.route("/todo", methods=['DELETE'])
@login_required
def delete_task():
    id = int(request.args["id"])
    if id not in current_user.tasks:
        abort(404)
    del current_user.tasks[id]
    return jsonify(True)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify({'error': 'Conflict'}), 409)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
