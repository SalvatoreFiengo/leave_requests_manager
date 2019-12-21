$(document).ready(function () {
    // check validity based on dates provided and if reason has been selected (not default)
    function checkValidity() {
        const dateFrom = $('#from').val();
        const dateTo = $('#to').val();
        const dateError = $('#date-error');
        const selectedError = $('#select-error');
        if (dateFrom == "" && dateTo == "") {
            let error = `<p id="no-dates" class="text-warning">Select dates please</p>`;
            $('#submit-button').attr('disabled', true);
            $('#submit-button').after(error);
        } else {
            $('#no-dates').remove();
        }
        if (dateError.hasClass('text-warning')) {
            $('#submit-button').attr('disabled', true);
        } else if (dateError.hasClass('text-danger')) {
            $('#submit-button').attr('disabled', true);
        } else if (selectedError.hasClass('text-danger')) {
            $('#submit-button').attr('disabled', true);
        } else {
            $('#submit-button').attr('disabled', false);
        }
    }

    checkValidity();
    // handling validity errors separately from checkValidity
    $('#from, #to').on('change', function () {
        let def = $.Deferred();
        const dateFrom = $('#from').val();
        const dateTo = $('#to').val();
        const fromArray = dateFrom.replace(/-/g, ',').split(",");
        const toArray = dateTo.replace(/-/g, ',').split(",");
        const _from = new Date(fromArray[2], fromArray[1], fromArray[0]).valueOf();
        const _to = new Date(toArray[2], toArray[1], toArray[0]).valueOf();
        let error = `<p id="date-error" class="text-danger">'From' is greater than 'To'. please check selected dates</p>`;
        if (_from <= _to && (!isNaN(_from) && !isNaN(_to))) {
            $('#date-error').remove();
            def.resolve();

        } else if (isNaN(_from) || isNaN(_to)) {
            error = `<p id="date-error" class="text-warning">Please select one more date</p>`;
            $('#date-error').remove();
            $('#submit-button').after(error);
            def.resolve();

        }
        else {
            $('#date-error').remove();
            $('#submit-button').after(error);
            def.resolve();

        }
        def.done(function () { checkValidity(); });
    });
    if ($('#reason').val() == 'Select Reason') {
        let error = `<p id="select-error" class="text-danger">Reason not selected</p>`;
        $('#select-error').remove();
        $('#reason').after(error);

    }
    $('#reason').change(function () {
        let error = `<p id="select-error" class="text-danger">Reason not selected</p>`;
        const def = $.Deferred();
        if ($(this).val() == 'Select Reason') {
            $('#select-error').remove();
            $('#reason').after(error);
            def.resolve();

        } else {
            $('#select-error').remove();
            def.resolve();

        }
        def.done(function () { checkValidity(); });
    });

});