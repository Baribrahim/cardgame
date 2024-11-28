# Higher/Lower Card Game

A simple web-based Higher/Lower card game built with Flask.

## Features

- **Higher or Lower Gameplay**: Intuitive guessing mechanic where players predict the next card's value.
- **Best Score Tracking**: Keeps track of the highest score achieved during a browsing session.
- **Progress Bar**: Visually represents the player's progress through the deck of cards.
- **Sound Effects**: Plays distinct sounds for correct and incorrect guesses to provide immediate feedback.
- **Joker Cards (Optional)**: Includes Joker cards for bonus points based on user preference.

## Getting Started

Follow these simple steps to set up and run the application locally.

### Prerequisites

- **Python 3.7 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (comes with Python)
- **Git** (optional): For cloning the repository

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/baribrahim/cardgame.git
   cd cardgame

2. **Create a Virtual Environment (Optional but Recommended)**
  - **On macOS and Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
- **On Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
### Running the Application
1. **Run the Application**
    ```bash
    python app.py
2. **Access the game**
Open your web browser and navigate to http://127.0.0.1:5000/ to start playing.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript

## Design Decisions
- **Flask Framework**: Chosen for its simplicity and flexibility, making it ideal for building a lightweight web application.
- **Session Management**: Utilised Flask sessions to track user scores and game state without the need for a database.
- **Bootstrap Integration**: Implemented Bootstrap for responsive and clean UI design, making sure the game looks good on all devices.
- **Sound Effects**: Added HTML5 Audio for immediate feedback, improving user engagement.
- **Progress Bar Calculation**: Designed the progress bar to show the percentage of the deck used, visualing game progress.

## Future Improvements
- **Persistent Storage**: Implement a database to save Best Scores across sessions and devices.
- **User Authentication**: Allow users to create accounts and track their scores over time.
- **Leaderboard**: Introduce a global leaderboard to encourage competition among players.
- **Improved UI/UX**: Incorporate more animations and visual effects to make the game more interactive and engaging.
- **Mobile Optimisation**: Further optimise the game for mobile devices to ensure good user experience on all devices.
