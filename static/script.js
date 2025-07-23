function applyFilter(filterType) {
    window.location.href = `/index?filter=${filterType}`;
}

function showDatePopup() {
    document.getElementById('datePopup').style.display = 'block';
}

function showMonthPopup() {
    document.getElementById('monthPopup').style.display = 'block';
}

function hidePopup(popupId) {
    document.getElementById(popupId).style.display = 'none';
}

function applySpecificDateFilter() {
    const specificDate = document.getElementById('specificDateInput').value;
    window.location.href = `/index?filter=specific_date&specific_date=${specificDate}`;
}

function applySpecificMonthFilter() {
    const specificMonth = document.getElementById('specificMonthInput').value;
    window.location.href = `/index?filter=specific_month&specific_month=${specificMonth}`;
}

function logout() {
    window.location.href = '/logout';
}

function showEmployeePopup() {
    document.getElementById('employeePopup').style.display = 'block';
}

function hidePopup(popupId) {
    document.getElementById(popupId).style.display = 'none';
}

function applyEmployeeFilter() {
    const selectedEmployee = document.getElementById('employeeSelect').value;
    const urlParams = new URLSearchParams(window.location.search);
    const currentFilter = urlParams.get('filter') || 'today'; // Keep current filter type
    const specificDate = urlParams.get('specific_date'); // Preserve specific date
    const specificMonth = urlParams.get('specific_month'); // Preserve specific month

    // Apply employee filter while maintaining the current date filter
    let query = `/index?filter=${currentFilter}&employee_name=${encodeURIComponent(selectedEmployee)}`;
    if (specificDate) {
        query += `&specific_date=${specificDate}`;
    }
    if (specificMonth) {
        query += `&specific_month=${specificMonth}`;
    }

    window.location.href = query;
}
// Ensure `employeePerformanceData` is defined in the HTML before this script is included
const ctx = document.getElementById('employeePerformanceChart').getContext('2d');
const employeePerformanceData = window.employeePerformanceData || {}; // Define this in HTML
const labels = Object.keys(employeePerformanceData);
const data = Object.values(employeePerformanceData);

const employeePerformanceChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: [
                '#FF6F61',  // Coral Red
                '#6B8E23',  // Olive Green
                '#4682B4',  // Steel Blue
                '#FFD700',  // Gold
                '#FF8C00',  // Dark Orange
                '#9370DB',  // Medium Purple
                '#C0C0C0',  // Silver
                '#FFB6C1'   // Light Pink
            ],
            borderColor: [
                '#FF6F61',  // Coral Red
                '#6B8E23',  // Olive Green
                '#4682B4',  // Steel Blue
                '#FFD700',  // Gold
                '#FF8C00',  // Dark Orange
                '#9370DB',  // Medium Purple
                '#C0C0C0',  // Silver
                '#FFB6C1'   // Light Pink
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return `${tooltipItem.label}: ${tooltipItem.raw}`;
                    }
                }
            },
            // 3D effect configuration
            chart3d: {
                enabled: true,
                rotation: {
                    x: 30,
                    y: 30,
                    z: 0
                },
                depth: 200
            }
        }
    }
});