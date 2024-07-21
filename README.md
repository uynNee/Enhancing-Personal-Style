# Enhancing Personal Style: Clothing Recommendation System

## Overview
The Enhancing Personal Style is a web-based application designed to provide personalized clothing recommendations to users. It leverages various algorithms, including content-based and collaborative filtering, to suggest items that match users' preferences in terms of body shape, skin tone, and personal style.

## Features
- **User Authentication**: Secure login and registration functionality to manage user sessions.
- **Body Shape Prediction**: Utilizes user-provided measurements to predict the user's body shape using a pre-trained model.
- **Personalized Recommendations**: Offers clothing recommendations based on the user's body shape, skin tone, and gender.
- **Like System**: Users can like products, which influences future recommendations through collaborative filtering.
- **Search Functionality**: Integrated search feature to find products on external platforms like Amazon.

## Technologies Used
- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 for storing user data and preferences
- **Machine Learning**: Scikit-learn for predictive modeling and recommendation algorithms

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/uynNee/Enhancing-Personal-Style.git
   ```
2. Navigate to the project directory:
   ```
   cd Enhancing-Personal-Style\my_project\Enhancing Personal Style\
   ```
3. Initialize the database:
   ```
   python init_db.py
   ```
4. Run the application:
   ```
   python app.py
   ```
   The application will be accessible at `http://localhost:5000`.

## Usage
- **Register**: Create a new account using the registration form.
- **Login**: Access the system by logging in with your credentials.
- **Set Preferences**: Update your profile with body measurements, skin tone, and gender for personalized recommendations.
- **Explore Recommendations**: Browse through the recommended clothing items tailored to your profile.
- **Like Items**: Like items to refine future recommendations.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
