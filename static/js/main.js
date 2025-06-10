// Load the navbar burger

document.addEventListener("DOMContentLoaded", function () {
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  if ($navbarBurgers.length > 0) {
    $navbarBurgers.forEach(($el) => {
      $el.addEventListener("click", () => {
        const target = $el.dataset.target;
        const $target = document.getElementById(target);

        $el.classList.toggle("is-active");
        $target.classList.toggle("is-active");
      });
    });
  }
});

// Load the testimonials animation

document.addEventListener("DOMContentLoaded", () => {
  const testimonialCards = document.querySelectorAll(".card");

  const observerOptions = {
    threshold: 0.3,
    rootMargin: "0px 0px -50px 0px",
  };

  const testimonialObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const content = card.querySelector(".card-content");
        const media = card.querySelector(".media");

        setTimeout(() => {
          card.classList.add("visible");
        }, 0);

        setTimeout(() => {
          content.classList.add("visible");
        }, 200);

        setTimeout(() => {
          media.classList.add("visible");
        }, 400);

        testimonialObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  testimonialCards.forEach((card) => {
    testimonialObserver.observe(card);
  });
});

// Load the counter animation for statistics section

document.addEventListener("DOMContentLoaded", () => {
  const statValues = document.querySelectorAll(".stat-value");

  const observerOptions = {
    threshold: 0.5,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const statValue = entry.target;
        const originalText = statValue.textContent;
        const endValue = parseInt(originalText.replace(/[k+%]/g, ""));

        animateCounter(statValue, endValue, originalText);

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  statValues.forEach((stat) => observer.observe(stat));
});

function animateCounter(element, endValue, originalText) {
  let startValue = 0;
  const duration = 2000;
  const startTime = performance.now();

  // Extract ‘k+’ or ‘%’ from the original text
  const suffix = originalText.replace(endValue.toString(), "");

  function updateCounter(currentTime) {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);
    const currentValue = Math.round(
      startValue + progress * (endValue - startValue)
    );

    element.textContent = currentValue + suffix;

    if (progress < 1) {
      requestAnimationFrame(updateCounter);
    }
  }

  requestAnimationFrame(updateCounter);
}

// FAQ accordion functionality

document.addEventListener("DOMContentLoaded", () => {
  // FAQ accordion functionality
  const faqQuestions = document.querySelectorAll(".faq-question");

  faqQuestions.forEach((question) => {
    question.addEventListener("click", () => {
      const answer = question.nextElementSibling;

      // Toggle active state
      answer.classList.toggle("is-active");

      // Change icon
      const icon = question.querySelector(".icon i");
      if (answer.classList.contains("is-active")) {
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
      } else {
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
      }
    });
  });

  // Team card hover effect
  const teamCards = document.querySelectorAll(".team-card");
  teamCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.classList.add("has-shadow");
    });

    card.addEventListener("mouseleave", () => {
      card.classList.remove("has-shadow");
    });
  });
});

// JavaScript for Modals

document.addEventListener("DOMContentLoaded", function () {
  var editButtons = document.querySelectorAll('[id^="edit-survey-"]');
  editButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var id = this.getAttribute("data-id");
      var title = this.getAttribute("data-title");
      var description = this.getAttribute("data-description");
      showEditModal(id, title, description);
    });
  });

  var deleteButtons = document.querySelectorAll('[id^="delete-survey-"]');
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var id = this.getAttribute("data-id");
      showDeleteModal(id);
    });
  });
});

function showEditModal(id, title, description) {
  document.getElementById("edit_survey_id").value = id;
  document.getElementById("edit_title").value = title;
  document.getElementById("edit_description").value = description;
  document.getElementById("editModal").classList.add("is-active");
}

function closeEditModal() {
  document.getElementById("editModal").classList.remove("is-active");
}

function submitEditForm() {
  document.getElementById("editForm").submit();
}

function showDeleteModal(id) {
  document.getElementById("delete_survey_id").value = id;
  document.getElementById("deleteModal").classList.add("is-active");
}

function closeDeleteModal() {
  document.getElementById("deleteModal").classList.remove("is-active");
}

// Show the delete modal in the surveys page

function showDeleteModal(id) {
  document.getElementById("delete_survey_id").value = id;
  document.getElementById("deleteModal").classList.add("is-active");
}

function closeDeleteModal() {
  document.getElementById("deleteModal").classList.remove("is-active");
}

// Add options dynamically in the survey creation form

