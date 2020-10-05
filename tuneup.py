#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment
Use the timeit and cProfile libraries to find bad code.
"""
__author__ = """
Kevin Clark,
source of help
'https://www.youtube.com/watch?time_continue=377&v=8qEnExGLZfY&feature=emb_logo'
"""

from functools import wraps
from pstats import SortKey
import cProfile
import pstats
import timeit
import io


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        work = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return(work)
    return wrapper


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    movies = [title.lower() for title in movies]
    movies.sort()
    duplicate = [
        movie_one for movie_one, movie_two
        in zip(movies[:-1], movies[1:])
        if movie_one == movie_two
        ]
    return duplicate


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer('main()')
    repeat = 7
    number = 1
    result = t.repeat(repeat, number)
    average = sum(result) / len(result)
    print(
        f"""Best time across {repeat} repeats of {number}
        run(s) per repeat: {average} sec"""
        )
    return result


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
    timeit_helper()