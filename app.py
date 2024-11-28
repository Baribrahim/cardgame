# app.py

from flask import Flask, render_template, session, redirect, url_for, request, flash
from deck import Deck
from card import Card
import random

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'  # Replace with a secure secret key

def parse_card_string(card_str):
    """
    Parses a card string and returns a tuple of (rank, suit).
    For Jokers, suit is 'Joker' and rank is the card name.
    """
    if 'Joker' in card_str:
        return card_str, 'Joker'  # rank, suit
    else:
        rank, _, suit = card_str.partition(' of ')
        return rank.strip(), suit.strip()

def parse_card_string_to_card(card_str):
    """
    Converts a card string back to a Card object.
    """
    if 'Joker' in card_str:
        return Card('Joker', card_str)
    else:
        rank, _, suit = card_str.partition(' of ')
        return Card(suit.strip(), rank.strip())

def reconstruct_deck(deck_cards_str_list):
    """
    Reconstructs the Deck object from a list of card strings.
    """
    deck = Deck(include_jokers=False)  # We'll set the cards manually
    deck.cards = []
    for card_str in deck_cards_str_list:
        if 'Joker' in card_str:
            # Handle Joker cards
            card = Card('Joker', card_str)
        else:
            # Parse the card string
            rank, _, suit = card_str.partition(' of ')
            card = Card(suit.strip(), rank.strip())
        deck.cards.append(card)
    return deck

def get_card_value(rank):
    """
    Assigns a numerical value to each card rank for comparison.
    """
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'jack': 11, 'queen': 12, 'king': 13, 'ace': 14,
        'Black Joker': 15,
        'Red Joker': 15
    }
    return rank_values.get(rank, 0)

def compare_cards(current_card_str, next_card_str, guess):
    """
    Compares the current card with the next card based on the player's guess.
    Returns True for correct guess, False for incorrect, 'tie' for equal ranks, 'joker' for Joker cards.
    """
    current_rank, current_suit = parse_card_string(current_card_str)
    next_rank, next_suit = parse_card_string(next_card_str)

    # Debugging Statements
    print(f"Current Card: {current_rank} of {current_suit}")
    print(f"Next Card: {next_rank} of {next_suit}")
    print(f"Player's Guess: {guess}")

    # Check if the next card is a Joker
    if 'Joker' in next_rank:
        session['score'] += 1  # Bonus point
        flash('A Joker appeared! You get a bonus point!', 'success')
        return 'joker'

    current_value = get_card_value(current_rank)
    next_value = get_card_value(next_rank)

    print(f"Current Card Value: {current_value}")
    print(f"Next Card Value: {next_value}")

    if next_value == current_value:
        # Neutral outcome
        return 'tie'
    elif guess == 'higher' and next_value > current_value:
        return True
    elif guess == 'lower' and next_value < current_value:
        return True
    else:
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    # Clear any existing session data to reset the game
    session.clear()

    # Get the user's choice from the form
    include_jokers_choice = request.form.get('include_jokers')
    if include_jokers_choice not in ['yes', 'no']:
        flash('Invalid selection for Jokers. Please try again.', 'danger')
        return redirect(url_for('home'))
    include_jokers = include_jokers_choice == 'yes'

    # Store the choice in the session
    session['include_jokers'] = include_jokers

    # Initialize a new deck based on the user's choice
    deck = Deck(include_jokers=include_jokers)
    deck.shuffle()

    # Store the deck and current card in the session
    session['deck'] = [str(card) for card in deck.cards]
    session['current_card'] = str(deck.deal_one())
    session['score'] = 0
    session['total_cards'] = len(deck.cards) + 1  # +1 for the dealt card

    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'current_card' not in session:
        return redirect(url_for('home'))

    current_card = session['current_card']
    score = session.get('score', 0)
    total_cards = session.get('total_cards', 52)
    remaining_cards = len(session['deck'])
    progress = ((total_cards - remaining_cards - 1) / total_cards) * 100  # -1 because one card is already dealt
    progress = max(0, min(progress, 100))  # Clamp the value between 0 and 100


    # Prepare image filename
    current_card_image = current_card.replace(' ', '_') + '.png'

    return render_template(
        'game.html',
        current_card=current_card,
        current_card_image=current_card_image,
        score=score,
        progress=progress
    )

@app.route('/guess', methods=['POST'])
def guess():
    if 'current_card' not in session or 'deck' not in session:
        flash('Game session not found. Please start a new game.', 'danger')
        return redirect(url_for('home'))

    guess = request.form.get('guess')  # 'higher' or 'lower'

    if guess not in ['higher', 'lower']:
        flash('Invalid guess. Please choose "Higher" or "Lower".', 'danger')
        return redirect(url_for('game'))

    # Reconstruct the deck from the session
    deck_cards = session['deck']
    deck = reconstruct_deck(deck_cards)

    current_card_str = session['current_card']
    next_card = deck.deal_one()

    if next_card is None:
        # No more cards in the deck
        flash('No more cards in the deck. Game over!', 'info')
        return redirect(url_for('game_over'))

    next_card_str = str(next_card)
    # Debugging Statements
    print(f"Current Card: {current_card_str}")
    print(f"Next Card: {next_card_str}")
    print(f"Player's Guess: {guess}")
    # Compare cards
    result = compare_cards(current_card_str, next_card_str, guess)

    if result == True:
        session['score'] += 1
        flash('Correct! You gain a point.', 'success')
    elif result == False:
        flash('Incorrect! Game over.', 'danger')
        return redirect(url_for('game_over'))
    elif result == 'tie':
        flash('It\'s a tie! No points awarded.', 'info')
    elif result == 'joker':
        # Bonus point already added in compare_cards
        pass

    # Update session variables
    session['deck'] = [str(card) for card in deck.cards]
    session['current_card'] = next_card_str

    return redirect(url_for('game'))

@app.route('/game_over')
def game_over():
    score = session.get('score', 0)
    include_jokers = session.get('include_jokers', False)
    return render_template('game_over.html', score=score, include_jokers=include_jokers)

if __name__ == '__main__':
    app.run(debug=True)
