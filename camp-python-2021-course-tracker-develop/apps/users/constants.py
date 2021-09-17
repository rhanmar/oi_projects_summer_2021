"""Todo: move all permissions and allowed lists into specialized files when
    when there will be no open PRs
"""

__all__ = (
    "DEFAULT_USER_PERMISSIONS",
    "DEFAULT_STUDENT_PERMISSIONS",
    "DEFAULT_MENTOR_PERMISSIONS",
)

DEFAULT_USER_PERMISSIONS = {
    "name": "Default user",
    "permissions": [
        "view_userlink",
        "view_user",
        "view_attachment",
        "view_chapter",
        "view_comment",
        "view_course",
        "view_rating",
        "view_task",
        "view_topic",
        "change_userlink",
    ]
}

DEFAULT_STUDENT_PERMISSIONS = {
    "name": "Student",
    "permissions": DEFAULT_USER_PERMISSIONS["permissions"] + [
        "change_attachment",
        "change_comment",
        "change_rating",
        "add_attachment",
        "add_comment",
        "add_rating",
        "delete_attachment",
        "delete_comment",
        "delete_rating",
    ]
}

DEFAULT_MENTOR_PERMISSIONS = {
    "name": "Mentor",
    "permissions": DEFAULT_USER_PERMISSIONS["permissions"] + [
        "change_attachment",
        "change_comment",
        "change_rating",
        "change_user",
        "change_chapter",
        "change_course",
        "change_rating",
        "change_task",
        "change_topic",
        "add_attachment",
        "add_comment",
        "add_rating",
        "add_user",
        "add_chapter",
        "add_course",
        "add_rating",
        "add_task",
        "add_topic",
        "delete_attachment",
        "delete_comment",
        "delete_rating",
        "delete_user",
        "delete_chapter",
        "delete_course",
        "delete_rating",
        "delete_task",
        "delete_topic",
        "view_solution",
        "can_rate_tasks",
    ]
}
