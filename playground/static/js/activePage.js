document.addEventListener("DOMContentLoaded", function() {
    const activePage = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        const linkPathname = new URL(link.href).pathname;
        if (linkPathname === activePage) {
            link.classList.add('current');
        }
    });
});
