/* GLOBALS */
// Response message
const _message = document.querySelector("#message");

/* Handle Login */
// Data from login input form
const loginForm = document.querySelector("#loginForm");
// Login function
async function login() {
  let response = await fetch("/login", {
    method: "POST",
    body: new FormData(loginForm),
  });
  const result = await response.json();

  _message.innerHTML = result.detail;

  setTimeout(redirectToProfile, 1000);
}

/* Redirect functions */
function redirectToProfile() {
  location.href = "/profile";
}

function redirectToLogin() {
  location.href = "/";
}

/* ------------------------------------------------------------------------------------------------------- */
/* Handle GET requests from FormData to JSON */
// get secret key on email
function getKey() {
  const user = document.getElementById("user-id").value;
  fetch("/get_key/" + user, {
    method: "GET",
  }).then((response) => {
    if (response.redirected) {
      window.location.href = response.url;
    } else {
      window.location.href = "/";
    }
  });
}

/* Handle POST requests from FormData to JSON */
// Event handler for form submit event that MUST include action URL and type="submit" button

async function handlePostFormSubmit(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const url = form.action;

  try {
    const formData = new FormData(form);
    responseData = await postFormDataAsJson({ url, formData });
  } catch (error) {
    responseData = error;
  }

  _message.innerHTML = responseData.detail;

  setTimeout(() => {
    _message.innerHTML = "";
  }, 3000);
  location.reload();
}
// Helper function for Posting data
async function postFormDataAsJson({ url, formData }) {
  const plainFormData = Object.fromEntries(formData.entries());
  const formDataJsonString = JSON.stringify(plainFormData);

  const fetchOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: formDataJsonString,
  };

  const response = await fetch(url, fetchOptions);
  console.log(response);

  if (!response.ok) {
    const errorMessage = await response.json();
    throw errorMessage;
  }

  return response.json();
}

/* ------------------------------------------------------------------------------------------------------- */

/* Post events from FormData */
// User registration
const signUpForm = document.getElementById("signUpForm");
if (signUpForm) {
  signUpForm.addEventListener("submit", handlePostFormSubmit);
}
// Create new system
const addSystem = document.querySelector("#addSystem");
if (addSystem) {
  addSystem.addEventListener("submit", handlePostFormSubmit);
}
// Create new pump
const addPump = document.querySelector("#addPump");
if (addPump) {
  addPump.addEventListener("submit", handlePostFormSubmit);
}
// Create new valve
const addValve = document.querySelector("#addValve");
if (addValve) {
  addValve.addEventListener("submit", handlePostFormSubmit);
}
// Create new sensor
const addSensor = document.querySelector("#addSensor");
if (addSensor) {
  addSensor.addEventListener("submit", handlePostFormSubmit);
}
// Create new shift
const addShiftForm = document.getElementById("addShiftForm");
if (addShiftForm) {
  addShiftForm.addEventListener("submit", handlePostFormSubmit);
}

// Create new timer
const addTimerShiftForm = document.getElementById("addTimerShiftForm");
if (addTimerShiftForm) {
  addTimerShiftForm.addEventListener("submit", handlePostFormSubmit);
}

// Subscribing to newsletter
const subscribeForm = document.querySelector("#subscribeForm");
subscribeForm.addEventListener("submit", handlePostFormSubmit);

/* ------------------------------------------------------------------------------------------------------ */
/* Handle DELETE requests */
// General delete request
function deleteRequest(id) {
  fetch("/base/" + id, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 3000);
    });
}

/* ------------------------------------------------------------------------------------------------------- */
/* Handle PATCH requests from FormData to JSON */
// reset users password
function resetPassword() {
  const data = {};
  let password1 = document.getElementById("reset-password").value;
  let password2 = document.getElementById("retype-new-password").value;
  let _message = document.querySelector("#q-message");
  const secret = document.getElementById("secret-key").value;

  if (password1 !== password2) {
    _message.innerHTML = "Passwords doesn't matches. Please check your entry!";

    setTimeout(location.reload(), 8000);
  } else {
    data["password"] = password1;
    data["secret"] = secret;
    console.log(data);

    fetch("reset_password/" + secret, {
      method: "PATCH",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        _message.innerHTML = data.detail;

        setTimeout(redirectToLogin, 3000);
      });
  }
}

/* ------------------------------------------------------------------------------------------------------- */
/* Handle PUT requests from FormData to JSON */
// update user attributes

function adminUpdate(id) {
  const data = {};
  data["delisted"] = document.querySelector(
    'input[name="delisted"]:checked'
  ).value;
  data["premium"] = document.querySelector(
    'input[name="premium"]:checked'
  ).value;
  data["admin"] = document.querySelector('input[name="admin"]:checked').value;

  fetch("/base/admin/" + id, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 3000);
    });
}

function timerShiftUpdate(id) {
  const data = {};
  data["Mon"] = document.getElementById("Mon").checked;
  data["Tue"] = document.getElementById("Tue").checked;
  data["Wed"] = document.getElementById("Wed").checked;
  data["Thu"] = document.getElementById("Thu").checked;
  data["Fri"] = document.getElementById("Fri").checked;
  data["Sat"] = document.getElementById("Sat").checked;
  data["Sun"] = document.getElementById("Sun").checked;
  data["start"] = document.getElementById("start").value;
  data["stop"] = document.getElementById("stop").value;
  data["mode"] = document.getElementById("timer-mode").value;
  console.log(data);

  fetch("/base/shift/" + id, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 3000);
    });
}

function sensorShiftUpdate(id) {
  const data = {};
  data["mode"] = document.getElementById("sensor-mode").value;
  data["sensors_settings"] = document.querySelector(
    'input[name="sensors_settings"]:checked'
  ).value;
  data["turn_on"] = document.getElementById("turn_on").value;
  data["turn_off"] = document.getElementById("turn_off").value;
  console.log(data);

  fetch("/base/shift/" + id, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 3000);
    });
}

/*
const addShiftSensor = document.querySelector(`[id="shift-sensor-id"]`);

addShiftSensor.addEventListener(`change`, (e) => {
  const data = {};
  data["set_lvl_1"] = true;
  data["set_lvl_2"] = true;
  data["set_lvl_3"] = true;
  const select = e.target;
  const value = select.value;
  const sensor_id = select.selectedOptions[0].text;
  data["shift_id"] = value;
  console.log(data);
  console.log(sensor_id);

  fetch("/base/sensor/" + sensor_id, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 1000);
    });
});

const addTimerValve = document.querySelector(`[id="shift-timer-valve-id"]`);

addTimerValve.addEventListener(`change`, (e) => {
  const data = {};
  data["mode"] = "TIMER";
  const select = e.target;
  const value = select.value;
  const valve_id = select.selectedOptions[0].text;
  data["shift_id"] = value;
  console.log(data);
  console.log(valve_id);

  fetch("/base/valve/" + valve_id, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      let _message = document.querySelector("#message");
      _message.innerHTML = data.detail;

      setTimeout(location.reload(), 1000);
    });
});
*/
