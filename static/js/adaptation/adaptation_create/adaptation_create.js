// Assigning Elements
let university_input = $("#id_university");
let faculty_input = $("#id_faculty");
let science_input = $("#id_science");

const cleanOptions = function (select_input) {
  select_input.find("option").each(function () {
    $(this).removeAttr("selected");
    $(this).removeAttr("data-select2-id");
    if ($(this).val()) {
      $(this).remove();
    }
  });
};
const fillOptions = function (select_input, data, callback = null) {
  // get already selected value
  // to select it with new option list
  
  cleanOptions(select_input);


  for (option of data) {
    console.log(option)
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

      } catch (e) {
      }
  } else if (document.selection && document.selection.type != "Control") {
      // For IE
      return document.selection.createRange().text;
  }
}
function updateFaculties() {
    new_value = getSelectionText(university_input)
    if (!new_value) {
      cleanOptions(faculty_input);
    } else {
      urlParams = new URLSearchParams();
      urlParams.set("university", new_value);
      faculties_api_url.search = urlParams;
      fetch(faculties_api_url)
        .then((response) => response.json())
        .then((data) => fillOptions(faculty_input, data))
    }
}

function updateSciences() {
    new_value = getSelectionText(science_input)
    if (!new_value) {
      cleanOptions(science_input);
    } else {
      urlParams = new URLSearchParams();
      urlParams.set("faculty", new_value);
      sciences_api_url.search = urlParams;
      fetch(sciences_api_url)
        .then((response) => response.json())
        .then((data) => fillOptions(science_input, data))
    }
}
function setupListeners(){
    university_input.change(() => {
      updateFaculties();
    });
    faculty_input.change(() => {
      updateSciences();
    });
}