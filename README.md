# collisions
High energy proton-proton collisions as an *inspiration*. 

# Why?
Nowadays, scientists use large particle accelerators to collide particles and study the tiniest components of matter. Each collision generates hundreds of particles that compose beautiful patterns, exhibiting the power and simplicity of the fundamental laws of nature. We would like to capture these moments.

# What?
We use a state-of-the-art event generator called [PYTHIA8](http://home.thep.lu.se/~torbjorn/Pythia.html) - which is also used in particle physics research - to simulate the collision process realistically. You can choose from a wide range of established physics process, such as the [Higgs boson](https://en.wikipedia.org/wiki/Higgs_boson) production, or hypothetical processes which are currently in study, such production of [dark matter](https://en.wikipedia.org/wiki/Dark_matter) or the inclusion of [supersymmetry](https://en.wikipedia.org/wiki/Supersymmetry).

# How?
Install [docker](https://www.docker.com/products/docker-desktop). Download the content of this repository (or git clone it).

Open the terminal of your computer and enter into the folder with the content of this repository. Now run:

    docker-compose up

Go to your browser and type:

    localhost:8888

You will get a jupyter notebook server where you can interact with the data, generate more events and try some of the plots. It is recommended for you to first try the tutorial.

