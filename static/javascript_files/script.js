const placeOrderBtn = document.getElementById("place-order-btn");
const trackOrderBtn = document.getElementById("track-order-btn");
const calculateBillBtn = document.getElementById("calculate-bill-btn");

const placeOrderSection = document.getElementById("place-order-section");
const trackOrderSection = document.getElementById("track-order-section");
const calculateBillSection = document.getElementById("calculate-bill-section");

function toggleSection(section) {
    section.classList.toggle("hidden");
}

// Event listeners for each button
placeOrderBtn.addEventListener("click", function() {
    toggleSection(placeOrderSection);
    trackOrderSection.classList.add("hidden");
    calculateBillSection.classList.add("hidden");
});

trackOrderBtn.addEventListener("click", function() {
    toggleSection(trackOrderSection);
    placeOrderSection.classList.add("hidden");
    calculateBillSection.classList.add("hidden");
});

calculateBillBtn.addEventListener("click", function() {
    toggleSection(calculateBillSection);
    placeOrderSection.classList.add("hidden");
    trackOrderSection.classList.add("hidden");
});

// function submitForm(){
//     document.getElementById('popup-content').style.display='none'; 
//     document.getElementsByClassName('.next-button-div').style.display='flex';
//     document.createElement('div');
//     document.
// }
// function submitForm() {
//         // Hide the recipient form
//         document.getElementById('recipient-form-popup').classList.add('hidden');

//         // Show the order details form
//         document.getElementById('order-details-form').classList.remove('hidden');
// }


function showForm(formId) {
    // Hide all forms
    var forms = document.querySelectorAll('.popup-content > div');
    forms.forEach(function(form) {
        form.classList.add('hidden');
    });

    // Show the selected form
    document.getElementById(formId).classList.remove('hidden');

    // Show or hide the submit button based on the current form
    var submitBtn = document.getElementById('submit-btn');
    if (formId === 'order-details-form') {
        submitBtn.classList.remove('hidden');
    } else {
        submitBtn.classList.add('hidden');
    }
}

// for calculator
function calculateBill() {
    // Get the values of distance and weight
    var distance = parseFloat(document.getElementById("distance").value);
    var weight = parseFloat(document.getElementById("weight").value);
    
    // Define the rate per km and rate per kg (in INR)
    var ratePerKm = 5; // ₹5 per km
    var ratePerKg = 10; // ₹10 per kg
    
    // Calculate the bill
    var distanceBill = distance * ratePerKm;
    var weightBill = weight * ratePerKg;
    var totalBill = distanceBill + weightBill;
    
    // Display the result
    var resultElement = document.getElementById("result");
    resultElement.innerHTML = "Distance Bill: ₹" + distanceBill.toFixed(2) + "<br>" +
                              "Weight Bill: ₹" + weightBill.toFixed(2) + "<br>" +
                              "Total Bill: ₹" + totalBill.toFixed(2);
}

// end of calculator code





function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("popup-visible");

    // Adjust position to keep the dropdown within the page width
    if (dropdownContent.classList.contains("popup-visible")) {
        var iconRect = document.getElementById("userIcon").getBoundingClientRect();
        var dropdownWidth = dropdownContent.offsetWidth;
        if ((iconRect.right + dropdownWidth) > window.innerWidth) {
            dropdownContent.style.right = "auto";
            dropdownContent.style.left = "calc(100% - " + dropdownWidth + "px)";
        } else {
            dropdownContent.style.right = "0";
            dropdownContent.style.left = "auto";
        }
    }
}

// Close the dropdown menu when clicking outside of it
window.onclick = function(event) {
    if (!event.target.matches('#userIcon')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var dropdown = dropdowns[i];
            if (dropdown.classList.contains('popup-visible')) {
                dropdown.classList.remove('popup-visible');
            }
        }
    }
}
