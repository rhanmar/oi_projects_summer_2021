import pytest

from apps.github.servises import (
    get_comment_from_github_message,
    get_jira_tag_from_branch_name,
    get_mark_from_github_message,
)


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ("kill:feature/PC19-534-fmaerog", "PC19-534"),
        ("2134:feature/qweasdx-aa-fmaerog", "qweasdx-aa"),
        ("2134feature/qweasdx-aa-fmaerog", "qweasdx-aa"),
        ("2134:featureqweasdx-aa-fmaerog", "featureqweasdx-aa"),
    ]
)
def test_get_jira_tag_correct_work(test_data, expected):
    """Ensure that get_jira_tag_from_branch function return correct value."""
    assert get_jira_tag_from_branch_name(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ("Hello world. Mark 6", "Hello world"),
        (
            "qweqweqweqwe. fmadofgmaweoirgm. ewaopfpawe. 111",
            "qweqweqweqwe. fmadofgmaweoirgm. ewaopfpawe"
        ),
        ("zzzzz. xxxx", "zzzzz"),
        ("qweqweqwe", ""),
    ]
)
def test_get_comment_correct_work(test_data, expected):
    """Ensure that get_comment_from_github function return correct value."""
    assert get_comment_from_github_message(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ("Hello world. Mark", 0),
        (
            "qweqweqweqwe. fmadofgmaweoirgm. ewaopfpawe. 111. Mark 9",
            9
        ),
        ("zzzzz. xxxx. 10", 10),
        ("zxvzxcv. Mark 1", 1),
    ]
)
def test_get_mark_correct_work(test_data, expected):
    """Ensure that get_mark_from_github function return correct value."""
    assert get_mark_from_github_message(test_data) == expected
