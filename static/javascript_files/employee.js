document.addEventListener("DOMContentLoaded", function() {
    const orderBtn = document.getElementById("orderbtn");
    const trackBtn = document.getElementById("trackbtn");
    const billBtn = document.getElementById("billbtn");
    const orderSection = document.getElementById("ordersection");
    const trackSection = document.getElementById("tracksection");
    const billSection = document.getElementById("billsection");

    orderBtn.addEventListener("click", function() {
        orderBtn.classList.add("selected-operation");
        trackBtn.classList.remove("selected-operation");
        billBtn.classList.remove("selected-operation");
        orderSection.classList.remove("hidden");
        trackSection.classList.add("hidden");
        billSection.classList.add("hidden");
    });

    trackBtn.addEventListener("click", function() {
        trackBtn.classList.add("selected-operation");
        orderBtn.classList.remove("selected-operation");
        billBtn.classList.remove("selected-operation");
        trackSection.classList.remove("hidden");
        orderSection.classList.add("hidden");
        billSection.classList.add("hidden");
    });

    billBtn.addEventListener("click", function() {
        billBtn.classList.add("selected-operation");
        orderBtn.classList.remove("selected-operation");
        trackBtn.classList.remove("selected-operation");
        billSection.classList.remove("hidden");
        orderSection.classList.add("hidden");
        trackSection.classList.add("hidden");
    });
});



$(document).ready(function() {
    // Fetch orders from the backend when the page loads
    $.get("/employee/view_orders", function(data) {
        // Clear existing table rows
        $("#ordersTableBody").empty();
        
        // Add new rows with order data
        data.forEach(function(order) {
            $("#ordersTableBody").append(
                "<tr>" +
                "<td>" + order[0] + "</td>" +
                "<td>" + order[1] + "</td>" +
                "<td>" + order[2] + "</td>" +
                "<td class='actualDelivery'>" + order[3] + "</td>" +
                "<td>" + order[4] + "</td>" +
                "<td>" + order[5] + "</td>" +
                "<td>" + order[6] + "</td>" +
                "<td>" + order[7] + "</td>" +
                "<td>" + order[8] + "</td>" +
                "<td>" + order[9] + "</td>" +
                "<td>" + order[10] + "</td>" +
                "<td>" + order[11] + "</td>" +
                "<td><button class='editBtn'>Edit</button></td>" +
                "</tr>"
            );
        });
    });

    // Handle click event for edit buttons
    $(document).on("click", ".editBtn", function() {
        // Get the actual delivery date cell
        var actualDeliveryCell = $(this).closest("tr").find(".actualDelivery");
        
        // Get the current actual delivery date value
        var currentActualDelivery = actualDeliveryCell.text();
        
        // Prompt the user to enter the new actual delivery date
        var newActualDelivery = prompt("Enter new actual delivery date (YYYY-MM-DD) :", currentActualDelivery);
        
        // Check if the user entered a new actual delivery date
        if (newActualDelivery !== null) {
            // Send the new actual delivery date to the server using AJAX
            var orderId = $(this).closest("tr").find("td:first").text(); // Get the order ID
            var requestData = {
                orderId: orderId,
                newActualDelivery: newActualDelivery
            };
            
            $.ajax({
                type: "POST",
                url: "/update_actual_delivery",
                contentType: "application/json",
                data: JSON.stringify(requestData),
                success: function(response) {
                    // Update the actual delivery date cell with the new value
                    actualDeliveryCell.text(newActualDelivery);
                    alert("Actual delivery date updated successfully");
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                    alert("An error occurred while updating the actual delivery date");
                }
            });
        }
    });
});
// for logout
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btnLogout').addEventListener('click', function() {
        // Call the logout function
        logOut();
    });

    function logOut() {
        window.location.href = '/logout'; 
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const trackSection = document.getElementById('tracksection');
    const updateForm = document.getElementById('updateForm');
    const updateResultDiv = document.getElementById('updateResult');

    function updateTracking(event) {
        event.preventDefault();
        
        const trackingId = document.getElementById('trackingId').value;
        const pickupTime = document.getElementById('pickupTime').value;
        const status = document.getElementById('status').value;
        const receivedTime = document.getElementById('receivedTime').value;
        const receiverName = document.getElementById('receiverName').value;
        const receiverRelation = document.getElementById('receiverRelation').value;

        fetch('/update_tracking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                trackingId: trackingId,
                pickupTime: pickupTime,
                status: status,
                receivedTime: receivedTime,
                receiverName: receiverName,
                receiverRelation: receiverRelation
            })
        })
        .then(response => response.json())
        .then(data => {
            updateResultDiv.innerHTML = '<p>' + data.message + '</p>';
        })
        .catch(error => {
            console.error('Error updating tracking:', error);
            updateResultDiv.innerHTML = '<p>An error occurred while updating tracking information. Please try again later.</p>';
        });
    }

    updateForm.addEventListener('submit', updateTracking);

    // Show the tracking section
    trackSection.classList.remove('hidden');
});


