# Wander List
<p align="center">
  <img src="https://github.com/Yubo-Cao/traveler/blob/master/Wander%20List%20Logo.png?raw=true">
</p>

Wander List is a website that provide users with a list of places to visit
in the world. The user can add places to the list, and also remove places
from the list. The user can also edit the places in the list.

In addition, embedding layers and collaborative filtering are used to
recommend places to the user. Pytorch is used to build the embedding layers,
and the collaborative filtering is implemented using the KNN algorithm. In
addition, we recmmended places to the user based on the places they have
visited. For zero-shot (i.e., new places) recommendations, we used means
average precision (MAP) as the evaluation metric.

This is a flask app that uses a sqlite database to store the places. Object
relationship mapping is used to map the database to the python objects (sql
alchemy).

# Media

<p align="center">
  <img src="media.png">
</p>
