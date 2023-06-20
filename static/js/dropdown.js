document.addEventListener('click', function (event) {
  var dropdowns = document.getElementsByClassName('dropdown');
  for (var i = 0; i < dropdowns.length; i++) {
    var dropdown = dropdowns[i];
    if (dropdown.contains(event.target)) {
      dropdown.classList.toggle('show');
    } else {
      dropdown.classList.remove('show');
    }
  }
});
