$(document).ready(function() {
    if ($('#id_authorization').is(':checked')) {
        $('#id_amount').prop('readonly', true);
        $('#id_faith_promise').prop('readonly', true);
        $('option:not(:selected)').remove();
    }
});