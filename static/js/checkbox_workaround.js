const checkbox1 = document.getElementById('id_groups_0');
const checkbox2 = document.getElementById('id_groups_1');

checkbox1.addEventListener('change', function() {
    if (this.checked) {
        checkbox2.checked = false;
    }
});

checkbox2.addEventListener('change', function() {
    if (this.checked) {
        checkbox1.checked = false;
    }
});
