from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# ✅ Replace with your actual Atlas URI:
app.config["MONGO_URI"] = "mongodb+srv://marioqm_db_user:n5kvbICO6RVVAgxV@cluster0.rk1vnwg.mongodb.net/todo_db?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task = {
            'content': task_content,
            'completed': 0,
            'date_created': datetime.utcnow()
        }
        try:
            mongo.db.todos.insert_one(task)
            return redirect('/')
        except Exception as e:
            print("Error inserting:", e)
            return "Problem inserting value."
    else:
        tasks = mongo.db.todos.find().sort('date_created', 1)
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    try:
        mongo.db.todos.delete_one({'_id': ObjectId(id)})
        return redirect('/')
    except Exception as e:
        print("Error deleting:", e)
        return 'There was a problem deleting the task'

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    task = mongo.db.todos.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        new_content = request.form['content']
        try:
            mongo.db.todos.update_one(
                {'_id': ObjectId(id)},
                {'$set': {'content': new_content}}
            )
            return redirect('/')
        except Exception as e:
            print("Error updating:", e)
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
