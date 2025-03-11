// Load the navbar burger

document.addEventListener('DOMContentLoaded', function () {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach($el => {
            $el.addEventListener('click', () => {
                const target = $el.dataset.target;
                const $target = document.getElementById(target);

                $el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }
});