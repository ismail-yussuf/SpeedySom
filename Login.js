document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
  
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
  
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/verify", true); // Adjust the URL as needed
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          document.getElementById("login-result").textContent = "Login successful!";
          window.location.href = "/Index.html";
        } 
        else {
          document.getElementById("login-result").textContent = "Login failed. Please try again.";
        }
      }
    };
    xhr.send("username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password));
  });
  