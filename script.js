// ===============================
// FRANCIS GATHOGO WEBSITE
// JAVASCRIPT
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Francis Gathogo website loaded successfully.");

    // ===============================
    // NAVIGATION
    // ===============================

    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.forEach(function (item) {
                item.classList.remove("active");
            });
            this.classList.add("active");
        });
    });

    // ===============================
    // CONTACT FORM → PYTHON
    // ===============================

    const contactForm = document.querySelector(".contact-form");

    if (contactForm) {

        contactForm.addEventListener("submit", async function (event) {

            event.preventDefault();

            const formData = new FormData(contactForm);

            try {

                const response = await fetch("/contact", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    alert(result.message);
                    contactForm.reset();
                } else {
                    alert(result.error || "Something went wrong. Please try again.");
                }

            } catch (error) {

                console.error("Error:", error);

                alert(
                    "Could not connect to the server. " +
                    "Please try again."
                );

            }

        });

    }

    // ===============================
    // SCROLL REVEAL
    // ===============================

    const sections = document.querySelectorAll("section");

    const revealSections = function () {

        sections.forEach(function (section) {

            const sectionPosition = section.getBoundingClientRect().top;
            const screenPosition = window.innerHeight * 0.85;

            if (sectionPosition < screenPosition) {
                section.classList.add("show-section");
            }

        });

    };

    window.addEventListener("scroll", revealSections);

    revealSections();

});