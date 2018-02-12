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
    user_roles = [x.role for x in course_user.roles.all()]
    _admin_roles = ["Instructor", "TeachingAssistant"]
    for role in _admin_roles:
        if role in user_roles:
            return True
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


def get_default_consent_form():
    return """<div class=WordSection1>

        <p>Dear Participant,</p>

        <p></p>

        <p>Researchers and practitioners from The University of Queensland are seeking 
        your consent to use your data collected through your interactions with the Ripple 
        platform for the current semester (from the first day of classes until the week 
        after final exams) and response to a voluntary 10-minute questionnaire.</p>

        <p></p>

		<p><b>What will my data be used for?</b></p>

        <p>Data collected will be used to:</p>

        <ul><li>improve the design of the platform;</li>

        <li>improve the quality of the recommendations made by the platform;</li>

        <li>improve learning and enhance the learning experience of learners;</li>

        <li>conduct scientific research, particularly, for example, in the areas 
        of cognitive science and educational data mining; and share the results of 
        our research in terms of scientific publications with the broader community.</li></ul>

        <p></p>

		<p><b>What are the risks to me in granting consent?</b></p>

        <p>The data collected will only be from your interactions
        within this platform. The questionnaire, should you choose to complete it, only
        involves questions that relate to your user experience with this platform.
        Results published will only use anonymised and aggregated values to protect
        your identity. As such, we do not anticipate any foreseeable risks involved in
        granting consent.</p>

        <p></p>

		<p><b>Can I revoke my consent at a later date?</b></p>

        <p>You can revoke your consent at any time during the semester.</p>


        <p></p>

		<p><b>How will the data be managed?</b></p>

        <p>The collected data will be collated by the investigators and will be
        stored in password protected electronic formats. Data will only be viewable by
        the researchers working on this project.</p>

        <p></p>

        <p>If
        you agree to provide consent for your data to be used in this research, please
        press the "I accept" button. Otherwise, press the "I decline button".</p>

        <p></p>

        <p>This study adheres to the Guidelines of the ethical
        review process of The University of Queensland and the National Statement on
        Ethical Conduct in Human Research. Whilst you are free to discuss your
        participation in this study with the principal
        investigator of the project Dr Hassan Khosrav (contactable on hkhosrav@uq.edu.au), 
        if you would like to speak to an officer of the University not involved in the 
        study, you may contact the Ethics Coordinators on +617 3365 3924 / +617 3443 1656 
        or email humanethics@research.uq.edu.au.</p>

        </div>
        """