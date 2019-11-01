$(document).ready(function () {
    $('[id$=_copy]').click(function() {
        var id = $(this).attr('id');
        var query = id.replace("_copy", "");

        var textArea = document.createElement("textarea");
        textArea.value = $('#' + query).val();
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    });
});