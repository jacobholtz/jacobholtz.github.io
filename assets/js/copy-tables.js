document.addEventListener('DOMContentLoaded', function () {
  var COPY_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><rect x="5.5" y="5.5" width="9" height="9" rx="1.3"/><path d="M3.5 10.2h-.75A1.25 1.25 0 011.5 8.95v-6.2A1.25 1.25 0 012.75 1.5h6.2a1.25 1.25 0 011.25 1.25v.75"/></svg>';
  var CHECK_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5l3 3 7-7.5"/></svg>';

  // Wraps `el` in a positioned container with a copy button in its corner.
  // `getText` runs on click, so the copied text is read from the live DOM.
  function addCopyButton(el, wrapClass, label, getText) {
    var wrap = document.createElement('div');
    wrap.className = wrapClass;
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'table-copy-btn';
    btn.setAttribute('aria-label', label);
    btn.title = label;
    btn.innerHTML = COPY_ICON;
    wrap.appendChild(btn);

    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(getText()).then(function () {
        btn.innerHTML = CHECK_ICON;
        btn.classList.add('table-copy-btn--copied');
        btn.title = 'Copied';
        setTimeout(function () {
          btn.innerHTML = COPY_ICON;
          btn.classList.remove('table-copy-btn--copied');
          btn.title = label;
        }, 1400);
      });
    });
  }

  document.querySelectorAll('.post-content table').forEach(function (table) {
    addCopyButton(table, 'table-wrap', 'Copy table', function () {
      var rows = table.querySelectorAll('tr');
      return Array.prototype.map.call(rows, function (row) {
        var cells = row.querySelectorAll('th, td');
        return Array.prototype.map.call(cells, function (cell) {
          return cell.textContent.trim();
        }).join('\t');
      }).join('\n');
    });
  });

  // Code blocks (detection queries, rules). The button sits on a wrapper
  // outside the <pre>, so it stays put when a long line scrolls sideways.
  document.querySelectorAll('.post-content pre').forEach(function (pre) {
    addCopyButton(pre, 'code-wrap', 'Copy code', function () {
      return pre.textContent.replace(/\n$/, '');
    });
  });
});
