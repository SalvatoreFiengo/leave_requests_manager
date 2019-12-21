$(document).ready(function () {
    // if user on IE renders an alert on screen
    if (navigator.userAgent.indexOf('MSIE') !== -1
        || navigator.appVersion.indexOf('Trident/') > -1) {
        const error = "<h2 class='text-danger text-center mb-3'>Several features are not supported by this browser.<br> Please consider to switch to Chrome or Edge</h2>";
        $('#calendar-wrapper').children().hide();
        $('#calendar-wrapper').after(error);
    }
});