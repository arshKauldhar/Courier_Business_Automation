document.addEventListener('DOMContentLoaded', function() {
    const operationButtons = document.querySelectorAll('.operation-buttons button');
    const formContainers = document.querySelectorAll('.form-container');

    operationButtons.forEach(function(button, index) {
        button.addEventListener('click', function() {
            console.log('Button clicked:', button.textContent); // Debug statement
            // Hide all form containers
            formContainers.forEach(function(container) {
                container.classList.remove('active');
            });

            // Show the corresponding form container based on the clicked button
            formContainers[index].classList.add('active');
        });
    });

    const showBranchesButtons = document.querySelectorAll('.btn-show-branches');
    const branchForm = document.querySelector('.form-container.search-form'); // Select the branch form container

    // Show branch form when any show branches button is clicked
    showBranchesButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Hide all form containers except the branch form
            formContainers.forEach(function(container) {
                if (container !== branchForm) {
                    container.classList.remove('active');
                }
            });

            // Show branch form
            branchForm.classList.add('active');
        });
    });

    // Handle search functionality
    document.getElementById('search-btn').addEventListener('click', function() {
        // Perform search operation...
    });
});



$(document).ready(function() {
    $('#search-btn').click(function() {
        $.ajax({
            url: '/admin/display_employee',
            type: 'GET',
            success: function(response) {
                // Clear existing table data
                $('#employee-table tbody').empty();
                // Append fetched data to table
                $.each(response, function(index, employee) {
                    $('#employee-table tbody').append(
                        '<tr>' +
                            '<td>' + employee.emp_user_id + '</td>' +
                            '<td>' + employee.designation + '</td>' +
                            '<td>' + employee.join_date + '</td>' +
                            '<td>' + employee.P_name + '</td>' +
                            '<td>' + employee.age + '</td>' +
                            '<td>' + employee.area_or_village + '</td>' +
                            '<td>' + employee.city + '</td>' +
                            '<td>' + employee.P_role + '</td>' +
                        '</tr>'
                    );
                });
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('show-branches-btn').addEventListener('click', function() {
        fetch('/admin/get_branches')
            .then(response => response.json())
            .then(data => {
                // Clear existing table data
                document.getElementById('branch-table').querySelector('tbody').innerHTML = '';

                // Populate table with fetched branch data
                data.forEach(branch => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${branch[0]}</td>
                        <td>${branch[1]}</td>
                        <td>${branch[2]}</td>
                        <td>${branch[3]}</td>
                        <td>${branch[4]}</td>
                    `;
                    document.getElementById('branch-table').querySelector('tbody').appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching branch data:', error);
                // Handle error, such as displaying an error message
            });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('search-orders-btn').addEventListener('click', function() {
        fetch('/admin/get_orders')
            .then(response => response.json())
            .then(data => {
                // Clear existing table data
                document.getElementById('order-table').querySelector('tbody').innerHTML = '';

                // Populate table with fetched order data
                data.forEach(order => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${order[0]}</td>
                        <td>${order[1]}</td>
                        <td>${order[2]}</td>
                        <td>${order[3]}</td>
                        <td>${order[4]}</td>
                        <td>${order[5]}</td>
                        <!-- Add more table data for other columns -->
                    `;
                    document.getElementById('order-table').querySelector('tbody').appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching order data:', error);
                // Handle error, such as displaying an error message
            });
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
