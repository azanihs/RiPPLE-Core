import itertools
import imghdr

from base64 import b64decode
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError

from questions.models import Question, Distractor, QuestionImage, ExplanationImage, DistractorImage
from users.models import ConsentImage

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


def generate_static_path(host):
    def _format(x):
        if len(x) == 0: return x
        return (x + "/") if x[-1] != "/" else x

    return merge_url_parts([
        _format("//" + host),
        _format("static")
    ])

def mean(collection):
    return sum((float(x) for x in collection)) / float(len(collection))

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
                       name="u" + str(image_id) + "." + ext)
    # Validate image
    if imghdr.what(data) != ext:
        return None
    return data

def merge_url_parts(parts, url=""):
    if len(parts) == 0:
        return url
    return merge_url_parts(parts, urljoin(url, parts.pop(0)))

def is_administrator(course_user):
    if "Instructor" in (x.role for x in course_user.roles.all()):
        return True
    else:
        return False

def verify_content(content):
    if len(content) == 0:
        return False

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all('script')
    if len(scripts) > 0:
        return False
    return True

def extract_image_from_html(image_id, obj, images, image_type, host):
    # type q=question, d=distractor, e=explanation, c=ConsentFormImage
    urls = []
    database_image_types = {
        "c": ConsentImage,
        "q": QuestionImage,
        "d": DistractorImage,
        "e": ExplanationImage
    }
    ImageToSaveClass = database_image_types.get(image_type, None)

    for i, image in images.items():
        contentfile_image = save_image(image, image_id)
        if contentfile_image is None:
            raise IntegrityError("Image is not of valid type")

        if image_type == "c":
            new_image = ImageToSaveClass.objects.create(form=obj, image=contentfile_image)
        # Question + Explanation in the same object
        elif image_type == "q" or image_type == "e":
            new_image = ImageToSaveClass.objects.create(question=obj, image=contentfile_image)
        else:
            new_image = ImageToSaveClass.objects.create(distractor=obj, image=contentfile_image)
        urls.append(new_image.image.name)

    if image_type == "e":
        obj.explanation = update_image_sources(urls, obj.explanation, host)
    else:
        obj.content = update_image_sources(urls, obj.content, host)

    obj.save()


def update_image_sources(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    # Only get substitutable images
    images = soup.find_all("img", src=lambda img_src: img_src.startswith("#:"))
    for i, file_location in enumerate(urls):
        images[i]['src'] = "//" + host + file_location
        images[i]['src'] = merge_url_parts([host, file_location])

    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])
