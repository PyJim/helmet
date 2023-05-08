from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

# Placeholder data for reported disasters
disasters = [
    {
        'id': 1,
        'type': 'Earthquake',
        'location': 'Example City',
        'intensity': 'High',
        'description': 'Lorem ipsum dolor sit amet...',
        'media': [],
        'latitude': 37.7749,
        'longitude': -122.4194
    },
    {
        'id': 2,
        'type': 'Flood',
        'location': 'Another City',
        'intensity': 'Medium',
        'description': 'Lorem ipsum dolor sit amet...',
        'media': [],
        'latitude': 40.7128,
        'longitude': -74.0060
    }
]

@app.route('/')
def index():
    return render_template('index.html', disasters=disasters)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Process the form data and add a new disaster report to the list
        disaster = {
            'id': len(disasters) + 1,
            'type': request.form['type'],
            'location': request.form['location'],
            'intensity': request.form['intensity'],
            'description': request.form['description'],
            'media': [],
            'latitude': 0,  # Set default latitude value
            'longitude': 0  # Set default longitude value
        }
        disasters.append(disaster)
        return render_template('report_success.html', disaster=disaster)
    else:
        return render_template('report.html')

@app.route('/disaster/<int:disaster_id>')
def view_disaster(disaster_id):
    # Find the disaster with the given ID
    disaster = next((d for d in disasters if d['id'] == disaster_id), None)
    if disaster:
        return render_template('disaster.html', disaster=disaster)
    else:
        return render_template('disaster_not_found.html')

# Route for the interactive map
@app.route('/map')
def view_map():
    return render_template('map.html', disasters=disasters)

# Route for disaster updates
@app.route('/disaster/<int:disaster_id>/update', methods=['GET', 'POST'])
def update_disaster(disaster_id):
    disaster = next((d for d in disasters if d['id'] == disaster_id), None)
    if request.method == 'POST':
        # Process the form data and update the disaster information
        disaster['intensity'] = request.form['intensity']
        # Add logic to update other fields as needed
        return render_template('disaster.html', disaster=disaster)
    else:
        return render_template('update_disaster.html', disaster=disaster)

# Route for search feature
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].lower()
    filtered_disasters = [d for d in disasters if query in d['type'].lower() or query in d['location'].lower()]
    return render_template('search_results.html', query=query, disasters=filtered_disasters)

# Add routes and functions for notifications, filter, etc.



if __name__ == '__main__':
    app.run(debug=True)
