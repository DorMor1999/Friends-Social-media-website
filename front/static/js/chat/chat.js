window.addEventListener('load', scrollToBottom);

function scrollToBottom() {
  var element = document.documentElement; // Select the root element of the document (the <html> tag)
  var scrollHeight = element.scrollHeight; // Total height of the scrollable content
  
  // Scroll to the bottom
  element.scrollTop = scrollHeight;
}