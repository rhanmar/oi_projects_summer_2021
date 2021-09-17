from django.urls import reverse


def get_data(client, title_part):
    """Return response data from """
    response = client.get(
        reverse("api:search-autocomplete-list"),
        params={"q": title_part, "limit": 3}
    )
    return response.data


def test_startups_autocomplete_list(client, startups):
    """Test autocomplete suggestions startup titles."""
    startup = startups[0]
    title_part = startup.title[:len(startup.title) // 2]
    data = get_data(client, title_part)
    autocompletes = map(lambda x: x["autocomplete"], data)
    assert startup.title in list(autocompletes)


def test_cvs_autocomplete_list(client, cvs):
    """Test autocomplete suggestions cv titles."""
    cv_instance = cvs[0]
    title_part = cv_instance.title[:len(cv_instance.title) // 2]
    data = get_data(client, title_part)
    autocompletes = map(lambda x: x["autocomplete"], data)
    assert cv_instance.title in list(autocompletes)


def test_vacancies_autocomplete_list(client, vacancies):
    """Test autocomplete suggestions vacancy titles."""
    vacancy = vacancies[0]
    title_part = vacancy.title[:len(vacancy.title) // 2]
    data = get_data(client, title_part)
    autocompletes = map(lambda x: x["autocomplete"], data)
    assert vacancy.title in list(autocompletes)
