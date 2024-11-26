# app.py

from flask import Flask, render_template, session, redirect, url_for, request
from deck import Deck
from card import Card
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    # Initialize a new deck
    deck = Deck()
    deck.shuffle()

    # Store the deck and current card in the session
    session['deck'] = [str(card) for card in deck.cards]  # Store card representations
    session['current_card'] = str(deck.deal_one())
    session['score'] = 0

    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'current_card' not in session:
        return redirect(url_for('start_game'))

    current_card = session['current_card']
    score = session.get('score', 0)

    return render_template('game.html', current_card=current_card, score=score)

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess']  # 'higher' or 'lower'

    # Reconstruct the deck from the session
    deck_cards = session['deck']
    deck = Deck()
    deck.cards = [Card(suit, rank) for suit, rank in (card.split(' of ') for card in deck_cards)]

    current_card = session['current_card']
    next_card = deck.deal_one()

    if next_card is None:
        # No more cards in the deck
        return redirect(url_for('game_over'))

    # Compare cards
    result = compare_cards(current_card, next_card, guess)
    if result:
        session['score'] += 1
    else:
        return redirect(url_for('game_over'))

    # Update session variables
    session['deck'] = [str(card) for card in deck.cards]
    session['current_card'] = str(next_card)

    return redirect(url_for('game'))

@app.route('/game_over')
def game_over():
    score = session.get('score', 0)
    return render_template('game_over.html', score=score)

def compare_cards(current_card_str, next_card_str, guess):
    # Convert card strings back to Card objects
    current_suit, current_rank = current_card_str.split(' of ')
    next_suit, next_rank = next_card_str.split(' of ')

    current_value = get_card_value(current_rank)
    next_value = get_card_value(next_rank)

    if next_value == current_value:
        # Neutral outcome
        return 'tie'
    elif guess == 'higher' and next_value > current_value:
        return True
    elif guess == 'lower' and next_value < current_value:
        return True
    else:
        return False

def get_card_value(rank):
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
    }
    return rank_values.get(rank, 0)

if __name__ == '__main__':
    app.run(debug=True)
