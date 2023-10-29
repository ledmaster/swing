## Implementation of the Swing Algorithm for Substitute Product Recommendation in Python

My attempt at implementing [Large Scale Product Graph Construction for Recommendation in E-commerce](https://arxiv.org/abs/2010.05525).

A very high-level idea of what the Swing algorithm tries to capture:

Alice, Bob, Charles and David visit the product page of the latest NVIDIA GPU.

We look at their visit logs (without regards to the sequence of actions) and find that:
- Alice and Bob visited the product page for a Deep Learning book
- Charles visited the product page for a strategy game
- David went to buy popcorn

Which of these: book, game or popcorn, is the best recommendation for someone that is looking at the product page for the latest NVIDIA GPU?

The Swing Algorithm considers that if many users share the same item, it is likely to be a good recommendation for the seed (GPU) item.

This is not a completely new idea, but Swing weighs the users by how many other items they click, making users that click fewer items more important.

If you found this interesting, you can read more about it in the [original paper](https://arxiv.org/abs/2010.05525).

This code is VERY slow, as I didn't optimize it in any way. It was just a learning exercise for me to internalize and really understand the algorithm.

The complexity is $O(T \cdot N^2 \cdot M)$, where $T$ is the number of items, $N$ is the average degree of item nodes and $M$ is the average degree of user nodes.

I compared it with generating a simple list of best-sellers, and it beat it by a huge margin, so it's likely correct.

Find me at [Forecastegy](https://forecastegy.com).