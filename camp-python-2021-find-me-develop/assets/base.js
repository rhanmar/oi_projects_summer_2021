const chatNotificationSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/dialog-notifications/'
);

chatNotificationSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  if (window.location.pathname !== `/dialogs/dialog/${data.dialog}/`) {
        alert(`There is new message in ${data.title}:\n${data.message}`);
  }
}

chatNotificationSocket.onclose = function (e) {
  console.error('Chat socket closed unexpectedly');
};
