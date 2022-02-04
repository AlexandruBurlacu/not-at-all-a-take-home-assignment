# Take home assignment for Sprout.ai

Basically, a (dummy) blog API that interacts with a (dummy) content moderation system. The content moderation takes the form of detection of foul language in blog posts and flagging said blogposts.

## How to launch it?

Simple answer: `docker-compose up`

A bit longer answer: If you don't want to use `docker-compose` or `docker` in general, you can launch it locally, following the steps below.
1. Create a virtual environment, be it `venv` or `conda`.
2. Once done, activate it. Depending on what kind of virtual environment you use, it will be either `source <virtual environment name>/bin/activate` for `venv`, or `conda activate <virtual environment name>` for `conda`.
3. Before launching _only_ the dummy API, install `pip install -r requirements.txt`.
4. What do I mean by _only_? You see, to also run tests, type checking, or a better REPL, you will need to install `pip install -r dev-requirements.txt`. Why so many requirements files, you ask? To keep the docker image size to the minimum.
5. You're ready to launch it. Type `uvicorn blog_api:app` into your shell, and you're good to go.

You can access the Swagger docs at `http://localhost:8000/docs`.

## How to develop it? Test it? Type-check it?

First, follow the __How to launch it?__ part. Then...
1. Run `pip install -r dev-requirements.txt`.
2. Run `pytest tests/` for testing the project.
3. Run `mypy .` for type checking the project. On its first run, it might take a while, don't worry, it's not broken.


## Discussions

I couldn't keep myself from showing off at least a bit. That's why this solution has the following whistles and bells.
- Because I decided it would be better to detect and flag blogposts with foul language soon after they were added, I opted for a deferred task approach of architecting this thing.
- Because of this, I needed a way to defer tasks, and that's why I used a `ThreadPoolExecutor`. Why not go the `asyncio` way? Because using `ThreadPoolExecutor` allows for a simple implementation of a kind of client-side rate limiter. Basically, it would somewhat prevent overflowing the ML API from too many in-flight requests by limiting them to the number of `max_workers`, which can be set with an env var.
- Also, an exponential backoff strategy, with jitter, was implemented to handle occasional 5xx errors from the ML API. It was inspired by [this](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) blog on AWS.

## What's missing for it to be a production-like system?

- More tests.
- Better (read cleaner) code organization, although I tried.
- A persistent connection to the ML API, so as to not waste time on TCP and TLS handshakes.
- Obviously a proper database, and an easy way to vertically scale the application. I forwarded the container port outside, so it's non-trivial now to `docker-compose up --scale=K blog`.

