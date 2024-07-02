function createNotification(title, body, imgUrl) {
    const container = document.querySelector('.notification-container');

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification hidden'; // Start hidden to manage transition
    notification.innerHTML = `
        <div class="innernoti">
            <img src="${imgUrl}" alt="Icon" class="notification-icon">
            <div class="text-content">
                <div class="notification-header">
                    <span class="notification-title">${title}</span>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="notification-body">${body}</div>
            </div>
        </div>
    `;

    // Insert the new notification at the top of the container
    container.prepend(notification); // Ensures new notifications are added at the top

    // Show notification with a delay to allow CSS transition
    setTimeout(() => {
        notification.classList.remove('hidden');
    }, 100);

    // Set auto-hide with cleanup
    setTimeout(() => {
        notification.classList.add('hidden');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 500); // Ensure smooth fading before removal
    }, 30000);

    // Close button functionality
    notification.querySelector('.close-btn').addEventListener('click', () => {
        notification.classList.add('hidden');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 500); // Remove from DOM after transition
    });
}