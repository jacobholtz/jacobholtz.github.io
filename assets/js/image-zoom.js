document.addEventListener('DOMContentLoaded', function () {
  var images = document.querySelectorAll('.post-content img');
  if (!images.length) return;

  var overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Image preview');

  var fullImage = document.createElement('img');
  fullImage.className = 'lightbox__image';
  overlay.appendChild(fullImage);

  var closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'lightbox__close';
  closeBtn.setAttribute('aria-label', 'Close');
  closeBtn.innerHTML = '&times;';
  overlay.appendChild(closeBtn);

  document.body.appendChild(overlay);

  var trigger = null;

  function open(image) {
    trigger = image;
    fullImage.src = image.src;
    fullImage.alt = image.alt || '';
    overlay.classList.add('lightbox--open');
    document.documentElement.classList.add('lightbox-open');
    closeBtn.focus();
  }

  function close() {
    overlay.classList.remove('lightbox--open');
    document.documentElement.classList.remove('lightbox-open');
    fullImage.src = '';
    if (trigger) trigger.focus();
  }

  images.forEach(function (image) {
    image.tabIndex = 0;
    image.setAttribute('role', 'button');
    image.setAttribute('aria-label', 'Click to zoom in on this image');

    image.addEventListener('click', function () { open(image); });
    image.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(image);
      }
    });
  });

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) close();
  });
  closeBtn.addEventListener('click', close);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('lightbox--open')) close();
  });
});
