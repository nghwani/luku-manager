document.addEventListener("DOMContentLoaded", function () {
    fetch("/create_notification/")
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayNotification(data.message);
        }
    })
    .catch(error => console.error("Error fetching data:", error));  
});

function displayNotification(message) {
    const notificationContainer = document.createElement('div');
    notificationContainer.className = 'notification';
    notificationContainer.innerHTML = `
        <p>${message}</p>
        <button onclick="this.parentElement.remove()">close</button>
    `;

    document.body.appendChild(notificationContainer)
}