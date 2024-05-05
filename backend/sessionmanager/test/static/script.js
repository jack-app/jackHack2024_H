function req() {
  alert("b1 clicked");

  // fetch("http://localhost:8000/auth")
  //   .then((res) => res.json())
  //   .then((data) => {
  //     console.log(data);
  //   });
  window.location.href = "http://localhost:8000/auth";
}

window.addEventListener("load", function () {
  document.getElementById("b1").addEventListener("click", req);
});
