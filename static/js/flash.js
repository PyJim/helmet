// Get the flash message container
const flashContainer = document.getElementsByClassName('flash-messages');

// Check if the flash messages exist

flashContainer.forEach(element => {
    if (element) {
    // Set the timeout duration in milliseconds (e.g., 3000ms for 3 seconds)
    const timeoutDuration = 2000;

    // Remove the flash messages after the specified duration
    setTimeout(() => {
        element.style.display = 'none';
    }, timeoutDuration);
}
});

