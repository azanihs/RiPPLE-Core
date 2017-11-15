import itertools
from django.core.files.base import ContentFile
from base64 import b64decode
import imghdr
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

def is_number(test_str):
    try:
        val = int(test_str)
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


def save_image(encoded_image, image_id):
    image_format, base64_payload = encoded_image.split(';base64,')
    ext = image_format.split('/')[-1]
    data = ContentFile(b64decode(base64_payload),
                       name="u" + image_id + "." + ext)
    # Validate image
    if imghdr.what(data) != ext:
        return None
    return data

def merge_url_parts(parts, url=""):
    if len(parts) == 0:
        return url
    return merge_url_parts(parts, urljoin(url, parts.pop(0)))
