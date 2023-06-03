$(document).ready(function() {
    if ($('#id_authorization').is(':checked')) {
        $('#id_name').prop('readonly', true);
        $('#id_amount').prop('readonly', true);
        $('#id_faith_promise').prop('readonly', true);
        $('option:not(:selected)').remove();
        $('#id_authorization').prop('disabled', true).prop('name', '');
        let elem = $('div').find('[data-contentpath="authorization"]');
        elem.append('<input id="id_authorization" type="hidden" name="authorization" value="true">');
    }
});