function addOption() {
  const optionsList = document.getElementById("options_list");
  const count = optionsList.children.length + 1;
  const div = document.createElement("div");
  div.className = "control mb-2";
  div.innerHTML = `<input class="input option-input" type="text" name="options[]" placeholder="Option ${count}" required>`;
  optionsList.appendChild(div);
}

function toggleOptions() {
  const type = document.getElementById("question_type").value;
  const optionsContainer = document.getElementById("options_container");
  if (type === "radio" || type === "checkbox") {
    optionsContainer.style.display = "";

    if (document.querySelectorAll(".option-input").length < 2) {
      addOption();
    }
  } else {
    optionsContainer.style.display = "none";
  }
}

// JavaScript for the survey creation form

let questionCount = 1;

function addQuestion() {
  const questionsContainer = document.getElementById("questions_container");
  const idx = questionCount++;
  const box = document.createElement("div");
  box.className = "box question-box mb-5";
  box.innerHTML = `
    <div class="field">
      <label class="label">Question Type</label>
      <div class="control">
        <div class="select is-purple is-fullwidth">
          <select name="questions[${idx}][type]" onchange="toggleOptions(this)">
            <option value="radio">Single choice</option>
            <option value="checkbox">Multiple choice</option>
            <option value="text">Text response</option>
          </select>
        </div>
      </div>
    </div>
    <div class="field">
      <label class="label">Question</label>
      <div class="control">
        <input
          class="input is-purple"
          type="text"
          name="questions[${idx}][text]"
          placeholder="Enter your question"
          required />
      </div>
    </div>
    <div class="field options-container">
      <label class="label">Options</label>
      <div class="options-list"></div>
      <button
        type="button"
        class="button is-small is-purple mt-2"
        onclick="addOption(this)">
        + Add Option
      </button>
    </div>
    <button
      type="button"
      class="button is-danger is-small mt-2"
      onclick="removeQuestion(this)">
      Remove Question
    </button>
  `;
  questionsContainer.appendChild(box);

  const select = box.querySelector("select");
  toggleOptions(select);
}

function renderOption(questionIdx, optionIdx, type) {
  // type: "radio" | "checkbox"
  return `
    <div class="field is-flex is-align-items-center mb-2 option-row">
      <label class="radio mr-2" style="pointer-events:none; margin-bottom:0;">
        <input type="${type}" disabled style="vertical-align:middle;">
      </label>
      <input class="input is-purple option-input" type="text" name="questions[${questionIdx}][options][]" placeholder="Option ${optionIdx + 1}" required style="flex:1;">
    </div>
  `;
}

function addOption(btn) {
  const questionBox = btn.closest(".question-box");
  const optionsList = questionBox.querySelector(".options-list");
  const select = questionBox.querySelector("select");
  const type = select.value;
  const questionIdx = getQuestionIdx(questionBox);
  const optionIdx = optionsList.querySelectorAll(".option-row").length;
  optionsList.insertAdjacentHTML("beforeend", renderOption(questionIdx, optionIdx, type));
}

function toggleOptions(select) {
  const questionBox = select.closest(".question-box");
  const optionsContainer = questionBox.querySelector(".options-container");
  const optionsList = optionsContainer.querySelector(".options-list");
  const type = select.value;
  const questionIdx = getQuestionIdx(questionBox);

  if (type === "radio" || type === "checkbox") {
    optionsContainer.style.display = "";
    optionsList.innerHTML = "";
    optionsList.insertAdjacentHTML("beforeend", renderOption(questionIdx, 0, type));
    optionsList.insertAdjacentHTML("beforeend", renderOption(questionIdx, 1, type));
    optionsContainer.querySelector("button").style.display = "";
  } else {
    // Text response: Show only 1 answer input
    optionsContainer.style.display = "";
    optionsList.innerHTML = `
      <div class="field mb-2">
        <input class="input is-purple" type="text" name="questions[${questionIdx}][text_response]" placeholder="User's answer will appear here" disabled>
      </div>
    `;
    optionsContainer.querySelector("button").style.display = "none";
  }
}

function getQuestionIdx(questionBox) {
  const input = questionBox.querySelector('input[name^="questions"]');
  return input ? input.name.match(/\d+/)[0] : 0;
}

function removeQuestion(btn) {
  btn.closest(".question-box").remove();
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".question-box select").forEach(toggleOptions);
});

window.addQuestion = addQuestion;
window.addOption = addOption;
window.toggleOptions = toggleOptions;
window.removeQuestion = removeQuestion;

window.onload = toggleOptions;

window.addOption = addOption;
window.toggleOptions = toggleOptions;