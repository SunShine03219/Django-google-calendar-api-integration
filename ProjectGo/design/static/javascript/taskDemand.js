

const ths = document.querySelectorAll('th');

ths.forEach((th) => {

const a = th.querySelector('a');

const href = a.getAttribute('href');
const sortParam = href.split('=')[1].split('&')[0];
const sortDir = href.split('=')[2];

var sortParams = window.sortParam;
var sortDirs = window.sortDir;

if (sortParams === 'some value' && sortDirs === 'some value') {
    const arrow = sortDir === 'asc' ? '&uarr;' : '&darr;';
    a.innerHTML += arrow;
}
});

function attachModalEvent(buttons, modalId, confirmId) {
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function(event) {
      event.preventDefault();
      var form = this.closest('form');
      var modal = new bootstrap.Modal(document.getElementById(modalId));
      modal.show();
      var confirmButton = document.getElementById(confirmId);
      confirmButton.addEventListener('click', function() {
        form.submit();
      });
    });
  }
}

var finishButtons = document.getElementsByClassName('finish-btn');
attachModalEvent(finishButtons, 'finish-modal', 'finish-confirm');

var deleteButtons = document.getElementsByClassName('delete-btn');
attachModalEvent(deleteButtons, 'delete-modal', 'delete-confirm');

var duplicateButtons = document.getElementsByClassName('duplicate-btn');
attachModalEvent(duplicateButtons, 'duplicate-modal', 'duplicate-confirm');

var cancelButtons = document.getElementsByClassName('cancel-btn');
attachModalEvent(cancelButtons, 'cancel-modal', 'cancel-confirm');

function generateModal(modalId, modalLabel, title, body, cancelText, confirmText, confirmId, confirmClass) {
  return `
    <div class="modal fade" id="${modalId}" tabindex="-1" aria-labelledby="${modalId}-label" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="${modalId}-label">${title}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            ${body}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${cancelText}</button>
            <button type="button" class="btn ${confirmClass}" id="${confirmId}">${confirmText}</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Generate Delete Modal
const deleteModal = generateModal(
  'delete-modal',
  'delete-modal',
  'Confirm Deletion',
  'Are you sure you want to delete this item?',
  'Cancel',
  'Delete',
  'delete-confirm',
  'btn-danger'
);

// Generate Cancel Modal
const cancelModal = generateModal(
  'cancel-modal',
  'cancel-modal',
  'Confirm Cancellation',
  'Are you sure you want to cancel this item?',
  'Cancel',
  'Cancel',
  'cancel-confirm',
  'btn-warning'
);

// Generate Finish Modal
const finishModal = generateModal(
  'finish-modal',
  'finish-modal',
  'Finish IT',
  'Are you sure you want to finish this item?',
  'Cancel',
  'Finish IT',
  'finish-confirm',
  'btn-success'
);

// Generate Duplicate Modal
const duplicateModal = generateModal(
  'duplicate-modal',
  'duplicate-modal',
  'Duplicate IT',
  'Are you sure you want to duplicate this item?',
  'Cancel',
  'Duplicate',
  'duplicate-confirm',
  'btn-danger'
);

// Append modals to the DOM
document.body.insertAdjacentHTML('beforeend', deleteModal);
document.body.insertAdjacentHTML('beforeend', cancelModal);
document.body.insertAdjacentHTML('beforeend', finishModal);
document.body.insertAdjacentHTML('beforeend', duplicateModal);

// Your existing JavaScript code...
