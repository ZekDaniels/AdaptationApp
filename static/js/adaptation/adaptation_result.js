// Assigning Elements
const request = new Request(csrfToken);

const show_content_button_selector =".show_content_button";
const finish_adaptation_button_selector ="#finish_adaptation_button";

const activate_button = $("#activate_button");
const deactivate_button = $("#deactivate_button");

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

$(semester_dropdowns_selector).on("click", function(){
  let semester = $(this).data("semester");
  semesterTable = $(`#semester-table-${semester}`);
  semesterTable.slideToggle();
});

$(show_content_button_selector).on("click", function(){
  let id = $(this).data("id");
  getAdaptationClassContent(id, adaptation_class_detail_api_url, AdaptationClassContentModal)
});

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
        "name":"code",
        "data": "adaptation_class.code"
      },   
      {
        "name":"class_name",
        "data": "adaptation_class.class_name"
      },    
      {
        "name":"confirmation",
        "data": "adaptation_class.code",
        "render": function ( data, type, row ) {
          if(row.confirmation.exists)
          return `<span class="badge badge-success">Onaylandı</span>`;
          else 
          return `<span class="badge badge-danger">Reddedildi</span>`;
        }
      },
    ],
    "rowsGroup": [
      "confirmation:name",
      "code:name",
      "class_name:name"
    ]
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