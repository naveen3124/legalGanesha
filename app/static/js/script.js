document.addEventListener("DOMContentLoaded", function() {
    // Add click event listener to blockquote for triggering scroll animation
    const blockquote = document.getElementById("quote");
    blockquote.addEventListener("click", function() {
        this.classList.toggle("animated-scroll");
    });
});