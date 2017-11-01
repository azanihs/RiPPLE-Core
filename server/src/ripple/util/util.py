import itertools


def is_number(inStr):
    try:
        val = int(inStr)
        return True
    except ValueError:
        return False


def combinations(iterable):
    """
        From https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
        Returns all combinations of the provided iterable (inclusive of subsets)
    """
    combination_set = []
    for L in range(1, len(iterable) + 1):
        for subset in itertools.combinations(iterable, L):
            combination_set.append(subset)
    return combination_set


def topic_weights(question_topics):
    """
        Returns all topic weights for the given topics such that the weight is the topic_combination_length / total_topics
    """
    return [{
        "weight": len(x) / float(len(question_topics)),
        "topics": x
    } for x in combinations(question_topics)]
