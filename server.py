from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Chain', 'min_amount': 100},
    {'id': 2, 'name': 'Painting', 'min_amount': 200},
    {'id': 3, 'name': 'Flower Vase', 'min_amount': 150},
    {'id': 4, 'name': 'Gramophone', 'min_amount': 300},
    {'id': 5, 'name': 'Pistol', 'min_amount': 250}
]

total_clients = 0
total_participants = 0
participants = []
max_amounts = {}


@app.route('/')
def index():
    return render_template('index.html', products=products)


@app.route('/setup', methods=['POST'])
def setup_auction():
    global total_clients, total_participants, participants, max_amounts

    total_clients = int(request.form['total_clients'])
    bid_limit = int(request.form['bid_limit'])

    total_participants = 0
    participants = []
    max_amounts = {}

    return jsonify({'message': 'Auction setup successful'})


@app.route('/register', methods=['POST'])
def register_participant():
    global total_participants, participants, max_amounts

    product_id = int(request.form['product_id'])
    min_amount = int(request.form['min_amount'])

    participant_id = total_participants + 1
    participant = {'participant_id': participant_id, 'product_id': product_id, 'min_amount': min_amount}
    participants.append(participant)

    if product_id in max_amounts:
        if min_amount > max_amounts[product_id]:
            max_amounts[product_id] = min_amount
    else:
        max_amounts[product_id] = min_amount

    total_participants += 1

    if total_participants >= total_clients:
        return jsonify({'message': 'Auction completed', 'participants': participants, 'max_amounts': max_amounts})
    else:
        return jsonify({'message': 'Participant registered', 'participant_id': participant_id})


if __name__ == '__main__':
    app.run(debug=True)
