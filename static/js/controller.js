
$(document).ready(function () {
    // handling focus on controller nav
    $("#leave_request_menu").click(function () {
        $(this).addClass("active");
        $("#leave_request").removeClass("d-none");
        $("#manage_team,#manage-bin").addClass("d-none");

    });
    $("#manage_team_menu").click(function () {
        $(this).addClass("active");
        $("#leave_request,#manage-bin").addClass("d-none");
        $("#manage_team").removeClass("d-none");
    });
    $("#bin").click(function () {
        $(this).addClass("active");
        $("#manage_team, #leave_request").addClass("d-none");
        $("#manage-bin").removeClass("d-none");
    });
    // changing form action in approval choice and team select if click on edit
    $('#edit_team').click(function (event) {
        event.preventDefault();
        const action = $('#modal_approval_choice').attr('action');

        $('#modal_approval_choice').attr('action', action + "/edit_team");

        $('#team_select').change(function () {
            $('#modal_approval_choice').attr('action', action + "/edit_team");
        });
    });
});