// Assigning Elements
const request = new Request(csrfToken);


const update_class_button_selector = ".update_class_button";
const delete_class_button_selector = ".delete_class_button";
const show_content_button_selector =".show_content_button";
const finish_adaptation_button_selector ="#finish_adaptation_button";

const semester_dropdowns_selector = ".toggle-semester-table";

const university_input = $("#id_university");
const faculty_input = $("#id_faculty");
const science_input = $("#id_science");
const turkish_content = $("#turkish-content");
const english_content = $("#english-content");

const mainForm = $("#mainForm");
const addClassForm = $("#addClassForm");

const addClassModal = $("#addClassModal");
const deleteClassModal = $("#deleteClassModal");
const AdaptationClassContentModal = $("#AdaptationClassContentModal");

const main_submit_button = $("#main_submit_button");
const add_class_button = $("#add_class_button");
const finish_adaptation_button = $(finish_adaptation_button_selector);

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

// Variables
var table = $("#class-datatable");
let updateable_class_id = null;
let updateable = false;

init();

function init() {
  setupListeners();
  initializeStudentClassDatatables(table, student_classes_list_api_url, adaptation_id)
}

function clearAddClassForm() {
  $("#addClassForm input").val(''); 
  $("#addClassForm textarea").val(''); 
  $("#addClassForm select").val(''); 
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
    formData.append("adaptation", adaptation_id);
    let data = Object.fromEntries(formData.entries());

    if (updateable)
    updateStudentClass(updateable_class_id, data, student_class_update_api_url, add_class_button, table, addClassModal);
    else
    addStudentClass(data, student_class_create_api_url, add_class_button, table, addClassModal);

    updateable = false;
  });
 
}


//jQuery events

$('tbody').on("click", '.delete_class_button', function () {
  let deleteable_class_id = $(this).data('id');
  DeleteStudentClass(deleteable_class_id, student_class_update_api_url, table);
});

$('tbody').on("click", '.update_class_button', function (event) {
  updateable_class_id = $(this).data('id');
  updateable = true;
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  FillDataAddClassForm(data);
});

$(semester_dropdowns_selector).on("click", function(){
  let semester = $(this).data("semester");
  semesterTable = $(`#semester-table-${semester}`);
  semesterTable.slideToggle();
});

$(show_content_button_selector).on("click", function(){
  let id = $(this).data("id");
  getAdaptationClassContent(id, adaptation_class_detail_api_url, AdaptationClassContentModal)
});
$(finish_adaptation_button_selector).on("click", function(){
  data = { 'is_closed': true };
  finishAdaptation(adaptation_id, data, adaptation_update_api_url, finish_adaptation_button);
});




//Adaptation Activies
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

function UpdateAdaptation(_data, _url, _button = null, _table = null, _modal = null) {
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
          if (_modal) {
            _modal.modal('hide');
          }
        })
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function finishAdaptation(_id,_data, _url, _button = null) {
  sweetCombineDynamic(
    "Emin misin?",
    "Bu intibak başvurusunu bitirmek istediğine emin misin!",
    "success",
    "Başvuruyu bitir.",
    "İptal et.",
    () => {
      request
      .patch_r(_url.replace("0", _id), _data).then((response) => {
        if (response.ok) {
          response.json().then(data => {
            console.log(_button);
            _button.prop("disabled", true);
          });
        } else {
          response.json().then(errors => {
            console.log(errors);
            fire_alert([{
              message: errors,
              icon: "error"
            }]);
          })
          throw new Error('Something went wrong');
        }
      });
    }
    
  );
}


