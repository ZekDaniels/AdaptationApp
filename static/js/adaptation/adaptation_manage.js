// Assigning Elements
const request = new Request(csrfToken);

const university_input = $("#id_university");
const faculty_input = $("#id_faculty");
const science_input = $("#id_science");
const mainForm = $("#mainForm")
const addClassForm = $("#addClassForm")
const main_submit_button = $("#main_submit_button");
const add_class_button = $("#add_class_button");

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
  main_submit_button.click(function (event) {
    mainForm.submit();
  });
  add_class_button.click(function (event) {
    addClassForm.submit();
  });
  mainForm.submit(function name(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());
    UpdateAdaptation(data, adaptation_update_api_url, main_submit_button);
  });
  addClassForm.submit(function name(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let data = Object.fromEntries(formData.entries());
    console.log(data);  
    addStudentClass(data, student_class_create_api_url, add_class_button);
  });
}

function UpdateAdaptation(_data, _url, _button) {
  console.log("asdss")
  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .put_r(_url.replace("0", adaptation_id), _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          fire_alert([{
            message: {message:"Kaydınız başarıyla güncellendi"},
            icon: "success"
          }]);
        })
      } else {
        response.json().then(errors => {
          console.log(errors)
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function addStudentClass(_data, _url, _button) {
  console.log(_data);  

  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .post_r(_url, _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          console.log(data);
        })
      } else {
        response.json().then(errors => {
          console.log(errors)
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function buildClass() {
  
}