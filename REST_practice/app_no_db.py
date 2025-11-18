from flask import Flask, jsonify

app = Flask(__name__)

users_info = [
    {"id": "0", "name":"suzuki"},
    {"id": "1", "name":"sasaki"}
]


@app.route('/users', methods=["GET"])
def get_users():
    return jsonify({"users": users_info})

@app.route('/users/<string:userid>', methods=["GET"])
def get_user(userid):
    return jsonify({"user": users_info[userid]})
    

@app.route('/users/one', methods=["POST"])
def add_user():
    """
    ユーザー情報を一人分追加する API
    """
    data = {"id":"2", "name":"tanaka"}  # 仮データ
    users_info.append(data)
    return jsonify({"users": users_info})

@app.route('/users/multiple', methods=["POST"])
def add_users():
    """
    ユーザー情報を複数追加する API
    """
    add_users_info = [
         {"id":"3", "name":"sato"},
         {"id":"4", "name":"takahashi"},
         {"id":"5", "name":"ito"}
    ]
    users_info.extend(add_users_info)
    return jsonify({"users": users_info})


@app.route('/users/<string:userid>', methods=["DELETE"])
def delete_user(userid):
    """
    ユーザー情報を一つ削除する
    """
    for user in users_info:
          if userid == user["id"]:
               users_info.remove(user)
    return jsonify({"users": users_info})

@app.route('/users', methods=["DELETE"])
def delete_users():
    """
    ユーザー情報をすべて削除する
    """
    users_info.clear()
    return jsonify({"users": users_info})


@app.route('/users/<string:userid>', methods=["PUT"])
def update_user(userid):
    """
    ユーザー情報を一部更新する
    """
    new_data = {"name": "name_updated"}
    for user in users_info:
        if userid == user["id"]:
            user.update(new_data)
    return jsonify({"users": users_info})

if __name__ == "__main__":
    app.run(debug=True)
