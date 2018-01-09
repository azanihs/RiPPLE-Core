import rfc3987
from celtic_lib import get_lti_validator, LTIValidatorException
from lti.models import LTIConfiguration, RequestHistory
from django.conf import settings

from .endpoint import SignatureEndpoint
from ..exceptions import OAuthException, LTIException
from users.services.UserService import insert_course_if_not_exists, insert_user_if_not_exists, insert_course_user_if_not_exists, update_user_roles, delete_user_roles

ROLE_HANDLES = [
    "Instructor",
    "TeachingAssistant",
    "Administrator",
    "Mentor",
    "Staff",
    "Faculty",
    "Student",
    "Learner",
    "Member",
    "ProspectiveStudent",
    "Alumni",
    "Guest",
    "Observer",
    "Other",
    "None"
]


def validate_lti_request(uri, method, request_payload):
    try:
        lti_validator = get_lti_validator(
            settings.LTI["URL"], settings.LTI["APP_KEY"])
        status, result = lti_validator.validate_request(
            uri, method, request_payload)
        return result
    except LTIValidatorException as e:
        return {"error": e.message}


def request_to_course(lti_params, user):
    course_context = {
        "course_code": lti_params.get("context_id"),
        "course_name": lti_params.get("context_label")
    }

    return insert_course_if_not_exists(course_context, user)


def request_to_user(lti_params, root_path):
    user_context = {
        "user_id": lti_params.get("user_id"),
        "first_name": lti_params.get("lis_person_name_given"),
        "last_name": lti_params.get("lis_person_name_family")
    }

    return insert_user_if_not_exists(user_context, root_path)


def create_course_user(course, user, lti_params):
    if not lti_params["roles"]:
        raise ValueError("LTI request must include roles")

    roles = lti_params["roles"].split(",")
    user_roles = []
    for i in roles:
        parsed_role = ""
        try:
            role = rfc3987.parse(i, rule="URI")
            parsed_role = role["path"].split("/")[-1]
        except ValueError as e:
            # Not a valid URI, check if namespaced already
            parsed_role = i

        if parsed_role not in ROLE_HANDLES:
            raise ValueError("Cannot process role: " + i)

        user_roles.append(parsed_role)
    if not user_roles:
        raise ValueError("No processed roles for user")

    course_user = insert_course_user_if_not_exists(course, user)

    delete_user_roles(course_user)
    for i in user_roles:
        update_user_roles(course_user, i)

    return course_user
