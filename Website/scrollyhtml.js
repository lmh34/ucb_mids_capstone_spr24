// your-script.js

// Define the background element and the text container element
var backgroundEl = document.querySelector('.background');
var textContainerEl = document.querySelector('.text-container');

// Get all the scroll paragraphs
var scrollParagraphs = document.querySelectorAll('.scroll-paragraph');

// Map each paragraph to a Waypoint instance
var waypoints = Array.from(scrollParagraphs).map(function(el) {
    var step = +el.getAttribute('data-step');

    return new Waypoint({
        element: el,
        handler: function(direction) {
            var translateY = direction === 'down' ? '0%' : '100%';
            el.style.transform = 'translateY(' + translateY + ')';
        },
        offset: '50%',
    });
});

// Set up the enter and exit Waypoints for the text container
var enterWaypoint = new Waypoint({
    element: textContainerEl,
    handler: function(direction) {
        var fixed = direction === 'down';
        var bottom = false;
        toggle(fixed, bottom);
    },
});

var exitWaypoint = new Waypoint({
    element: textContainerEl,
    handler: function(direction) {
        var fixed = direction === 'up';
        var bottom = !fixed;
        toggle(fixed, bottom);
    },
    offset: 'bottom-in-view',
});

// Define the toggle function (assuming you have one)
function toggle(fixed, bottom) {
    // Your toggle logic goes here
    // For example, you could add/remove a class to change the background appearance
}
