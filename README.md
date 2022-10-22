# Wander List
![alt text](https://github.com/Yubo-Cao/traveler/blob/master/Wander%20List%20Logo.png?raw=true) \
## Inspiration
We were inspired by apps like GeoCache and TripAdvisor for the making of this project. We wanted to be able to combine the interactivity of geocaching with the social factor of TripAdvisor (commenting and viewing other user profiles).

## What it does
Wander List is a website that provide users with a list of places to visit in the world. The user can add places to the list, and also remove places from the list. The user can also edit the places in the list. Essentially, Wander List lets users list the places they have traveled to in the world and rate them. They can post their travel experiences on their profile and comment on other people's experiences. They can comment on nearby places that are in their city and complete "Landmarks" by discovering enough popular places near them in addition to places recommended by the app based on their interests. Users gain experience and level up from completing landmarks and visiting new areas.

## How we built it
We used React and VUE for the backend. We used PyTorch to create embedded layers and collaborative filtering to recommend places to each user. For new places, we used means average precision (MAP) as the evaluation metric. We also used flask to host a SQLite database that holds user information. Object relationship mapping was used to map the database to the python objects with SQL alchemy.

## Challenges we ran into
We struggled for an hour to deploy the Flask server. We also spent a very long time on the backend when we could have worked more on the frontend instead.
## Accomplishments that we're proud of
- We created a recommendation algorithm that is better than many other full-stack software out there and deployed it onto a website. 
- We made a minimalist database and integrated it with Javascript objects using OOP and SQLite.
- We manually created a Python scraper for extracting Place objects from Google Maps because their official API wanted to charge us money

## What we learned
- How to manage our time better 
- How to communicate better
- How to delegate tasks better with tasks that we specialize in

## What's next for Wander List
- Integration with user location permissions
- A mobile application
- Being able to add past travels to one's travel list (it won't earn you points, though)


