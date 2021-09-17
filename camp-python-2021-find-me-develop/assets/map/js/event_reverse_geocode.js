ymaps.ready(initMap);

const createdMarks = [];
let userLocationMark;
let idOpenedSelfMeeting = -1;
let idChosenUser = -1;
let reviewId;
const meetingType = "Meeting";

// Process blocks
const processModalAddMeeting = $("#process_add_meeting_modal");
const processModalUser = $("#process_user_modal");
const processDetailMeeting = $("#process_detail_meeting");

// Save meeting
const sendMeeting = $("#send_meeting");

// Alert block for meeting
const alertJoinMeeting = $("#alert_join_meeting");

// Alert blocks for  reviews
const alertAddReview = $("#alert-add-review");
const alertEditReview = $("#alert-edit-review");

// Modals for meeting
const modalDetailMeeting = $("#modal_detail_meeting");
const modalAddMeeting = $("#modal_add_meeting");

// Modals for review
const modalListReviews = $("#modal-list-reviews");
const modalAddReview = $("#modal-add-review");
const modalEditReview = $("#modal-edit-review");

// Modal for user
const modalUserDetail = $("#modal_detail_user");

// Meetings buttons
const btnEditMeeting = $("#btn_edit_meeting");
const btnDelMeeting = $("#btn_del_meeting");
const btnJoinMeeting = $("#btn_join_meeting");

// Review buttons
const btnAddReview = $("#btn-add-review");
const btnEditReview = $("#btn-edit-review");
const btnDelReview = $("#btn-delete-review");
const btnListReviews = $("#btn-list-reviews");

// User buttons
const btnTextUser= $("#btn_text_user");

