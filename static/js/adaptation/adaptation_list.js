// Assigning Elements
const request = new Request(csrfToken);

var table = $("#class-datatable");
init();

function init() {
  setupListeners();
  initializeAdaptationDatatables(table, adaptations_list_api_url);
}

function initializeAdaptationDatatables(_table, _adaptations_list_api_url) {
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
    serverSide: true,
    ajax: { url: _adaptations_list_api_url, dataSrc: "" },
    columns: [
      {
        data: "username",
      },

      {
        data: "name_surname",
      },

      {
        data: "university",
      },
      {
        data: "decision_date",
      },

      {
        data: null,
        render: function (data, type, row) {
            if(data.is_closed)  return `<span class="badge badge-warning">Kapatıldı ama tamamlanmadı</span>`;
            else return `<span class="badge badge-danger">Tamamlanmadı</span>`;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
          return `
            <div class="row">
            <button class='btn btn-success compare_class_button mx-auto'  data-id="${data.id}"><i class='text-white fas fa-door-open'></i>&nbspBaşvuruya Git</button>
            </div>
            `;
        },
      },
    ],
  });
}


function setupListeners() {
}