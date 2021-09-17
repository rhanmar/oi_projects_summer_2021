def get_jira_tag_from_branch_name(branch_name: str) -> (str, None):
    """Return jira tag from branch name string.

    For example:
        in:
            "feature/PC19-100-py-camp"
        out:
            "PC19-100"
    """
    current_branch = branch_name[branch_name.find(":") + 1:]
    current_jira_tag_list = current_branch[current_branch.find(
        "/"
    ) + 1:].split("-", 2)
    current_jira_tag = "-".join(current_jira_tag_list[:2])
    return current_jira_tag


def get_comment_from_github_message(github_message: str) -> str:
    """Return all sentences in string except last."""
    message_list = github_message.split(".")
    comment = ".".join(message_list[:-1])
    return comment


def get_mark_from_github_message(github_message: str) -> int:
    """Return last item of str if it is integer."""
    if github_message[-2:].isdigit() and int(github_message[-2:]) == 10:
        return 10
    mark = github_message[-1]
    if not mark.isdigit():
        return 0
    return int(mark)
