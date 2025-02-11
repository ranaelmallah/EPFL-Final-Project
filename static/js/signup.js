document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.querySelector(".nav-links");

    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const fullnameInput = document.getElementById("fullname");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = form.querySelector("input[type='submit']");

    const fullnameError = document.getElementById("fullname-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    function validateInputs() {
        let isValid = true;

        if (fullnameInput.value.trim().length < 3) {
            fullnameError.style.display = "block";
            isValid = false;
        } else {
            fullnameError.style.display = "none";
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value.trim())) {
            emailError.style.display = "block";
            isValid = false;
        } else {
            emailError.style.display = "none";
        }

        if (passwordInput.value.length < 6) {
            passwordError.style.display = "block";
            isValid = false;
        } else {
            passwordError.style.display = "none";
        }

        submitButton.disabled = !isValid;
    }

    fullnameInput.addEventListener("input", validateInputs);
    emailInput.addEventListener("input", validateInputs);
    passwordInput.addEventListener("input", validateInputs);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userData = {
            fullname: fullnameInput.value.trim(),
            email: emailInput.value.trim(),
            password: passwordInput.value,
        };

        let users = JSON.parse(localStorage.getItem("users")) || [];
        if (users.some(user => user.email === userData.email)) {
            alert("Email already exists! Please use a different email.");
            return;
        }

        users.push(userData);
        localStorage.setItem("users", JSON.stringify(users));

        try {

            const formData = new FormData();
            formData.append("fullname", fullnameInput.value.trim());
            formData.append("email", emailInput.value.trim());
            formData.append("password", passwordInput.value);

            const response = await fetch("/auth/signup", {
                method: "POST",
                body: formData,
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                alert("Signup failed! Please try again.");
            }
        } catch (error) {
            console.log("Error:", error);
        }
    });
});