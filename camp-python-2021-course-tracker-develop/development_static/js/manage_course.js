$(document).ready(function() {
  const btnBecomeSpeakerIdPrefix = "topic_";
  const dayDeltaValIdPrefix = "day_delta_";
  const actionNext = "next";

  $(".btn_become_speaker").click(function (event) {
    const target = $(event.target);
    const topicId = target.attr("id").slice(btnBecomeSpeakerIdPrefix.length);
    $("#topic_id_for_speaker").val(topicId);
    $("#form_become_speaker").submit();
  });

  $(".btn_reschedule_topic").click(function (event) {
    const target = $(event.target);
    const topicId = target.data("topicId");
    let dayDelta = parseInt($("#" + dayDeltaValIdPrefix + topicId).val());
    if (dayDelta < 1) dayDelta = 1;
    else if (dayDelta > 5) dayDelta = 5;
    $("#topic_id_for_reschedule").val(topicId);
    $("#id_day_delta").val(dayDelta);
    $("#form_reschedule_topic").submit();
  });
});
