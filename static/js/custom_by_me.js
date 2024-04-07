// Open image in popup window
document.addEventListener('DOMContentLoaded', function() {
    let popupLinks = document.querySelectorAll('.popup-link');

    popupLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default anchor behavior
            let imgSrc = this.querySelector('img').getAttribute('src');
            let imgWidth = this.querySelector('img').naturalWidth;
            let imgHeight = this.querySelector('img').naturalHeight;

            // Create modal container
            let modalContainer = document.createElement('div');
            modalContainer.style.position = 'fixed';
            modalContainer.style.top = '0';
            modalContainer.style.left = '0';
            modalContainer.style.width = '100%';
            modalContainer.style.height = '100%';
            modalContainer.style.display = 'flex';
            modalContainer.style.justifyContent = 'center';
            modalContainer.style.alignItems = 'center';
            modalContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
            modalContainer.addEventListener('click', function() {
                modalContainer.remove();
            });

            // Create close button
            let closeButton = document.createElement('span');
            closeButton.innerHTML = '&times;';
            closeButton.style.position = 'absolute';
            closeButton.style.top = '10px';
            closeButton.style.right = '10px';
            closeButton.style.color = '#fff';
            closeButton.style.fontSize = '30px';
            closeButton.style.cursor = 'pointer';
            closeButton.addEventListener('click', function(event) {
                event.stopPropagation(); // Prevent modal closing when clicking on close button
                modalContainer.remove();
            });
            modalContainer.appendChild(closeButton);

            // Create image element
            let modalImage = document.createElement('img');
            modalImage.style.width = imgWidth + 'px';
            modalImage.style.height = imgHeight + 'px';
            modalImage.style.display = 'block';
            modalImage.style.margin = 'auto';
            modalImage.setAttribute('src', imgSrc);
            modalContainer.appendChild(modalImage);

            document.body.appendChild(modalContainer);
        });
    });
});


// Inbox Popups

document.addEventListener('DOMContentLoaded', function () {
    const toggleRespondWindowButtons = document.querySelectorAll('.toggle-respond-window-btn');

    toggleRespondWindowButtons.forEach(button => {
        button.addEventListener('click', function () {
            const messageId = button.getAttribute('data-message-id');
            const respondWindow = document.getElementById(`respond-window-${messageId}`);
            const buttonText = button.innerText;

            if (buttonText === 'Respond') {
                button.innerText = 'Close Response';
            } else {
                button.innerText = 'Respond';
            }

            respondWindow.style.display = respondWindow.style.display === 'block' ? 'none' : 'block';
        });
    });
});

// Button delete script

document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    let messageIdToDelete;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            messageIdToDelete = button.getAttribute('data-message-id');
            $('#confirmDeleteModal').modal('show');
        });
    });

    confirmDeleteBtn.addEventListener('click', function () {
        // Submit form or trigger delete action
        $('#confirmDeleteModal').modal('hide');
        document.querySelector(`input[name="message_id"][value="${messageIdToDelete}"]`).closest('form').submit();
    });
});

// Filter by category

document.querySelectorAll('#category-form button').forEach(button => {
    button.addEventListener('click', function () {
        document.querySelectorAll('#category-form button').forEach(btn => {
            btn.classList.remove('active');
        });
        this.classList.add('active');
    });
});