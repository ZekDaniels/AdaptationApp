// Assigning Elements
const request = new Request(csrfToken);

const show_content_button_selector =".show_content_button";
const finish_adaptation_button_selector ="#finish_adaptation_button";

const semester_dropdowns_selector = ".toggle-semester-table";

const turkish_content = $("#turkish-content");
const english_content = $("#english-content");

const AdaptationClassContentModal = $("#AdaptationClassContentModal");


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

init();

function init() {
  setupListeners();
  initializeStudentClassDatatables(table, student_classes_list_api_url, adaptation_id)
}

function clearAddClassForm() {
  $("#addClassForm input").val(''); 
  $("#addClassForm textarea").val(''); 
  $("#addClassForm select").val(''); 
  add_class_button.html("Ders Ekle");
  add_class_modal_label.html("Ders Ekle");
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

 
}


//jQuery events


$('tbody').on("click", '.compare_class_button', function (event) {
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  if (data){
    FillDataCompareClassModal(data);
  }
  
});

$('tbody').on("click", '.confirm_class_button', function (event) {
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  if (data){
    disconfirm_data = { 'is_confirmed': true };
    updateStudentClass(data.id, disconfirm_data, student_class_confirmation_api_url, $(this), table);
  }
  
});

$('tbody').on("click", '.disconfirm_class_button', function (event) {
  let row = $(this).closest("tr");
  let data = table.row(row).data();
  if (data){
    disconfirm_data = { 'is_confirmed': false };
    updateStudentClass(data.id, disconfirm_data, student_class_confirmation_api_url, $(this), table);
  }
  
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

$(addClassModal).on('hidden.bs.modal', function () {
  clearAddClassForm();
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
      {
        "data": "teorical"
      },
      {
        "data": "practical"
      },
      {
        "data": "sum"
      },
      {
        "data": "credit"
      },
      
      {
        "data": "akts"
      },
      {
        "data": null,
        "render": function ( data, type, row ) {
            return `
            <div class="row">
             <button class='btn btn-primary compare_class_button mx-auto'  data-toggle="modal" data-target="#compareClassModal" data-id="${data.id}">Karşılaştır</button>
            </div>
          `;
        }
      },
      {
        "data": null,
        "render": function ( data, type, row ) {
          if(data.is_confirmed)
          return `
          <div class="row">
            <button class='btn disconfirm_class_button p-0 mx-auto' "><i class='text-danger fas fa-times m-1'></i></button>
            <button class='btn confirm_class_button p-0 mx-auto border border-success' " disabled><i class='text-success fas fa-check m-1'></i></button>
          </div>
          `;

          else 
          return `
          <div class="row">
            <button class='btn disconfirm_class_button p-0 mx-auto border border-danger' " disabled><i class='text-danger fas fa-times m-1'></i></button>
            <button class='btn confirm_class_button p-0 mx-auto' "><i class='text-success fas fa-check m-1'></i></button>
          </div>
          `;
        }
      },
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
          console.log(data);
          _table.ajax.reload();
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



function FillDataCompareClassModal(_data) {
  _data.grade = Number(_data.grade).toFixed(1);
  $.each( _data, function( key, value ) {     
    $(`.table-compare #id_${key}`).val(value);
  });
  $.each( _data.adaptation_class, function( key, value ) {     
    $(`.table-compare #id_${key}_adaptation_class`).val(value);
  });
  $(`#id_adaptation_class`).val(_data.adaptation_class.id);
}