function initMap() {
  const geolocation = ymaps.geolocation;

  const mapState = {
    center: [56.8431, 60.6454],
    zoom: 17,
    controls: ["typeSelector", "fullscreenControl",
      "zoomControl", "searchControl"],
  };

  const mapOptions = {searchControlProvider: "yandex#search"};
  const map = new ymaps.Map("map", mapState, mapOptions);

  geolocation.get().then(function (result) {
    const coords = result.geoObjects.get(0).geometry.getCoordinates();
    map.setCenter(coords, 11)
  })

  let placemark;
  map.events.add("click", handleMapClick);

  if (isUserLocationVisible)
    setUserLocation();

  loadMarks();
  setInterval(() => {
    map.geoObjects.removeAll();
    createdMarks.length = 0;
    loadMarks()
    if (isUserLocationVisible) {
      map.geoObjects.remove(userLocationMark);
      setUserLocation();
    }
  }, 60 * 1000);

  /** Load locations form db and display it on the map. */
  function loadMarks() {
    $.ajax({
      url: locationsUrl,
      type: "GET",
    }).done(displayPoints).fail(displayFail);
  }

  function displayPoints(res, textStatus, jqXHR) {
    if (jqXHR.readyState === 4 && jqXHR.status === 200) {
      res.forEach(
        location => {
          const createdMark = createPlacemark(
            location.point, location.title,
            location.point_type, location.linked_id
          );
          map.geoObjects.add(createdMark);
          addClickListenerToPlacemark(
            createdMark, location.point_type, location.linked_id
          )
        }
      )
    } else {
      console.log(res)
    }
  }

  function displayFail(res, textStatus, jqXHR) {
    console.log(res)
  }

  $(".close_meeting_form").click(function () {
    map.geoObjects.remove(placemark);
    placemark = undefined;
  });

  $("#form_add_meeting").submit(function (event) {
    event.preventDefault();

    $.ajax({
      url: meetingsUrl,
      type: "POST",
      data: $(this).serialize(),
      beforeSend: function () {
        processModalAddMeeting.show();
      },
    }).done(addNewMeetingToMap);
  });

  $("#form-add-review").submit(function (event) {
      event.preventDefault();
      let data = $(this).serializeArray();
      data.push({name: "meeting", value: idOpenedSelfMeeting})

      $.ajax({
        headers: {"csrftoken": $("#form-add-review > input[name='csdfmiddlewaretoken']").value},
        url: reviewsUrl,
        type: "POST",
        data: data
      }).done(function (res, textStatus, jqXHR) {
        if (jqXHR.readyState === 4 && jqXHR.status === 201) {
        modalAddReview.modal("hide");
        }
      }).fail(function (res, textStatus, jqXHR) {
        alertAddReview.text(res.responseJSON.data.meeting[0]);
        alertAddReview.css("visibility", "visible");
        setTimeout(
          () => alertAddReview.css("visibility", "hidden"),
          5000
        )
      })
    });

  $("#form-edit-review").submit(function (event) {
      event.preventDefault();
      let data = $(this).serializeArray();
      data.push({
        name: "meeting",
        value: idOpenedSelfMeeting,
      })
      const update_url = reviewsUrl + reviewId + "/"

      const csrf_token = $("#form-add-review input[name='csrfmiddlewaretoken']")[0].value
      $.ajax({
        url: update_url,
        headers: {"X-CSRFToken": csrf_token},
        type: "PATCH",
        data: data
      }).done(function (res, textStatus, jqXHR) {
        if (jqXHR.readyState === 4 && jqXHR.status === 200) {
          modalEditReview.modal("hide");
        }
      }).fail(function (res, textStatus, jqXHR) {
        console.log(res);
        alertEditReview.text(res.responseJSON.error);
        alertEditReview.css("visibility", "visible");
        setTimeout(
          () => alertEditReview.css("visibility", "hidden"),
          5000
        )
      })
    });

  function addClickListenerToPlacemark(mark, locationType, linked_id) {
    mark.events.add("click", function () {
      let url;
      if (locationType === meetingType)
        url = meetingsUrl + linked_id;
      else
        url = usersBaseUrl + linked_id + "/";
      $.ajax({
        url: url,
        type: "GET",
      }).done(function (res, textStatus, jqXHR) {
        if (jqXHR.readyState === 4 && jqXHR.status === 200) {
          if (locationType === meetingType)
            fillModalMeeting(res, linked_id);
          else {
            fillModalUser(res, linked_id);
            idChosenUser = linked_id;
          }
        }
      });
    });
  }

  function setUserLocation() {
    geolocation.get({
      provider: 'browser',
      mapStateAutoApply: false
    }).then(function (result) {
      userLocationMark = result.geoObjects.get(0);
      result.geoObjects.options.set('preset', 'islands#violetCircleIcon');
      map.geoObjects.add(result.geoObjects);
      uploadUserLocation(userLocationMark);
    });
  }

  /** Send user location coords to backend.*/
  function uploadUserLocation(placemark) {
    const coords = placemark.geometry.getCoordinates();
    const csrfToken = Cookies.get("csrftoken");
    const data = `csrfmiddlewaretoken=${csrfToken}&user_coords=${coords}`;
    $.ajax({
      url: changeUserLocationUrl,
      type: "POST",
      data: data,
    }).done(function (res, textStatus, jqXHR) {
      if (jqXHR.readyState === 4 && jqXHR.status === 201) {
        console.log("Success");
      }
    });
  }

  /** Check result of creation meeting and add new location to map.
   *
   * If add meetings is success it changes 'hasVisitorMeeting' to true.
   */
  function addNewMeetingToMap(res, textStatus, jqXHR) {
    document.getElementById("form_add_meeting").reset();
    if (jqXHR.readyState === 4 && jqXHR.status === 201) {
      hasVisitorMeeting = true;
      map.geoObjects.remove(placemark);
      const addedMeeting = createPlacemark(
        res.location.point, res.location.title, res.location.point_type
      )
      map.geoObjects.add(addedMeeting);
      addClickListenerToPlacemark(
        addedMeeting, res.location.point_type, res.location.linked_id
      )
      modalAddMeeting.modal("hide");
    } else console.log(res);
    sendMeeting.hide();
  }

  /** Fill modal meeting detail.*/
  function fillModalMeeting(res, linked_id) {
    $("#modal_detail_meeting_label").text(res.title);
    $("#meeting_description").text(res.description);
    $("#meeting_deadline").text(
      `Date of end: ${res.deadline}`
    );
    $("#meeting_owner").attr(
      "href",
      `${baseProfileUrl}${res.created_by}`
    ).text('Meeting owner profile');
    $("#meeting_members").text(
      `Members: ${res.dialog_members_count}/${res.max_people_limit}`
    );


    alertJoinMeeting.hide();
    const url = baseMeetingUrl + linked_id + "/";
    let isVisitorMeeting = false;
    if (visitorId === res.created_by) {
      btnEditMeeting.attr("href", url);
      isVisitorMeeting = true;
    }

    let hasUserReview = false;
    if (res.current_user_review_id != null) {
      reviewId = res.current_user_review_id;
      hasUserReview = true;
    }


    btnJoinMeeting.toggle(!isVisitorMeeting);
    btnEditMeeting.toggle(isVisitorMeeting);
    btnDelMeeting.toggle(isVisitorMeeting);
    btnAddReview.toggle(!hasUserReview);
    btnEditReview.toggle(hasUserReview);
    btnDelReview.toggle(hasUserReview);

    idOpenedSelfMeeting = linked_id;
    modalDetailMeeting.modal("show");
  }

  /** Fill modal user detail.*/
  function fillModalUser(res, linked_id) {
    $("#user_avatar").attr("src", res.avatar);
    $("#user_fullname").text(res.fullname);
    $("#user_rating").text(res.rate);
    $("#user_email").text(res.email);

    btnTextUser.toggle(visitorId !== linked_id)
    modalUserDetail.modal("show");
  }

  /**
   * Handle a click on the map.
   *
   * Move Placemark if exists to the click coordinates.
   * Create on coordinates if does not exist.
   */
  function handleMapClick(event) {
    if (hasVisitorMeeting) {
      // TODO: add handler for this situation
      return;
    }

    const coords = event.get('coords');
    modalAddMeeting.modal("show");
    $("#location_field").val(coords);
    if (placemark) {
      placemark.geometry.setCoordinates(coords);
      return
    }
    placemark = createPlacemark(coords);
    map.geoObjects.add(placemark);
  }

  /** Create new placemark. */
  function createPlacemark(coords, title, type, linked_id) {
    if (type === "Meeting")
      return new ymaps.Placemark(
        coords,
        {
          hintContent: type,
          balloonContent: title,
        },
        {
          preset: "islands#icon",
          iconColor: '#0095b6'
        }
      );

    let markPreset;
    if (linked_id === visitorId)
      markPreset = "islands#purpleCircleIcon";
    else
      markPreset = "islands#blueCircleIcon";
    return new ymaps.Placemark(
      coords,
      {
        hintContent: type,
        balloonContent: title,
      },
      {
        preset: markPreset,
      }
    );
  }

  modalDetailMeeting.on("hide.bs.modal", function () {
    idOpenedSelfMeeting = -1;
  });

  btnDelMeeting.click(function () {
    const url = meetingsUrl + idOpenedSelfMeeting + "/";
    const csrfToken = Cookies.get("csrftoken");
    $.ajax({
      url: url,
      type: "DELETE",
      headers: {
        "X-CSRFTOKEN": csrfToken,
      },
      beforeSend: function () {
        processDetailMeeting.show();
      }
    }).done(function (res, textStatus, jqXHR) {
      if (jqXHR.readyState === 4 && jqXHR.status === 204) {
        hasVisitorMeeting = false;
        map.geoObjects.removeAll();
        loadMarks();
        modalDetailMeeting.modal("hide");
      }
      processDetailMeeting.hide();
    });
  });

  btnJoinMeeting.click(function() {
    const url = meetingsUrl + idOpenedSelfMeeting + "/join/";
    const csrfToken = Cookies.get("csrftoken");
    const data = "csrfmiddlewaretoken=" + csrfToken
    $.ajax({
      url: url,
      type: "POST",
      data: data,
      beforeSend: function () {
         processDetailMeeting.show();
      }
    }).done(function (res, textStatus, jqXHR){
      if (jqXHR.readyState === 4 && jqXHR.status === 201) {
        console.log(res);
        window.location = res.dialog_url;
      }
      else {
        alertJoinMeeting.text("Meeting is full.")
        alertJoinMeeting.show();
      }
      processDetailMeeting.hide();
    }).fail(function (res, textStatus, jqXHR) {
      alertJoinMeeting.text("Meeting is full.")
      alertJoinMeeting.show();
      processDetailMeeting.hide();
    });
  });

  btnListReviews.click(function () {

    $.ajax({
      url: reviewsUrl,
      type: "GET",
      data: {"meeting": idOpenedSelfMeeting}
    }).done(function (res, textStatus, jqXHR) {
      $.each(jqXHR.responseJSON, function (num) {
        $("#modal-list-reviews .list-reviews").append(
          `<label for="reiview-title-${num}">Title</label>` +
          `<p id="review-title-${num}" class="review-title">${this.title}</p>` +
          `<label for="reiview-body-${num}">Text</label>` +
          `<p id="review-body-${num}" class="review-body">${this.body}</p>` +
          `<label for="reiview-rate-${num}">Rated</label>` +
          `<p id="review-rate-${num}" class="review-rate">${this.rate}</p>` +
          `<hr style="background: whitesmoke;">`
        )
      })
      modalListReviews.modal("show");
    }).fail(function () {
      alertJoinMeeting.text("Cannot get reviews.")
      alertJoinMeeting.show();
    })

  })

  modalListReviews.on("hidden.bs.modal",function () {
    $("#modal-list-reviews .list-reviews").html("");
  })

  btnAddReview.click(function () {
    modalAddReview.modal("show");
  });

  btnEditReview.click(function () {

    $.ajax({
      url: reviewsUrl,
      type: "GET",
      data: {"meeting": idOpenedSelfMeeting, "created_by": visitorId}
    }).done(function (res, textStatus, jqXHR) {
      if (jqXHR.readyState === 4 && jqXHR.status === 200 && jqXHR.responseJSON.length > 0) {
        reviewId = jqXHR.responseJSON[0].id;
        $("#form-edit-review input#id_title").val(jqXHR.responseJSON[0].title);
        $("#form-edit-review textarea#id_body").val(jqXHR.responseJSON[0].body);

        $("#form-edit-review input[name='rate']").each(function () {
          if ($(this).val() === String(jqXHR.responseJSON[0].rate)) {
            $(this).prop("checked", "checked");
          }
        })
        modalEditReview.modal("show");
      }
      else {
        alertJoinMeeting.text("You don't have a review")
        alertJoinMeeting.css("display", "inline");
        setTimeout(
          () => alertJoinMeeting.css("display", "none"),
          5000
        )
      }
    })
  })

  btnDelReview.click(function () {
    $.ajax({
      url: reviewsUrl,
      type: "GET",
      data: {"meeting": idOpenedSelfMeeting, "created_by": visitorId}
    }).done(function (res, textStatus, jqXHR) {
      if (jqXHR.readyState === 4 && jqXHR.status === 200 && jqXHR.responseJSON.length > 0) {
        reviewId = jqXHR.responseJSON[0].id;
      }
    })

    const csrf_token = Cookies.get("csrftoken");
    let delete_url = reviewsUrl + reviewId + "/";

    $.ajax({
        url: reviewsUrl + reviewId + "/",
        headers: {"X-CSRFToken": csrf_token},
        type: "DELETE",
      }).done(function (res, textStatus, jqXHR) {
        if (jqXHR.readyState === 4 && jqXHR.status === 204) {
          alertJoinMeeting.text("Review was deleted successfully.");
          alertJoinMeeting.css("display", "inline");
          setTimeout(
            () => alertJoinMeeting.css("display", "none"),
            5000
          )
        }
        else {
          alertJoinMeeting.text(res.responseJSON);
          alertJoinMeeting.css("display", "inline");
          setTimeout(
            () => alertJoinMeeting.css("display", "none"),
            5000
          )
        }
      }).fail(function (res, textStatus, jqXHR) {
        console.log(res);
        alertJoinMeeting.text(res.responseJSON[0]);
        alertJoinMeeting.css("visibility", "visible");
        setTimeout(
          () => alertEditReview.css("visibility", "hidden"),
          5000
        )
      })
  })
}

modalUserDetail.on("hide.bs.modal", function () {
  idChosenUser = -1;
});

$("#btn_go_to_user").click(function () {
  const url = baseProfileUrl + idChosenUser + "/";
  window.open(url, '_blank');
});

btnTextUser.click(function () {
  const url = usersBaseUrl + idChosenUser + "/join/";
  const csrfToken = Cookies.get("csrftoken");
  const data = "csrfmiddlewaretoken=" + csrfToken;
  $.ajax({
    url: url,
    type: "POST",
    data: data,
    beforeSend: function () {
      processModalUser.show();
    }
  }).done(function (res, textStatus, jqXHR) {
    if (jqXHR.readyState === 4 && jqXHR.status === 201) {
      window.location = res.dialog_url;
    }
    processModalUser.hide();
  });
});
