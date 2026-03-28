from models.tag_model import (
    create_tag, search_tags, get_user_tags,
    add_tag_to_user, remove_tag_from_user, count_user_tags
)
from utils.profile_validator import validate_tag_name
from services.profile_service import check_profile_completeness
from services.constants import MAX_TAGS_PER_USER
from services.errors import (
    ERR_MAX_TAGS, ERR_TAG_CREATION_FAILED,
    ERR_TAG_NOT_FOUND, ERR_SEARCH_QUERY_REQUIRED
)


def add_tag_to_profile(user_id, tag_name):
    valid, error = validate_tag_name(tag_name)
    if not valid:
        raise Exception(error)

    tag_count = count_user_tags(user_id)
    if tag_count >= MAX_TAGS_PER_USER:
        raise Exception(ERR_MAX_TAGS)

    tag = create_tag(tag_name)
    if not tag:
        raise Exception(ERR_TAG_CREATION_FAILED)
    add_tag_to_user(user_id, tag["id"])
    check_profile_completeness(user_id)

    return get_user_tags(user_id)


def remove_tag_from_profile(user_id, tag_name):
    tags = get_user_tags(user_id)
    tag = next((t for t in tags if t["name"] == tag_name), None)
    if not tag:
        raise Exception(ERR_TAG_NOT_FOUND)

    remove_tag_from_user(user_id, tag["id"])
    check_profile_completeness(user_id)

    return get_user_tags(user_id)


def get_user_profile_tags(user_id):
    return get_user_tags(user_id)


def search_available_tags(query):
    if not query or len(query.strip()) < 1:
        raise Exception(ERR_SEARCH_QUERY_REQUIRED)
    return search_tags(query.strip())
