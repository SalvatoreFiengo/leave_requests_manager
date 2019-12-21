$(document).ready(function () {
  // handling modal hide/show effect instead of having 2 modals
  $('.confirmation').hide();

  $('.modal').on('shown.bs.modal', function () {
    const modal_id = '#' + $(this).attr('id');
    $(modal_id + ' button.approve,' + modal_id + ' button.reject,' + modal_id + ' button.delete').off().on('click', function (event) {
      event.preventDefault();
      let value = "";
      value = $(this).val();
      $('input.input_approval').attr('value', value);

      $('.modal-body.modal_approval_choice').hide();
      $('.confirmation').show();
      $('button.approval_submit').off().on('submit', function (event) {
        event.preventDefault();
      });
    });
  });

  $('button.modal_back_to_choice').click(function () {
    $('.confirmation').hide();
    $('.modal-body.modal_approval_choice').show();
  });

});
