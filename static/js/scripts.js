// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    var closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(function(button) {
        button.onclick = function() {
            var div = this.parentElement;
            div.style.opacity = '0';
            setTimeout(function(){ div.style.display = 'none'; }, 600);
        };
    });

    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function(){ alert.style.display = 'none'; }, 600);
        });
    }, 5000);
});
