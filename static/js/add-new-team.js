$(document).ready(function () {
    // add a new user card based on users already present

    $('#add_user').click(function (event) {
        event.preventDefault();
        const node = $('#user_container input.form-control').last().attr('name');
        const lastNode = $('#user_container div').hasClass('last-node');
        if (node === undefined) return;
        if (lastNode) return;

        const lastNumber = parseInt(node.slice(-1));
        const lastTwoNumbers = parseInt(node.slice(-2));

        let nextInput = isNaN(lastTwoNumbers) ? lastNumber : lastTwoNumbers;
        nextInput = nextInput + 1;
        if (nextInput === 51) {
            const error = `<div class="input-group mt-2"><div class="last-node text-danger">Reached user quota for this team</div></div>`;
            $('#user_container')
                .append(error);
        }
        else {
            const user = `<div class="mt-3" id="` + nextInput + `">
                            <hr>
                            <div class="form-row my-1">
                                <div class="col-md-6">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <div id="remove-user-`+ nextInput + `" class="input-group-text">
                                                <i class="fas fa-minus"></i>
                                            </div>
                                        </div>
                                        <input class="form-control" type="text" id="name_`+ nextInput + `" name="name_` + nextInput + `" placeholder="Name ` + nextInput + `" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <div class="input-group-text">
                                                <i class="far fa-user"></i>
                                            </div>
                                        </div>
                                        <input class="form-control" type="text" id="surname_`+ nextInput + `" name="surname_` + nextInput + `" placeholder="Surname ` + nextInput + `" required>
                                    </div>
                                </div>
                            </div>
                            <div class="form-row my-1">
                                <div class="col-md-6">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <div  class="input-group-text">
                                                <i class="fas fa-at"></i>
                                            </div>
                                        </div>
                                        <input class="form-control" type="email" id="email_`+ nextInput + `" name="email_` + nextInput + `" placeholder="Email ` + nextInput + `" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <div  class="input-group-text">
                                                <i class="fas fa-user-tie"></i>
                                            </div>
                                        </div>    
                                        <select class="form-control mr-3" name="role_`+ nextInput + `" id="role_` + nextInput + `">
                                            <option default value="Agent">Pick a role</option>
                                            <option value="Agent">Agent</option>
                                            <option value="Team Lead">Team Lead</option>
                                            <option value="Manager">Manager</option>
                                        </select>
                                        <div class="form-check ml-2 mb-2">
                                            <input class="form-check-input" name="checkuser_`+ nextInput + `" type="checkbox" id="supervisor_checkbox_` + nextInput + `">
                                            <label class="form-check-label" for="supervisor_checkbox_`+ nextInput + `">Supervisor</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
            const newUserId = "#" + nextInput;
            const removeId = "#remove-user-" + nextInput;
            $('#user_container')
                .append(user);
            $(removeId).on('click', function () {
                $('div' + newUserId).remove();
            });
        }
        $('#user_container').on(
            {
                mouseenter: function () {
                    $(this).find('i.fa-minus').parent().addClass('bg-danger text-white');
                }, mouseleave: function () {
                    $(this).removeClass('bg-danger text-white');
                }
            }, ".input-group-text");
    });

});