const ths = document.querySelectorAll('th');


ths.forEach((th) => {

   const a = th.querySelector('a');


   const href = a.getAttribute('href');
   const sortParam = href.split('=')[1].split('&')[0];
   const sortDir = href.split('=')[2];

   var sortParams = window.sortParam;
   var sortDirs = window.sortDir;

   if (sortParams === 'some value' && sortDirs === 'some value') {
      const arrow = sortDir === 'asc' ? '↑' : '↓';
      a.innerHTML += arrow;
   }
});



var takeButtons = document.getElementsByClassName('take-btn');
for (var i = 0; i < takeButtons.length; i++) {
  takeButtons[i].addEventListener('click', function(event) {
    event.preventDefault();
    var form = this.closest('form');
    var modal = new bootstrap.Modal(document.getElementById('take-modal'));
    modal.show();
    var confirmButton = document.getElementById('take-confirm');
    confirmButton.addEventListener('click', function() {
      // Submit the form
      form.submit();
    });
  });
}



$(document).ready(function () {
   // Listen for changes to the search input
   $('#search-input').on('input', function () {
      // Get the search query
      var query = $(this).val().toLowerCase();

      // Filter the table rows based on the search query
      $('tbody tr').each(function () {
         var categoryL1 = $(this).find('td:nth-child(3)').text().toLowerCase();
         var categoryL2 = $(this).find('td:nth-child(4)').text().toLowerCase();
         if (categoryL1.indexOf(query) !== -1 || categoryL2.indexOf(query) !== -1) {
            $(this).show();
         } else {
            $(this).hide();
         }
      });
   });
});


$(document).ready(function() {
   var $switches = $('#switch1, #switch2');
   var $tableRows = $('tbody tr');

   $switches.prop('checked', true);
   filterRows();
   $switches.on('change', filterRows);

   function filterRows() {
      var switch1State = $('#switch1').prop('checked');
      var switch2State = $('#switch2').prop('checked');

      $tableRows.each(function() {
         var categoryL1 = $(this).find('td:nth-child(3)').text().toLowerCase();
         var isVisible = (switch1State && categoryL1.includes('informations technology')) || (switch2State && categoryL1.includes('services'));

         isVisible ? $(this).show() : $(this).hide();
      });
   }
});




const submitButton = document.getElementById('submit-tags');
const filterForm = document.getElementById('tags-form');

submitButton.addEventListener('click', () => {
   filterForm.submit();
});


// Get the search box element and tag items
var searchBox = document.getElementById("tag-search");
var tagItems = document.getElementsByClassName("tag-item");

// Add an event listener to the search box
searchBox.addEventListener("input", function () {
   // Get the search term and convert to lowercase
   var searchTerm = searchBox.value.toLowerCase();

   // Loop through the tag items and hide/show based on the search term
   for (var i = 0; i < tagItems.length; i++) {
      var tagItem = tagItems[i];
      var tagName = tagItem.querySelector(".form-check-label").textContent.toLowerCase();
      if (tagName.indexOf(searchTerm) >= 0) {
         tagItem.style.display = "";
      } else {
         tagItem.style.display = "none";
      }
   }
});