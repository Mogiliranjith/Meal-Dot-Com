function showSignIn() {
  document.getElementById("signin").style.display = "block";
  document.getElementById("signup").style.display = "none"
}

function showSignUp() {
    document.getElementById("signup").style.display = "block"
    document.getElementById("signin").style.display = "none";
}

function autoToggleForm(form) {
  if (form == "signup") {
    showSignUp();
  } else if (form === "signin") {
    showSignIn();
  }
}