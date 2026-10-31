(function () {
  // Menu no celular
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // E-mail montado no navegador (evita coleta automática por robôs)
  document.querySelectorAll('[data-email]').forEach(function (el) {
    var addr = el.getAttribute('data-u') + '@' + el.getAttribute('data-d');
    var subject = el.getAttribute('data-subject');
    if (el.tagName === 'A') {
      el.href = 'mailto:' + addr + (subject ? '?subject=' + encodeURIComponent(subject) : '');
    }
    if (el.hasAttribute('data-show')) el.textContent = addr;
  });
  document.querySelectorAll('.copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var addr = b.getAttribute('data-u') + '@' + b.getAttribute('data-d');
      var done = b.getAttribute('data-done') || 'Copiado';
      var label = b.textContent;
      var ok = function () { b.textContent = done; setTimeout(function () { b.textContent = label; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(addr).then(ok, function () { selectText(b); });
      } else { selectText(b); }
    });
  });
  function selectText(b) {
    var target = b.parentNode.querySelector('.email');
    if (!target) return;
    var r = document.createRange(); r.selectNodeContents(target);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  // Filtro de publicações
  var list = document.getElementById('pub-list');
  if (list) {
    var items = Array.prototype.slice.call(list.querySelectorAll('.pub'));
    var chips = document.querySelectorAll('.chip[data-topic]');
    var search = document.getElementById('pub-search');
    var count = document.getElementById('pub-count');
    var empty = document.getElementById('pub-empty');
    var topic = 'all';
    var fmt = count ? count.getAttribute('data-fmt') : '{n}';
    var norm = function (s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };
    var apply = function () {
      var q = search ? norm(search.value.trim()) : '';
      var n = 0;
      items.forEach(function (li) {
        var okTopic = topic === 'all' || li.getAttribute('data-topic') === topic;
        var okText = !q || norm(li.textContent).indexOf(q) !== -1;
        li.hidden = !(okTopic && okText);
        if (!li.hidden) n++;
      });
      if (count) count.textContent = fmt.replace('{n}', n);
      if (empty) empty.hidden = n !== 0;
    };
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        topic = c.getAttribute('data-topic');
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
    apply();
  }
})();
