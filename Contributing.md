# Contributing

If you'd like to contribute something to the project you are more than welcome to. Here's some guidelines to streamline the process.

## Branching

As is stands, the `master` branch will always be the version that is distributed to PyPI. If you need to check the docs for something, it'll be on that branch.
If you'd like to contribute, you should branch off of the `develop` branch. This branch is dedicated to testing, and could be thought of as a sort of staging area.
When you'd like to submit your merge request, make sure that you also merge into the `develop` branch on this repo.

## Code quality
I'm not going to tout myself as some arbiter of code perfection. I'm sure that if you look through here you'll find many examples of weird coding patterns and habits.
My biggest concern is making code easier to read and thus modify. This means:

1. No single character variables. The only exceptions are `f` for file work, and `i` for iterations.
2. If your code is complex to read (i.e. some crazy regex) please add a comment to explain what it's doing.
3. If your code does something really strange, please leave a comment as to **WHY** you are doing something weird. Most of the time someone can read **what** the code does, but there could be a good reason it's there.
4. Please don't leave useless comments (i.e. # end for loop)

Again, there may be some places in here that don't strictly fall in line with these rules, and you are free to call me out if it doesn't.

Documents are formatted with *4 spaces for indentation*.

## Thank you
I'd like to thank you for taking an interest in contributing to Scrython. I'm not always able to work on this and can't keep it maintained all the time, even as Scryfall updates its API.