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
        data: null,
        render: function (data, type, row) {
            if(data.decision_date) return data.decision_date;
            else return `Karar verilmedi`;
        },
      },

      {
        data: null,
        render: function (data, type, row) {
            if(data.is_closed && data.is_confirmated) return `<span class="badge badge-success">Tamamlandı ve onaylandı</span>`;
            if(data.is_closed)  return `<span class="badge badge-warning">Tamamlandı ama onaylanmadı</span>`;
            else return `<span class="badge badge-danger">Tamamlanmadı</span>`;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
           button_url = adaptation_result_url.replace("0", data.id);
          return `
            <a class='btn btn-sm btn-icon-split ml-auto btn-primary col-lg-12 mx-auto' href="${button_url}"><span class="icon my-auto text-white-50"><i class='text-white fas fa-list-alt'></i></span> <span class="text">Sonuç </span> </a>
            `;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
            button_url = adaptation_basic_pdf_admin_url.replace("0", data.id);
            if(data.is_closed) 
            return `
            <a class='btn btn-sm btn-icon-split ml-auto btn-secondary col-lg-12 mx-auto' href="${button_url}" disabled><span class="icon my-auto text-white-50"><i class='text-white fas fa-download'></i></span> <span class="text"> PDF'e git </span> </a>
            `;
            else
             return `
             <a class='btn btn-sm btn-icon-split ml-auto btn-secondary col-lg-12 mx-auto disabled' href="${button_url}" disabled><span class="icon my-auto text-white-50"><i class='text-white fas fa-download'></i></span> <span class="text"> PDF'e git </span> </a>
            `;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
            button_url = adaptation_complex_pdf_admin_url.replace("0", data.id);
            if(data.is_closed && data.is_confirmated) 
            return `
            <a class='btn btn-sm btn-icon-split ml-auto btn-secondary col-lg-12 mx-auto' href="${button_url}" disabled><span class="icon my-auto text-white-50"><i class='text-white fas fa-download'></i></span> <span class="text"> PDF'e git </span> </a>
            `;
            else
             return `
             <a class='btn btn-sm btn-icon-split ml-auto btn-secondary col-lg-12 mx-auto disabled' href="${button_url}" disabled><span class="icon my-auto text-white-50"><i class='text-white fas fa-download'></i></span> <span class="text"> PDF'e git </span> </a>
            `;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
           button_url = adaptation_manage_url.replace("0", data.id);
          return `         
            <a class='btn btn-sm btn-icon-split ml-auto btn-warning col-lg-12 mx-auto' href="${button_url}"><span class="icon my-auto text-white-50"><i class='text-white fas fa-edit'></i></span> <span class="text"> Düzenle </span> </a>
            `;
        },
      },
    ],
  });
}


function setupListeners() {
}