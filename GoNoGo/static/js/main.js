document.addEventListener("DOMContentLoaded", function () {
    const newEventBtn = document.getElementById('new-event-btn');
    const newEventModal = document.getElementById('new-event-modal');
    const newEventModalContent = document.getElementById('new-event-modal-content');

    function attachCloseEvent() {
        const closeBtn = document.getElementById('close-btn'); // Look for closeBtn after content is loaded
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                console.log("close btn!!!!!!");
                newEventModal.style.display = 'none'; // Hide the form
                window.location.href = '/dashboard/'; // Redirect to dashboard
            });
        }
    }

    newEventBtn.addEventListener('click', function () {
        fetch(`/new_event/`)
            .then(response => response.text())
            .then(data => {
                newEventModalContent.innerHTML = data;
                newEventModal.style.display = 'block';
                window.history.pushState({}, null, '/new_event/');
                attachCloseEvent();  // Call function to attach the close button event
            });
    });
});



