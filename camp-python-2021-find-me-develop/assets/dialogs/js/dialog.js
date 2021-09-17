function loadJson(selector) {
  // Load data from template "json_script" tags.
  return JSON.parse(document.getElementById(selector).innerText)
}

/** Dialog id from template **/
const dialogId = loadJson("dialog_id");

/** Websocket for chat handling. **/
const chatSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/dialog/'
  + dialogId
  + '/'
);

/** Message container element **/
const messageContainer = document.getElementById('message-container');

/** URL of next page of messages **/
let nextPageUrl = null;

/** Add messages to html **/
function drawMessage (toStart, messageObject) {
  const data = JSON.parse(messageObject.data);
  const senderData = JSON.parse(data.sender_data);
  const currentUserId = loadJson("user_id")
  if (data.sender === currentUserId) {
    const sentMessageHtml = `
      <div class="panel-body msg_container_base">
        <div class="row msg_container base_sent">
          <div class="col-md-10 col-xs-10">
            <div class="messages msg_sent">
              <p class="message-text">${data.message}</p>
              <time>
                ${senderData.first_name}
                ${senderData.last_name}
              </time>
            </div>
          </div>
          <div class="col-md-2 col-xs-2 avatar">
            <img class="img-responsive" src="${senderData.avatar_thumbnail}" style="width: 50px; height: 50px;">
          </div>
        </div>
      </div>`
    if (toStart === false){
      messageContainer.innerHTML += (sentMessageHtml + '\n');
    }
    else {
      messageContainer.innerHTML = sentMessageHtml + '\n' + messageContainer.innerHTML
    }
  }
  else {
    const receivedMessageHtml = `
      <div class="panel-body msg_container_base">
        <div class="row msg_container base_receive">
          <div class="col-md-2 col-xs-2 avatar">
            <img class="img-responsive" src="${senderData.avatar_thumbnail}" style="width: 50px; height: 50px;">
          </div>
          <div class="col-md-10 col-xs-10">
            <div class="messages msg_receive">
              <p class="message-text">${data.message}</p>
              <time>
                ${senderData.first_name}
                ${senderData.last_name}
              </time>
            </div>
          </div>
        </div>
      </div>`
    if (toStart === false) {
      messageContainer.innerHTML += (receivedMessageHtml + '\n');
    }
    else {
      messageContainer.innerHTML = receivedMessageHtml + '\n' + messageContainer.innerHTML
    }
  }
}

/** Check if scrolling bar of message container is at top. **/
function isFeedAtTop() {
    return 0 === messageContainer.scrollTop;
}

/** Fetches previous messages and draws it (defaults to 15). **/
function getPrevious15Messages() {
  if (nextPageUrl != null) {
    $.ajax({
      url: nextPageUrl,
      type: "GET",
    }).done(function (res, textStatus, jqXHR) {
      $.each(res.results, function () {
        nextPageUrl = res.next;
        const messageObject = {
        "data": JSON.stringify({
            "message": this.text,
            "sender": `${this.sender}`,
            "sender_data": JSON.stringify(this.sender_data),
          })
      };
      drawMessage(true, messageObject);
      })
    })
  }
}

/** Listen to scroll event **/
messageContainer.addEventListener("scroll", () => {
  if (isFeedAtTop()) {
    getPrevious15Messages();
  }
})

/** Listen to new messages. **/
chatSocket.onmessage = function (event) {
  drawMessage(false, event);
  messageContainer.scrollTop = messageContainer.scrollHeight;
}

/** Listen to socket close event. **/
chatSocket.onclose = function (e) {
  console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
  if (e.keyCode === 13) {  // enter, return
    document.querySelector('#btn-chat-message-submit').click();
  }
};

document.querySelector('#btn-chat-message-submit').onclick = function (e) {
  const messageInputDom = document.querySelector('#chat-message-input');
  const message = messageInputDom.value;
  chatSocket.send(JSON.stringify({
    'message': message,
  }));
  messageInputDom.value = '';
};

/** Fetches dialog info and previous 15 messages when DOM was loaded. **/
$(document).ready(function (event) {

  $.ajax({
    url: dialogUrl,
    type: "GET",
  }).done(function (res, textStatus, jqXHR) {
    $("#chat-name").text(res.title)
  })

  $.ajax({
    url: messagesUrl,
    type: "GET",
    data: {"dialog_id": dialogId}
  }).done(function (res, textStatus, jqXHR) {
    $.each(res.results.reverse(), function() {
      nextPageUrl = res.next;
      const messageObject = {
      "data": JSON.stringify({
          "message": this.text,
          "sender": `${this.sender}`,
          "sender_data": JSON.stringify(this.sender_data),
        })
      };
      drawMessage(false, messageObject);
    })
    messageContainer.scrollTop = messageContainer.scrollHeight;
  })
})

/** Leave meeting elements. **/
const btnLeaveMeeting = $('#btn-leave-meeting')
const alertLeaveMeeting = $('#alert-leave-meeting')

/** Listen to leave button click. **/
btnLeaveMeeting.click(function () {
  const url = meetingLeaveUrl;
  const csrfToken = Cookies.get("csrftoken");
  const data = "csrfmiddlewaretoken=" + csrfToken
  $.ajax({
    url: url,
    type: "POST",
    data: data
  }).done(function (res, textStatus, jqXHR) {
    if (jqXHR.readyState === 4 && jqXHR.status === 200) {
      window.location = "/";
    }
  }).fail(function (res, textStatus, jqXHR) {
    alertLeaveMeeting.text(res.responseJSON.error)
    alertLeaveMeeting.css("visibility", "visible");
    setTimeout(() => {
        alertLeaveMeeting.css("visibility", "hidden")
      }, 5000
    );
  });
})

