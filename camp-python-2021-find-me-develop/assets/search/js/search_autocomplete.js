const inputSearch = $("#search-input");
const resultSearch = $("#search-result");

function autocomplete(query) {
  $.ajax({
    url: searchUrl,
    type: "GET",
    data: {"q": query}
  }).done(function (res, textStatus, jqXHR) {
    if (jqXHR.readyState === 4 && jqXHR.status === 200) {
      if (jqXHR.responseJSON.results.length > 0) {
        $.each(jqXHR.responseJSON.results, function () {
          resultSearch.append(
            `<option value="${this.title}"></option>`
          )
        });
        resultSearch.show();
      }
    }
  })
}

inputSearch.change(function () {
  const query = inputSearch.val()
  resultSearch.text("")
  if (query.length > 2) {
    autocomplete(query);
  }
})
