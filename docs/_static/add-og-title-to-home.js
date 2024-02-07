document.addEventListener('DOMContentLoaded', function() {
 if(window.location.pathname === '/' || window.location.pathname === '/index.html') {

  let ogTitle = document.querySelector('meta[property="og:title"]')
  let ogTitleContent = ogTitle.getAttribute('content')

  if (ogTitleContent == "<no title>") {
    ogTitle.setAttribute('content', 'Falco')
  }
 }
});
