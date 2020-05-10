const btn = document.querySelector('.btnTop');

window.addEventListener('scroll', () => {

    if (window.pageYOffset > 300) {
        btn.style.display = 'block';

    } else {
        btn.style.display = 'none';
    }
});

btn.addEventListener('click', () => {
    window.scrollTo(0, 0);
});