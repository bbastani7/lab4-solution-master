document.addEventListener("DOMContentLoaded", function () {
  var theCTRLs = document.querySelector(".controls");
  var theKeys = theCTRLs.querySelectorAll("[data-key]");
  var theServerURL = "http://localhost:8000/drone_command";
  var COMMAND_STEP = 20;

  function sendCommand(aURL) {
    console.log("drone_command ", aURL);

    fetch(aURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    })
      .then((response) => response.json())
      .then(function (response) {
        //update your UI?
      });
  }

  function formatCommand(aCmd) {
    if (aCmd == "takeoff" || aCmd == "land" || aCmd == "toggle_video" || aCmd == "emergency")
      var theURL = `${theServerURL}/${aCmd}`;
    else
      var theURL = `${theServerURL}/${aCmd}/${COMMAND_STEP}`;

    return theURL;
  }

  theCTRLs.addEventListener(
    "click",
    function (event) {
      var theCmd = event.target.dataset.cmd;
      if (undefined === theCmd) theCmd = event.target.parentNode.dataset.cmd;
      if (undefined != theCmd) {
        sendCommand(formatCommand(theCmd));
      }
    },
    false
  );

  //listen for keyboard events, and fire assoc. cmd...
  document.addEventListener("keyup", (event) => {
    var theKey = event.key;
    theKeys.forEach(function (theElem) {
      if (theKey == theElem.dataset.key) {
        var theCmd = theElem.dataset.cmd;
        sendCommand(formatCommand(theCmd));
      }
    });
  });
});