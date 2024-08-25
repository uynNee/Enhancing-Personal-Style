# Enhancing Personal Style: Clothing Recommendation System

## Overview
The Enhancing Personal Style is a web-based application designed to provide personalized clothing recommendations to users. It leverages various algorithms, including content-based and collaborative filtering, to suggest items that match users' preferences in terms of body shape, skin tone, and personal style.

## Features
- **User Authentication**: Secure login and registration functionality to manage user sessions.
- **Body Shape Prediction**: Utilizes user-provided measurements to predict the user's body shape using a pre-trained model.

![Demo image 1](https://github.com/uynNee/Enhancing-Personal-Style/blob/d60dfde3b427d62ad077252ca8df8f6be8165318/my_project/demo1.png)

![Demo image 2](https://github.com/uynNee/Enhancing-Personal-Style/blob/d60dfde3b427d62ad077252ca8df8f6be8165318/my_project/demo2.png)

- **Personalized Recommendations**: Offers clothing recommendations based on the user's body shape, skin tone, and gender.
- **Like System**: Users can like products, which influences future recommendations through collaborative filtering.
- **Search Functionality**: Integrated search feature to find products on external platforms like Amazon.

## Technologies Used
- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 for storing user data and preferences
- **Machine Learning**: Scikit-learn for predictive modeling and recommendation algorithms

## What is in /my-project
1. Enhancing Personal Style: The web application, this is the main aspect of this project. Details of how to run the app is specified in [README.md](https://github.com/uynNee/Enhancing-Personal-Style/blob/main/my_project/Enhancing%20Personal%20Style/README.md)
2. data: The [dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small) used to train the model and run the web app. Contains the information and links to each fashion product.
3. notebooks: Contains everything for the preprocessing process (body shape prediction and fashion item recommendation models). Also contains the scratch data from [Body Shape Calculator](https://calculator-online.net/body-shape-calculator/) to build the body shape prediction model.

## Usage of Enhancing Personal Style
- **Register**: Create a new account using the registration form.
- **Login**: Access the system by logging in with your credentials.
- **Set Preferences**: Update your profile with body measurements, skin tone, and gender for personalized recommendations.
- **User Testing**: User can switch between testing page (to rate fashion items) and the main app.
- **Explore Recommendations**: Browse through the recommended clothing items tailored to your profile.
- **Like Items**: Like items to refine future recommendations.

## License
This project is licensed under the Enhancing Personal Style Non-Commercial License - see the LICENSE file for details.
