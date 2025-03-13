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

// Carousel slider

document.addEventListener('DOMContentLoaded', () => {
    const statValues = document.querySelectorAll('.stat-value');
    
    const observerOptions = {
      threshold: 0.5
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('has-text-primary');
          
          entry.target.style.animation = 'fadeInUp 0.5s ease-out';
          
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    statValues.forEach(stat => {
      observer.observe(stat);
    });
    
    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.classList.add('has-background-light');
      });
      
      card.addEventListener('mouseleave', () => {
        card.classList.remove('has-background-light');
      });
    });
  });