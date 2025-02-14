document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const alerts = document.getElementById("alerts");

    function showAlert(message, type = "error") {
        alerts.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
        setTimeout(() => alerts.innerHTML = "", 3000);
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;

            const response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();
            if (response.ok) {
                showAlert("Login successful!", "success");
                window.location.href = "/"; 
            } else {
                showAlert(result.error || "Invalid credentials");
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const first_name = document.getElementById("signupFirstName").value;
            const last_name = document.getElementById("signupLastName").value;
            const email = document.getElementById("signupEmail").value;
            const password = document.getElementById("signupPassword").value;

            const response = await fetch("/api/signup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ first_name, last_name, email, password })
            });

            const result = await response.json();
            if (response.ok) {
                showAlert("Signup successful! Redirecting...", "success");
                setTimeout(() => window.location.href = "/", 2000);
            } else {
                showAlert(result.error || "Signup failed");
            }
        });
    }
});
