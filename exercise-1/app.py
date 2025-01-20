from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal, URIRef

app = Flask(__name__)

# RDF graph to store social data
social_graph = Graph()

# Define Namespace
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# Sample user data
user_data = {
    "1": ("Luffy", ["2", "3", "4"]),
    "2": ("Zoro", ["1", "4", "3"]),
    "3": ("Nami", ["1", "4", "2"]),
    "4": ("Usopp", ["1", "3", "2"])
}

# Populate RDF graph with sample data
for user_id, (name, friends) in user_data.items():
    user_uri = URIRef(f"http://example.com/users/{user_id}")
    social_graph.add((user_uri, FOAF.name, Literal(name)))
    for friend_id in friends:
        friend_uri = URIRef(f"http://example.com/users/{friend_id}")
        social_graph.add((user_uri, FOAF.knows, friend_uri))

@app.route('/')
def index():
    # Display a list of users
    users = [(str(user), social_graph.value(user, FOAF.name)) for user in social_graph.subjects(predicate=FOAF.name)]
    return render_template('index.html', users=users)

@app.route('/profile/<user_id>')
def profile(user_id):
    try:
        user = URIRef(f"http://example.com/users/{user_id}")
        user_name = social_graph.value(user, FOAF.name)
        friends = [(str(friend), social_graph.value(friend, FOAF.name)) for friend in social_graph.objects(subject=user, predicate=FOAF.knows)]
        return render_template('profile.html', user_name=user_name, friends=friends)
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
