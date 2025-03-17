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

                    // ✅ Force Remove Scroll Lock (Fixes "Every Other Click" Issue)
                    setTimeout(() => {
                        document.body.style.overflow = "auto"; // Force scrolling to be enabled
                        document.documentElement.style.overflow = "auto"; // Ensure scrolling is active for the whole page
                        document.activeElement.blur(); // Remove focus from any active element
                    }, 100);

                    // ✅ Properly Remove the Grey Backdrop
                    setTimeout(() => {
                        let backdrop = document.querySelector('.offcanvas-backdrop');
                        if (backdrop) {
                            backdrop.remove();  // Manually remove Bootstrap's offcanvas backdrop
                        }
                    }, 300);

                    // ✅ Reinitialize Page-Specific Scripts
                    reinitializeScripts();
                })
                .catch(error => console.error("Error:", error));
        });
    });

    // ✅ Handle browser back/forward navigation
    window.onpopstate = function () {
        location.reload();
    };

    // ✅ Function to Reinitialize Page-Specific Scripts
    function reinitializeScripts() {
        console.log("Reinitializing page scripts...");

        // ✅ Force-enable scrolling
        document.body.style.overflow = "auto";
        document.documentElement.style.overflow = "auto";

        // ✅ Reinitialize Tech Stack Flip Animations (if needed)
        if (typeof initializeTechStack === "function") {
            initializeTechStack();
        }
    }
});
