// Assigning Elements
const request = new Request(csrfToken);

let university_input = $("#id_university");
let faculty_input = $("#id_faculty");
let science_input = $("#id_science");
let mainForm = $("#mainForm")
let submit_button = $("#mainForm button[type='submit']");
const custom_record = $("#custom_record");

let university = null;
let faculty = null;
let science = null;

const cleanOptions = function (select_input , callback=null) {
  select_input.find("option").each(function () {
    $(this).removeAttr("selected");
    $(this).removeAttr("data-select2-id");
    if ($(this).val()) {
      $(this).remove();
    }
  });

  if (callback) {
    callback();
  }
};
const fillOptions = function (select_input, data, callback = null) {
  // get already selected value
  // to select it with new option list

  cleanOptions(select_input);


  for (option of data) {
    $(select_input).append($('<option>', {
      value: option.id,
      text: option.name
    }));
  }
  if (callback) {
    callback();
  }
};

init();

function init() {
  updateFaculties();
  setupListeners();
}

function getSelectionText() {
  if (window.getSelection) {
    try {
      var activeElement = document.activeElement;
      if (activeElement && activeElement.value) {
        // firefox bug https://bugzilla.mozilla.org/show_bug.cgi?id=85686
        return activeElement.value.substring(activeElement.selectionStart, activeElement.selectionEnd);
      } else {
        return window.getSelection().toString();
      }

    } catch (e) {}
  } else if (document.selection && document.selection.type != "Control") {
    // For IE
    return document.selection.createRange().text;
  }
}

//Adaptation Activies
function fillUniversities() {
  fetch(university_list_api_url)
  .then((response) => response.json())
  .then((data) => {
    $("#id_university").append($('<option>', {
      value: "",
      text:"---------"
    }));
    for (option of data) {
      $("#id_university").append($('<option>', {
        value: option.id,
        text: option.name
      }));
    }
    
  });
}

function updateFaculties() {
  new_value = getSelectionText(university_input)
  if (!new_value) {
    cleanOptions(faculty_input);
  } else {
    urlParams = new URLSearchParams();
    urlParams.set("university", new_value);
    faculty_list_api_url.search = urlParams;
    fetch(faculty_list_api_url)
      .then((response) => response.json())
      .then((data) => fillOptions(faculty_input, data, cleanOptions(science_input)))
  }
}

function updateSciences() {
  new_value = getSelectionText(university_input)
  new_value_faculty = getSelectionText(faculty_input)
  if (!new_value) {
    cleanOptions(science_input);
  } else {
    urlParams = new URLSearchParams();
    urlParams.set("faculty", new_value);
    science_list_api_url.search = urlParams;
    fetch(science_list_api_url)
      .then((response) => response.json())
      .then((data) => fillOptions(science_input, data))
  }
}

function setupListeners() {
  university_input.change(() => {
    updateFaculties();
  });
  faculty_input.change(() => {
    updateSciences();
  });
  mainForm.submit(function (event) {
    event.preventDefault();
    let formData = new FormData(this);
    formData.append("is_unrecorded", is_unrecorded);
    let data = Object.fromEntries(formData.entries());
    let button = $(this).find("button[type='submit']").first();
    createAdaptation(data, adaptation_create_api_url, button);
  });
}

function createAdaptation(_data, _url, _button) {
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .post_r(_url, _data).then((response) => { // https://stackoverflow.com/a/38236296/14506165
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          location.reload();
        })
      } else {
        response.json().then(errors => {
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}


$(custom_record).on("click", function(event){
  event.preventDefault();
  is_unrecorded = !is_unrecorded;
  if (is_unrecorded){
    context = {}
    context['university_div'] =
    `
    <label>Üniversite</label>
    <input type="text" name="university_unrecorded" value="" maxlength="255" class="form-control" id="id_university_unrecorded">
    `;

    context['faculty_div'] =
    `
    <label>Fakülte</label>
    <input type="text" name="faculty_unrecorded" value="" maxlength="255" class="form-control" id="id_faculty_unrecorded">
    `;

    context['science_div'] =
    `
    <label>Bölüm</label>
    <input type="text" name="science_unrecorded" value="" maxlength="255" class="form-control" id="id_science_unrecorded">
    `;

    $.each( context, function( key, value ) {     
      $(`#${key}`).html(value);
    });

  }
  else {

    context = {}
    context['university_div'] =
    `<label>Üniversite</label>
    <select name="university" class="form-control" id="id_university">
    </select>`
    context['faculty_div'] =
    `<label>Fakülte</label>
    <select name="faculty" class="form-control" id="id_faculty">
      <option value="">---------</option>
    </select>`
    context['science_div'] =
    `<label>Bölüm</label>
    <select name="science" class="form-control" id="id_science">
      <option value="">---------</option>
    </select>`

    $.each( context, function( key, value ) {     
      $(`#${key}`).html(value);
    });
    
    fillUniversities();
    university_input = $("#id_university");
    faculty_input = $("#id_faculty");
    science_input = $("#id_science");
    
    university_input.change(() => {
      updateFaculties();
    });
    faculty_input.change(() => {
      updateSciences();
    });
    
  }
});