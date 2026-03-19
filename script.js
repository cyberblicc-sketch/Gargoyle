// Simple form submission handler (demo only)
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for your message! Our team will reach out soon.');
    form.reset();
  });
}
