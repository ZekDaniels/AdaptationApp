// Defaults
var swalInit = swal.mixin({
  buttonsStyling: false,
  customClass: {
    confirmButton: "btn m-1 btn-primary",
    cancelButton: "btn m-1 btn-light",
    denyButton: "btn m-1 btn-light",
    input: "form-control",
  },
});

// === BASIC ===

// ---Alert message -- notification type
function sweetType(title, text, type) {
  swalInit.fire({
    title: title,
    text: text,
    icon: type,
  });
}

// Combine messages
// ---Message with a function attached to the "Confirm" and "Cancel" buttons
function sweetCombine(
  title,
  text,
  type,
  confirmButtonText,
  cancelButtonText,
  success,
  succesMessageTitle,
  succesMessageText,
  succesMessageType,
  error,
  errorMessageTitle,
  errorMessageText,
  errorMessageType
) {
  swalInit
    .fire({
      title: title,
      text: text,
      icon: type,
      showCancelButton: true,
      confirmButtonText: confirmButtonText,
      cancelButtonText: cancelButtonText,
      confirmButtonClass: "btn m-1 btn-success",
      cancelButtonClass: "btn m-1 btn-danger",
      buttonsStyling: false,
    })
    .then(function (result) {
      if (result.value) {
        swalInit.fire(succesMessageTitle, succesMessageText, succesMessageType);
        success();
      } else if (result.dismiss === swal.DismissReason.cancel) {
        swalInit.fire(errorMessageTitle, errorMessageText, errorMessageType);
        error();
      }
    });
}

// === TOASTS ===

// ---Alert message -- toasts type
function sweetToastType(text, type) {
  swalInit.fire({
    text: text,
    icon: type,
    toast: true,
    showConfirmButton: false,
    timer: 4000,
    position: "bottom-right",
  });
}
// === INPUTS ===

// ---Alert message -- toasts type
function sweetInputType(title, type, placeholder, rensponseType, responseHTML) {
  swalInit
    .fire({
      title: title,
      input: type,
      inputPlaceholder: placeholder,
      showCancelButton: true,
      inputClass: "form-control",
    })
    .then(function (result) {
      if (result.value) {
        swalInit.fire({
          type: rensponseType,
          html: responseHTML,
          //   html: "Hi, " + result.value,
        });
      }
    });
}

const fire_alert = function (_messages) {
  let modals = []
  for (let modal of _messages) {
    modals.push(get_alert(modal))
  }

  let first_alert = swalInit.fire(modals[0])
  for (let i = 1; i < modals.length; i++) {
    first_alert = first_alert.then(function () {
      swalInit.fire(modals[i])
    })
  }
}

const get_alert = function (_modal) {
  let texts = [];
  for (var key of Object.keys(_modal.message)) {
    if ($(`[name='${key}']`).length) {
      let name = key.replaceAll('_', ' ')
      if (Array.isArray(_modal.message[key])) {
        texts.push(`<span class="font-weight-bold text-capitalize">${name}:</span>`);
        for (let text of _modal.message[key]) {
          texts.push(`<span>${text}</span><br>`)
        };
      } else {
        texts.push(`<span class="font-weight-bold text-capitalize">${name}:</span> <span>${_modal.message[key]}</span><br>`);
      }
    } else {
      if (Array.isArray(_modal.message[key])) {
        for (let text of _modal.message[key]) {
          if(key  ==  'non_field_errors')  texts.push(`<span>${text}</span><br>`);    
          else texts.push(`<span><b class='font-weight-bold'>${key}:</b> ${text}</span><br>`);         
        };
      } else {
        texts.push(`<span>${_modal.message[key]}</span>`);
      }
    }
  }
  return {
    html: texts.join("<br>"),
    icon: _modal.icon ? _modal.icon : "error",
    toast: _modal.toast ? true : false,
    showConfirmButton: _modal.toast ? false : true,
    position: _modal.position ? _modal.position : (_modal.toast ? "bottom-right" : null)
  }
}

// Combine messages
// ---Message with a function attached to the "Confirm" and "Cancel" buttons
// with dynamic conditions
const sweetCombineDynamic = function (
  title,
  text,
  type,
  confirmButtonText,
  cancelButtonText,
  success = null,
  succesMessageTitle = null,
  succesMessageText = null,
  succesMessageType = null,
  error = null,
  errorMessageTitle = null,
  errorMessageText = null,
  errorMessageType = null
) {
  swalInit
    .fire({
      title: title,
      text: text,
      icon: type,
      showCancelButton: true,
      confirmButtonText: confirmButtonText,
      cancelButtonText: cancelButtonText,
      confirmButtonClass: "btn m-1 btn-success",
      cancelButtonClass: "btn m-1 btn-danger",
      buttonsStyling: false,
    })
    .then(function (result) {
      if (result.value) {
        if (succesMessageTitle && succesMessageText && succesMessageType) swalInit.fire(succesMessageTitle, succesMessageText, succesMessageType);
        if (success) success();
      } else if (result.dismiss === swal.DismissReason.cancel) {
        if (errorMessageTitle && errorMessageText && errorMessageType) swalInit.fire(errorMessageTitle, errorMessageText, errorMessageType);
        if (error) error();
      }
    });
}