document.addEventListener('DOMContentLoaded', function () {
  var content = document.querySelector('.post-content');
  if (!content) return;

  var headings = content.querySelectorAll('h2[id], h3[id], h4[id]');
  if (headings.length < 2) return;

  var toc = document.createElement('nav');
  toc.className = 'post-toc';
  toc.setAttribute('aria-label', 'Table of contents');

  var title = document.createElement('h2');
  title.className = 'post-toc__title';
  title.textContent = 'Contents';
  toc.appendChild(title);

  var rootList = document.createElement('ol');
  toc.appendChild(rootList);

  // Nest by heading level. `list` is created lazily on an entry the first
  // time something deeper turns up beneath it, so a flat post (all h3, as
  // most writeups are) produces a single <ol> with no empty children.
  var stack = [{ level: 0, list: rootList, item: null }];

  headings.forEach(function (heading) {
    var level = parseInt(heading.tagName.charAt(1), 10);
    while (stack.length > 1 && stack[stack.length - 1].level >= level) stack.pop();

    var parent = stack[stack.length - 1];
    if (!parent.list) {
      parent.list = document.createElement('ol');
      parent.item.appendChild(parent.list);
    }

    var item = document.createElement('li');
    var link = document.createElement('a');
    link.href = '#' + heading.id;
    link.textContent = heading.textContent.trim();
    // Pinned entries are clamped to one line, so keep the full text reachable.
    link.title = link.textContent;
    item.appendChild(link);
    parent.list.appendChild(item);

    stack.push({ level: level, list: null, item: item });
  });

  // One TOC serves both layouts: pinned in the left margin on wide screens,
  // left in the flow at the top of the post on narrow ones. Either way it has
  // to be inserted ahead of the first heading, or the inline fallback would
  // land at the foot of the article.
  content.insertBefore(toc, headings[0]);

  var links = toc.querySelectorAll('a');

  // The active entry is the last heading to have crossed ACTIVE_LINE. Measured
  // live rather than cached, because images load late and shift the headings.
  var ACTIVE_LINE = 120;
  var currentIndex = -1;

  function updateCurrentSection() {
    var active = -1;
    for (var i = 0; i < headings.length; i++) {
      if (headings[i].getBoundingClientRect().top > ACTIVE_LINE) break;
      active = i;
    }

    // Nothing can cross the line once the page bottom is reached, so a final
    // section shorter than the viewport would otherwise never light up.
    if (window.innerHeight + window.pageYOffset >=
        document.documentElement.scrollHeight - 2) {
      active = headings.length - 1;
    }

    if (active === currentIndex) return;
    currentIndex = active;
    links.forEach(function (link, i) {
      link.classList.toggle('is-current', i === active);
    });
  }

  // Start the rail level with the post title, then let it ride up with the
  // page until it reaches TOC_MIN_TOP and hold. position:sticky would do this,
  // but the rail is fixed and out of the flow, so it has no containing block
  // to stick within. Below the pinning breakpoint the rail is static and
  // ignores `top`, making this a no-op there.
  var TOC_MIN_TOP = 40;
  var anchor = document.querySelector('.post-header__title');

  function updateTocTop() {
    if (!anchor) return;
    var anchored = anchor.getBoundingClientRect().top;
    toc.style.top = Math.max(TOC_MIN_TOP, anchored) + 'px';
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      updateTocTop();
      updateCurrentSection();
      ticking = false;
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  updateTocTop();
  updateCurrentSection();
});
