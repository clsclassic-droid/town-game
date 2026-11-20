/* Chapter 1 artwork only. Campaign text, goals and start callbacks stay in index.html. */
(function () {
  'use strict';
  const base = new URL('./', document.currentScript.src).href;
  window.initChapterOneStoryArt = function (el) {
    el.classList.add('chapter-one-art');
    const stage = el.querySelector('.stage');
    const dlg = el.querySelector('.dlg');
    const cast = document.createElement('div');
    cast.className = 'cast';
    const actors = {};
    ['cart', 'soldier', 'soldier', 'captain', 'farmer'].forEach((name) => {
      const img = new Image();
      img.className = 'actor ' + name;
      img.alt = '';
      img.draggable = false;
      img.src = base + name + '.png';
      cast.appendChild(img);
      actors[name] = img;
    });
    const title = document.createElement('div');
    title.className = 'chapter-title';
    title.textContent = 'ด่าน 1 · ชานเมือง';
    // v391: ภาพฉากวางเองใน .bgfit (ไม่ซูมตัดข้างมาก) · ส่วนที่เหลือเติมด้วยภาพเบลอ · ตัวละครผูกกับขนาดฉาก
    const bg = document.createElement('div');
    bg.className = 'bgfit';
    stage.prepend(bg);
    stage.append(title, cast);
    const positionCast = () => {
      const { width, height } = stage.getBoundingClientRect();
      if (!width || !height) return;
      const dh = dlg.offsetHeight || 0;
      const free = Math.max(120, height - dh);           // พื้นที่เหนือกรอบบทสนทนา
      const scale = Math.max(width / 1536, 0.8 * free / 1024);
      const imgW = 1536 * scale, imgH = 1024 * scale;
      const top = (free - imgH) / 2;                      // ติดลบ = ตัดบน/ล่างเท่าๆ กัน
      bg.style.width = imgW + 'px';
      bg.style.height = imgH + 'px';
      bg.style.left = (width - imgW) / 2 + 'px';
      bg.style.top = top + 'px';
      const ch = Math.max(30, 100 * scale);
      cast.style.width = 520 * scale + 'px';
      cast.style.height = ch + 'px';
      cast.style.gap = Math.max(4, 14 * scale) + 'px';
      cast.style.top = (top + 625 * scale) + 'px';
    };
    const observer = new ResizeObserver(positionCast);
    observer.observe(stage);
    observer.observe(dlg);
    positionCast();
    const portrait = new Image();
    portrait.className = 'dialogue-portrait';
    portrait.alt = '';
    portrait.draggable = false;
    dlg.appendChild(portrait);
    const next = el.querySelector('.nx');
    next.setAttribute('role', 'button');
    next.tabIndex = 0;
    next.setAttribute('aria-label', 'อ่านต่อ');
    next.textContent = 'ต่อไป ▶';
    next.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); next.click(); }
    });
    el.querySelector('.tx').setAttribute('aria-live', 'polite');
    return {
      close() { observer.disconnect(); },
      show(step) {
        const name = step.k === 'L' ? 'captain' : step.k === 'F' ? 'farmer' : null;
        portrait.hidden = !name;
        dlg.classList.toggle('no-portrait', !name);
        dlg.classList.toggle('no-plate', step.k === 'N' || step.k === 'G');
        if (name) portrait.src = base + 'portrait-' + name + '.png';
        Object.entries(actors).forEach(([key, img]) => img.classList.toggle('speaking', key === name));
      }
    };
  };
})();
