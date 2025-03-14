// Load the navbar burger

document.addEventListener('DOMContentLoaded', function () {
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

// Load the testimonials animation

document.addEventListener('DOMContentLoaded', () => {
  const testimonialCards = document.querySelectorAll('.testimonial-card');

  const observerOptions = {
    threshold: 0.3,
    rootMargin: '0px 0px -50px 0px'
  };

  const testimonialObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const content = card.querySelector('.testimonial-content');
        const media = card.querySelector('.media');

        setTimeout(() => {
          card.classList.add('visible');
        }, 0);

        setTimeout(() => {
          content.classList.add('visible');
        }, 200);

        setTimeout(() => {
          media.classList.add('visible');
        }, 400);

        testimonialObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  testimonialCards.forEach(card => {
    testimonialObserver.observe(card);
  });
});

// Load the counter animation for statistics section

document.addEventListener('DOMContentLoaded', () => {
  const statValues = document.querySelectorAll('.stat-value');

  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const statValue = entry.target;
        const originalText = statValue.textContent;
        const endValue = parseInt(originalText.replace(/[k+%]/g, ''));

        animateCounter(statValue, endValue, originalText);

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  statValues.forEach(stat => observer.observe(stat));
});

function animateCounter(element, endValue, originalText) {
  let startValue = 0;
  const duration = 2000;
  const startTime = performance.now();

  // Extract ‘k+’ or ‘%’ from the original text
  const suffix = originalText.replace(endValue.toString(), '');

  function updateCounter(currentTime) {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);
    const currentValue = Math.round(startValue + progress * (endValue - startValue));

    element.textContent = currentValue + suffix;

    if (progress < 1) {
      requestAnimationFrame(updateCounter);
    }
  }

  requestAnimationFrame(updateCounter);
}