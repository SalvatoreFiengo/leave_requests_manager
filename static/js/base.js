$(document).ready(function () {
  // init datatable.js
  $('#dataTable').DataTable({
    "paging": false,
    "info": false
  });

});
// init datepicker
$('.datepicker-container').datepicker({
  format: "dd-mm-yyyy",
  startDate: "01-01-2010",
  endDate: "01-12-2050",
  calendarWeeks: false,
  datesDisabled: []
}); 