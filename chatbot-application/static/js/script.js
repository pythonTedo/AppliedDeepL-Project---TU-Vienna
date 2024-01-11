function getCaret(el) {
    if (el.selectionStart) {
        return el.selectionStart;
    } else if (document.selection) {
        el.focus();
        var r = document.selection.createRange();
        if (r == null) {
            return 0;
        }
        var re = el.createTextRange(),
            rc = re.duplicate();
        re.moveToBookmark(r.getBookmark());
        rc.setEndPoint('EndToStart', re);
        return rc.text.length;
    }
    return 0;
}


document.addEventListener("DOMContentLoaded", function() {
    var textArea = document.getElementById('text');
    
    textArea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Use SHIFT AND ENTER FOR \n IN THE textarea ELEMENT
    $('#text').keydown(function (event) {
        if (event.shiftKey && event.keyCode == 13) {
            // Insert a newline at the current cursor position
            var content = this.value;
            var caret = getCaret(this);
            this.value = content.substring(0, caret) + "\n" + content.substring(caret, content.length);
            
            // Move the caret to right after the inserted newline
            this.setSelectionRange(caret + 1, caret + 1);
            // Scroll to the bottom of the textarea
            //this.scrollTop = this.scrollHeight;
            event.preventDefault();
        }
        else if (event.keyCode == 13) {
            this.value = this.value.trim();
            $("#messageArea").submit();
            this.value = '';
            event.preventDefault();
            this.style.height = ''
        }
    });

    var temperatureRange = document.getElementById('temperatureRange');
    var temperatureInput = document.getElementById('temperatureInput');
    
    // Update the displayed value for the temperature slider
    temperatureRange.addEventListener('input', function() {
        temperatureInput.textContent = temperatureRange.value;
    });

    // Access the length range slider and its corresponding output span
    var lengthRange = document.getElementById('lengthRange');
    var lengthInput = document.getElementById('lengthInput');

    // Update the displayed value for the length slider
    lengthRange.addEventListener('input', function() {
        lengthInput.textContent = lengthRange.value;
    });

    var conversationsRange = document.getElementById('conversationsRange');
    var conversationsInput = document.getElementById('conversationsInput');
    
    // Update the displayed value when the range slider value changes
    conversationsRange.addEventListener('input', function() {
        conversationsInput.textContent = conversationsRange.value;
    });

    document.getElementById('resetSessionBtn').addEventListener('click', function() {
        sessionStorage.clear();
        
        $.ajax({
            url: "/reset_session",
            type: "POST",
            success: function(response) {
                alert("Chat session reset!");
                // Reload the page to display the flashed message
                location.reload();
            }
        });
    });
});