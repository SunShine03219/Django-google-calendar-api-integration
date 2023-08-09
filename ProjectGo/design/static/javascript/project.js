$.noConflict();
/* 
  
  
  Hide/Unhide after cat L1/L2 has been added
  
  
  
  */
  $(document).ready(function () {
    $('#saveModalIT').click(function () {
       var selectedCategories = [];
       $('.modal-body :checkbox:checked').each(function () {
          selectedCategories.push($(this).siblings('label').text());
       });
       $('#selected-categories').val(selectedCategories.join(','));
       $('#modalIT').modal('hide');
       document.getElementById("taskForm").style.display = "block";
       document.getElementById("modalPart").style.display = "none";
       document.getElementById("Create").style.display = "none";
       document.getElementById("Send").style.display = "block";
       document.getElementById("tags-input").style.display = "none";
 
       var form = document.getElementById('taskForm');
       form.elements.categoryL1.value = "IT";
       form.elements.categoryL2.value = selectedCategories;
    });
    $('#saveModalServices').click(function () {
       var selectedCategories = [];
       $('.modal-body :checkbox:checked').each(function () {
          selectedCategories.push($(this).siblings('label').text());
       });
       $('#selected-categories').val(selectedCategories.join(','));
       $('#modalServices').modal('hide');
       document.getElementById("taskForm").style.display = "block";
       document.getElementById("modalPart").style.display = "none";
       document.getElementById("Create").style.display = "none";
       document.getElementById("Send").style.display = "block";
       document.getElementById("tags-input").style.display = "none";
 
       var form = document.getElementById('taskForm');
       form.elements.categoryL1.value = "S";
       form.elements.categoryL2.value = selectedCategories;
    });
 
 });
 /* 
  
  
  Autocomplete for Tags
  &
  Add Tag to Input
  
  
  
  */
 $("#TagSearch").autocomplete({
    source: existingTags,
    minLength: 1,
    select: function (event, ui) {
       event.preventDefault();
       var selectedTag = ui.item.value.trim().split(/\s+/)[0];
       var inputField = $("#tags-input");
       var tagButton = $("<button class='btn btn-outline-warning tag-button'>" + selectedTag + "</button>");
 
       // Append tag button to the input field
       inputField.before(tagButton);
 
       // Add selectedTag to the input field value
       inputField.val(function (i, val) {
          if (val !== '') {
             val += ' ';
          }
          return val + selectedTag;
       });
 
       // Automatically select all elements in the input field
       inputField[0].select();
    }
 });
 
 // Handle click event on tag buttons
 $(document).on('click', '.tag-button', function () {
    var selectedTag = $(this).text();
    var inputField = $("#tags-input");
 
    // Remove tag button
    $(this).remove();
 
    // Remove selectedTag from input field value
    var currentValue = inputField.val().trim();
    var tags = currentValue.split(/\s+/);
    var updatedTags = tags.filter(function (tag) {
       return tag !== selectedTag;
    });
    inputField.val(updatedTags.join(' '));
 });
 
 var tagButtons = document.querySelectorAll('#tagsList .modal-body .list-tag-btn');
 // Attach a click event listener to each button
 tagButtons.forEach(function (button) {
    button.addEventListener('click', function () {
       var tagName = this.innerText;
       document.getElementById('TagSearch').value = tagName;
       var inputField = $("#tags-input");
       inputField.val(function (i, val) {
          if (val !== '') {
             val += ' ';
          }
          return val + tagName;
       });
 
       // Create tag button
       var tagButton = $("<button class='btn btn-outline-warning tag-button'>" + tagName + "</button>");
       inputField.before(tagButton);
    });
 });
 
 
 /* 
 
 
 Submission
 
 
 
 */
 function submitTaskForm() {
    const formElements = document.querySelectorAll('[required]');
    for (let i = 0; i < formElements.length; i++) {
       const element = formElements[i];
       if (element.value.trim() === '') {
          const modal = new bootstrap.Modal(document.getElementById('alert-modal'));
          const alertText = document.getElementById('alert-text');
          alertText.innerHTML = `Please fill in the ${element.name.toUpperCase()} information`;
          modal.show();
          element.focus();
          const okButton = document.querySelector('#alert-modal .modal-footer button.btn-primary');
          okButton.addEventListener('click', () => {
             modal.hide();
          });
          return;
       }
    }
 
    var modal = new bootstrap.Modal(document.getElementById('publish-modal'));
    modal.show();
    var confirmButton = document.getElementById('publish-confirm');
    confirmButton.addEventListener('click', function () {
       document.getElementById('taskForm').submit();
    });
    var cancelButton = document.getElementById('publish-cancel');
    cancelButton.addEventListener('click', function () {
       modal.hide();
    });
 
 }
 
 
 $(document).ready(function () {
    $('#alert-modal').on('hidden.bs.modal', function (e) {
       // Reset the modal content when it is closed
       $('#alert-text').text('');
    });
 });
 
 
 // Calendar
 
 jQuery(document).ready(function () {
   // Initialize datepickers using Flatpickr
   flatpickr('.datepicker', {
     dateFormat: 'Y-m-d' // specify the date format
     // Add any other options you need for Flatpickr
   });
 });

 
 
 