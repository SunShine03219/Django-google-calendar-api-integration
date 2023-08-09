/* 
    LIGHT 
    &
    DARK
    MODE
*/

const toggleSwitch    = document.getElementById('mode-toggle');
const body            = document.body;
const tableElements   = document.querySelectorAll('table');
const colElements     = document.querySelectorAll('[class^="col-"]:not(#chatHeaderCol,#filterMenu)');
const cardElements    = document.querySelectorAll('.card:not(.mb-3)');
const modelbodychat   = document.getElementById('modal-body-chat');
const sendBoxChat     = document.getElementById('send-box');

// Set initial state based on user preference
const isLightMode = localStorage.getItem('mode') === 'light';
toggleSwitch.checked = isLightMode;
toggleMode(isLightMode);

//-------------------------------------------

function toggleWithTryCatch(element, className, isLightMode) {
  try {
    element.classList.toggle(className, isLightMode);
  } catch (error) {
    //console.log(`Error toggling "${className}" class in element:`, element);
  }
}

function toggleMode(isLightMode) {
  toggleWithTryCatch(body, 'light-mode', isLightMode);
  toggleWithTryCatch(body, 'bg-dark', !isLightMode);
  toggleWithTryCatch(body, 'text-white', !isLightMode);
  toggleWithTryCatch(modelbodychat, 'bg-dark', !isLightMode);
  toggleWithTryCatch(sendBoxChat, 'bg-dark', !isLightMode);

  tableElements.forEach(table => {
    toggleWithTryCatch(table, 'table-light', isLightMode);
    toggleWithTryCatch(table, 'table-dark', !isLightMode);
  });

  colElements.forEach(colElement => {
    toggleWithTryCatch(colElement, 'bg-light', isLightMode);
    toggleWithTryCatch(colElement, 'bg-dark', !isLightMode);
    toggleWithTryCatch(colElement, 'text-dark', isLightMode);
    toggleWithTryCatch(colElement, 'text-white', !isLightMode);
  });

  cardElements.forEach(cardElement => {
    toggleWithTryCatch(cardElement, 'bg-light', isLightMode);
    toggleWithTryCatch(cardElement, 'bg-dark', !isLightMode);
    toggleWithTryCatch(cardElement, 'text-dark', isLightMode);
    toggleWithTryCatch(cardElement, 'text-white', !isLightMode);
  });
}


//-------------------------------------------

// Add event listener to toggle switch
toggleSwitch.addEventListener('change', function() {
  const isLightMode = this.checked;
  toggleMode(isLightMode);
  localStorage.setItem('mode', isLightMode ? 'light' : 'dark');
});


