document.addEventListener("DOMContentLoaded", function () {
    // ✅ Prevent background animation from restarting
    if (!window.orbInitialized) {
        window.orbInitialized = true;
        console.log("Background animation initialized!");
    }

    // ✅ Handle AJAX Navigation for Navbar Links
    document.querySelectorAll('.ajax-link').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent full page reload

            let url = this.getAttribute("href");

            fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    let parser = new DOMParser();
                    let newDocument = parser.parseFromString(html, "text/html");
                    let newContent = newDocument.querySelector("#main-content").innerHTML;

                    document.querySelector("#main-content").innerHTML = newContent; // Replace content
                    window.history.pushState(null, "", url); // Update browser URL

                    // ✅ Close the offcanvas menu
                    let offcanvasElement = document.querySelector('.offcanvas');
                    let offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvasElement);
                    if (offcanvasInstance) {
                        offcanvasInstance.hide();
                    }

                    // ✅ Force-remove grey overlay
                    let backdrop = document.querySelector('.offcanvas-backdrop');
                    if (backdrop) {
                        backdrop.remove();  // Manually remove Bootstrap's offcanvas backdrop
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });

    // ✅ Handle browser back/forward navigation
    window.onpopstate = function () {
        location.reload();
    };
});