//Classes Activies
function initializeStudentClassDatatables(_table, _student_classes_list_api_url, _adaptation_id) {
  $.extend($.fn.dataTable.defaults, {
    autoWidth: false,
    dom: '<"datatable-header"fBl><"datatable-scroll-wrap"t><"datatable-footer"ip>',
    language: {
      search: "<span>Filter:</span> _INPUT_",
      searchPlaceholder: "Type to filter...",
      lengthMenu: "<span>Show:</span> _MENU_",
      paginate: {
        first: "First",
        last: "Last",
        next: $("html").attr("dir") == "rtl" ? "&larr;" : "&rarr;",
        previous: $("html").attr("dir") == "rtl" ? "&rarr;" : "&larr;",
      },
    },
  });
  table = _table.DataTable({
    "searchCols": [
      null,
      {
        "search": _adaptation_id
      },
    ],
    "serverSide": true,
    "ajax": {"url":_student_classes_list_api_url,"dataSrc":""},
    "columns": [
      {
        "data": "code"
      },
      
      {
        "data": "class_name"
      },
      
      {
        "data": "semester"
      },
      // {
      //   "data": "teorical"
      // },
      // {
      //   "data": "practical"
      // },
      // {
      //   "data": "sum"
      // },
      {
        "data": "credit"
      },
      
      {
        "data": "akts"
      },
      {
        "data": null,
        "render": function ( data, type, row ) {
          console.log(data)
          return `
          <div class="row">
          <button class='btn update_class_button p-0 mx-auto'  data-toggle="modal" data-target="#addClassModal" data-id="${data.id}"><i class='text-warning fas fa-edit'></i></button>
          <button class='btn delete_class_button p-0 mx-auto' data-id="${data.id}"><i class='text-danger fas fa-trash'></i></button>
          </div>
          `;
        }
      },
      {
        "name":"code",
        "data":"adaptation_class.code"
      },
      {
        "name":"class_name",
        "data":"adaptation_class.class_name"
      },
      {
        "name":"semester",
        "data":"adaptation_class.semester"
      },  
      // {
      //   "data": "adaptation_class.teorical"
      // },
      // {
      //   "data": "adaptation_class.practical"
      // },
      // {
      //   "data": "adaptation_class_sum"
      // },
      {
        "name":"credit",
        "data":"adaptation_class.credit"
      },   
      {
        "name":"akts",
        "data":"adaptation_class.akts"
      },
      {
        "name":"max_grade",
        "data":"max_grade"
      },
          
     
    ],
    "rowsGroup": [
      "code:name",
      "class_name:name",
      "semester:name",
      "credit:name",
      "akts:name",
      "max_grade:name",
    ],
  });
}

function getAdaptationClassContent(_id, _url, _modal = null) {
  request
    .get_r(_url.replace("0", _id))
    .then((response) => {
      if (response.ok) {
        response.json().then(data => {
          fillAdaptationClassContent(data);
        })
      } else {
        response.json().then(errors => {
          fire_alert([{ message: errors, icon: "error" }]);
        })
        throw new Error('Something went wrong');
      }
    })
}

function fillAdaptationClassContent(_data) {
  turkish_content.html(_data.turkish_content);
  english_content.html(_data.english_content);
}

function addStudentClass(_data, _url, _button = null, _table = null, _modal = null) {

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
          _table.ajax.reload();
          clearAddClassForm();
          if (_modal) {
            _modal.modal('hide');
          }
        })
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}

function updateStudentClass(_id, _data, _url, _button = null, _table = null, _modal = null) {

  let button_text = ""
  if (_button) {
    button_text = _button.html();
    _button.prop("disabled", true);
    _button.html(`<i class="icon-spinner2 spinner"></i>`);
  }
  request
    .put_r(_url.replace("0", _id), _data).then((response) => {
      if (_button) {
        _button.html(button_text);
        _button.prop("disabled", false);
      }
      if (response.ok) {
        response.json().then(data => {
          _table.ajax.reload();
          clearAddClassForm();
          if (_modal) {
            _modal.modal('hide');
          }
        })
      } else {
        response.json().then(errors => {
          console.log(errors);
          fire_alert([{
            message: errors,
            icon: "error"
          }]);
        })
        throw new Error('Something went wrong');
      }
    });
}


function DeleteStudentClass(_id, _url, _table = null) {
  sweetCombineDynamic(
    "Emin misin?",
    "Bu dersi silmek isdtediğine emin misin!",
    "warning",
    "Kaydı sil.",
    "İptal et.",
    () => {
      request
        .delete_r(_url.replace("0", _id))
        .then((response) => {
          if (response.ok) {
            if (_table) {
              _table.ajax.reload()
            }
          } else {
            response.json().then(errors => {
              fire_alert([{ message: errors, icon: "error" }]);
            })
            throw new Error('Something went wrong');
          }
        })
    },
    "saddas"
  );
}

function FillDataAddClassForm(_data) {
  _data['grade'] = _data['grade'].toFixed(1);
  $.each( _data, function( key, value ) {     
    $(`#id_${key}`).val(value);
  });
  $(`#id_adaptation_class`).val(_data.adaptation_class.id);
}
