const typeReplyParent = "reply_to_parent";
const idPrefix = "reply_to_";

let lastFormAddChildComment;

const comments = $("#comments");
const parentCommentText = $("#parent_text_comment");

const socket = new WebSocket(
  "ws://" + window.location.host + `/ws/comments/${modelName}/${objectId}/`
);

socket.onmessage = function (event) {
  const receivedData = JSON.parse(event.data);

  if (receivedData.status === "failed") {
    alert("Text: " + receivedData.errors.text);
    return
  }

  if (receivedData.parent === null)
    addParentComment(receivedData);
  else {
    removeFormAddChildComment();
    $("#reply_" + receivedData.parent).remove();
    addChildComment(receivedData);
  }
}

$(document).ready(function () {
  $("#form_add_parent_comment").submit(function (event) {
    event.preventDefault();
    const text = parentCommentText.val();
    const data = JSON.stringify({
      "text": text, "parent": null,
    })
    socket.send(data);
    parentCommentText.val("");
  });

  $(".btn_reply").click(clickBtnReply);

  parentCommentText.focusin(removeFormAddChildComment);
});

/** Add form for create child comment and delete last added form.*/
function addFormChildComment(parentDivId, parentId) {
  if (lastFormAddChildComment) lastFormAddChildComment.remove();

  const parentDiv = $(parentDivId);
  const form = $(
    `
      <form class="d-flex flex-column" method="post" id="form_add_child_comment">
        <input type="hidden" name="parent" id="id_parent" value="${parentId}">
        <textarea class="form-control" id="child_text_comment" rows="3" name="text" placeholder="Text"></textarea>
        <div class="d-flex mt-3">
          <button type="submit" class="btn btn-success btn_add_child_comment">Add</button>
          <button type="button" class="btn btn-secondary btn_close_form_add_comment">Close</button>
        </div>
      </form>
    `
  )
  parentDiv.append(form);
  lastFormAddChildComment = parentDiv.children().last();

  $(".btn_close_form_add_comment").click(removeFormAddChildComment);

  $("#form_add_child_comment").submit(function (event) {
    event.preventDefault();
    const text = $("#child_text_comment").val();
    const data = JSON.stringify({
      "text": text, "parent": parentId,
    });
    socket.send(data);
  })

  const childTextComment = $("#child_text_comment");
  childTextComment.focus();
}

/** Add parent comment to comments div.*/
function addParentComment(commentInfo) {
  const comment = `
    <div class="parent_comment d-flex flex-column mb-1" id="parent_${commentInfo.id}">
      <div class="d-flex align-items-center mb-1">
        <img src="${commentInfo.user_avatar}" alt="" class="author_avatar">
        <div class="d-flex flex-column">
          <span class="author_name">${commentInfo.username}</span>
          <span class="text-muted comment_date">${commentInfo.time}</span>
        </div>
      </div>
      <span class="comment_text text-wrap">${commentInfo.text}</span>
      <div class="reply_to_parent">
        <button class="btn_reply" data-parent="${commentInfo.id}" id="reply_${commentInfo.id}">&#8627;Reply</button>
      </div>
    </div>
    <div class="child_comments d-flex flex-column mb-3" id="child_${commentInfo.id}"></div>
  `
  comments.prepend(comment);

  $("#reply_" + commentInfo.id).click(clickBtnReply);
}

/** Add child comment to comments div.*/
function addChildComment(commentInfo) {
  const comment = `
    <div class="child_comment d-flex flex-column">
      <div class="d-flex align-items-center mb-1">
        <img src="${commentInfo.user_avatar}" alt="" class="author_avatar">
        <div class="d-flex flex-column">
          <span class="author_name">${commentInfo.username}</span>
          <span class="text-muted comment_date">${commentInfo.time}</span>
        </div>
      </div>
      <span class="comment_text">${commentInfo.text}</span>
    </div>
    <div class="reply_to_parent_from_child">
      <button class="btn_reply" data-parent="${commentInfo.parent}"
              id="reply_${commentInfo.parent}">
        &#8627;Reply
      </button>
    </div>
  `
  $("#child_" + commentInfo.parent).append(comment);
  $("#reply_" + commentInfo.parent).click(clickBtnReply);
}

/** Click handler for button reply.*/
function clickBtnReply(event) {
  const target = $(event.target);
  const replyType = target.parent().attr("class");
  const parentId = target.data("parent");

  if (replyType === typeReplyParent)
    addFormChildComment("#parent_" + parentId, parentId);
  else
    addFormChildComment("#child_" + parentId, parentId);
}

/**Remove form for add child comment.*/
function removeFormAddChildComment() {
  lastFormAddChildComment.remove();
  lastFormAddChildComment = undefined;
}
