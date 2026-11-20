/* Story artwork for campaign cutscenes (ด่าน 1, 2). Campaign text, goals and start callbacks stay in index.html. */
(function () {
  'use strict';
  const base = new URL('./', document.currentScript.src).href;
  const base2 = new URL('../chapter-2/', base).href;
  // v397: ตั้งค่าต่อด่าน — ภาพฉาก (แนวนอน/แนวตั้ง), ตัวละคร, ตำแหน่งเท้า (พิกัดในภาพ), ขอบบนที่ยอมตัด
  const CONFIGS = {
    1: { title: 'ด่าน 1 · ชานเมือง', leader: 'captain', bgL: base + 'village.webp', bgP: base + 'village-portrait.webp',
      sprites: {}, portraits: {}, feetL: 625, feetP: 900, cutL: 60, cutP: 150 },
    2: { title: 'ด่าน 2 · หมู่บ้าน', leader: 'sara', bgL: base2 + 'village.webp', bgP: base2 + 'village-portrait.webp',
      sprites: { sara: base2 + 'sara.png' }, portraits: { sara: base2 + 'portrait-sara.png' }, feetL: 620, feetP: 935, cutL: 20, cutP: 100 }
  };
  function initStoryArt(el, cfg) {
    el.classList.add('chapter-one-art');
    el.querySelector('.stage').style.setProperty('--bgfull', "url('" + cfg.bgL + "')");
    const stage = el.querySelector('.stage');
    const dlg = el.querySelector('.dlg');
    const cast = document.createElement('div');
    cast.className = 'cast';
    const actors = {};
    ['cart', 'soldier', 'soldier', cfg.leader, 'farmer'].forEach((name) => {
      const img = new Image();
      img.className = 'actor ' + name;
      img.alt = '';
      img.draggable = false;
      img.src = cfg.sprites[name] || base + name + '.png';
      const wrap = document.createElement('span'); // v396: ห่อรูป เพื่อวางเงาวงรีใต้เท้า (ไม่พึ่ง drop-shadow ของเบราว์เซอร์)
      wrap.className = 'aw ' + name;
      wrap.appendChild(img);
      cast.appendChild(wrap);
      actors[name] = img;
    });
    const title = document.createElement('div');
    title.className = 'chapter-title';
    title.textContent = cfg.title;
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
      let scale, imgW, imgH, top, feet;
      if (width < height) {
        // จอแนวตั้ง (v392): ใช้ภาพแนวตั้ง 1024x1536 · คลุมเต็มจอ ไม่ตัดมากเกินจำเป็น
        scale = Math.max(width / 1024, height / 1536);
        imgW = 1024 * scale; imgH = 1536 * scale;
        // v394: กันที่ให้กรอบแบบสูงสุด (หน้าเป้าหมาย) เสมอ → ฉากไม่ขยับตามความสูงกรอบ, เท้าตัวละครอยู่เหนือกรอบ มีหญ้าเหลือเล็กน้อย
        // หลังคา/ปล่องควันยังเห็น (ตัดบนไม่เกิน 150 พิกเซลของภาพ) · ภาพคลุมเต็มจอเสมอ
        const freeRef = height - Math.max(dh, 290);
        top = Math.min(0, Math.max(height - imgH, -cfg.cutP * scale, freeRef - (cfg.feetP + 90) * scale));
        feet = top + cfg.feetP * scale;
        bg.style.backgroundImage = "url('" + cfg.bgP + "')";
        bg.style.webkitMaskImage = bg.style.maskImage = 'none';
      } else {
        scale = Math.max(width / 1536, 0.8 * free / 1024);
        imgW = 1536 * scale; imgH = 1024 * scale;
        // v395: เห็นหลังคา/ปล่องครบ (ตัดบนไม่เกิน 60px ของภาพ) ส่วนเกินตัดจากล่าง (กรอบบังอยู่) · เท้าตัวละครต้องอยู่เหนือกรอบ · ภาพคลุมเต็มจอ
        const freeRef = height - Math.max(dh, Math.min(275, height * 0.45)); // กันที่ให้กรอบแบบสูงสุด (หน้าเป้าหมาย) ฉากจะได้ไม่ขยับ
        top = Math.max(height - imgH - 8, Math.min(-cfg.cutL * scale, freeRef - (cfg.feetL + 25) * scale)); // -8 = ยอมให้ขอบล่างภาพสูงขึ้นได้เล็กน้อย (ใต้กรอบ)
        feet = top + cfg.feetL * scale;
        bg.style.backgroundImage = "url('" + cfg.bgL + "')";
        bg.style.webkitMaskImage = bg.style.maskImage = '';
      }
      bg.style.width = imgW + 'px';
      bg.style.height = imgH + 'px';
      bg.style.left = (width - imgW) / 2 + 'px';
      bg.style.top = top + 'px';
      cast.style.width = 520 * scale + 'px';
      cast.style.height = Math.max(30, 100 * scale) + 'px';
      cast.style.gap = Math.max(4, 14 * scale) + 'px';
      cast.style.top = feet + 'px';
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
        const name = step.k === 'L' ? cfg.leader : step.k === 'F' ? 'farmer' : null;
        portrait.hidden = !name;
        dlg.classList.toggle('no-portrait', !name);
        dlg.classList.toggle('no-plate', step.k === 'N' || step.k === 'G');
        dlg.classList.toggle('side-r', name === 'farmer'); // ชาวนาพูด: รูปหน้า+ป้ายชื่ออยู่ขวา
        if (name) portrait.src = cfg.portraits[name] || base + 'portrait-' + name + '.png';
        Object.entries(actors).forEach(([key, img]) => img.classList.toggle('speaking', key === name));
      }
    };
  }
  window.initChapterOneStoryArt = (el) => initStoryArt(el, CONFIGS[1]);
  window.initChapterTwoStoryArt = (el) => initStoryArt(el, CONFIGS[2]);
})();
