/* Story artwork for campaign cutscenes (ด่าน 1, 2). Chapter one dialogue is set in its scene initializer. */
(function () {
  'use strict';
  const base = new URL('./', document.currentScript.src).href;
  const base2 = new URL('../chapter-2/', base).href;
  const base3 = new URL('../chapter-3/', base).href;
  const base4 = new URL('../chapter-4/', base).href;
  const base5 = new URL('../chapter-5/', base).href;
  const base6 = new URL('../chapter-6/', base).href; // v426
  // v397: ตั้งค่าต่อด่าน — ภาพฉาก (แนวนอน/แนวตั้ง), ตัวละคร, ตำแหน่งเท้า (พิกัดในภาพ), ขอบบนที่ยอมตัด
  const CONFIGS = {
    1: { title: 'ด่าน 1 · ชานเมือง', leader: 'captain', bgL: base + 'village.webp', bgP: base + 'village-portrait.webp',
      sprites: {}, portraits: {}, feetL: 625, feetP: 900, cutL: 60, cutP: 150 },
    2: { title: 'ด่าน 2 · หมู่บ้าน', leader: 'sara', bgL: base2 + 'village.webp', bgP: base2 + 'village-portrait.webp',
      sprites: { sara: base2 + 'sara.png' }, portraits: { sara: base2 + 'portrait-sara.png' }, feetL: 620, feetP: 935, cutL: 20, cutP: 100 },
    3: { title: 'ด่าน 3 · ในเมือง', leader: 'ray', bgL: base3 + 'village.webp', bgP: base3 + 'village-portrait.webp',
      sprites: { ray: base3 + 'ray.png' }, portraits: { ray: base3 + 'portrait-ray.png' }, feetL: 640, feetP: 930, cutL: 20, cutP: 100 },
    4: { title: 'ด่าน 4 · ฤดูหนาว', leader: 'leena', bgL: base4 + 'village.webp', bgP: base4 + 'village-portrait.webp',
      sprites: { leena: base4 + 'leena.png' }, portraits: { leena: base4 + 'portrait-leena.png' }, feetL: 640, feetP: 960, cutL: 20, cutP: 100 },
    5: { title: 'ด่าน 5 · แนวป้องกัน', leader: 'bronze', bgL: base5 + 'village.webp', bgP: base5 + 'village-portrait.webp',
      sprites: { bronze: base5 + 'bronze.png' }, portraits: { bronze: base5 + 'portrait-bronze.png' }, feetL: 630, feetP: 740, cutL: 20, cutP: 100 },
    6: { title: 'ด่าน 6 · ฐานเสบียงใหญ่', leader: 'vance', bgL: base6 + 'village.webp', bgP: base6 + 'village-portrait.webp',
      sprites: { vance: base6 + 'vance.png' }, portraits: { vance: base6 + 'portrait-vance.png' }, feetL: 650, feetP: 905, cutL: 20, cutP: 100 } // v426
  };
  function initStoryArt(el, cfg, steps) {
    const hasW = Array.isArray(steps) && steps.some((x) => x && x.k === 'W'); // v407: คนตัดไม้ยืนในขบวนเฉพาะด่านที่มีบท
    el.classList.add('chapter-one-art');
    el.querySelector('.stage').style.setProperty('--bgfull', "url('" + cfg.bgL + "')");
    const stage = el.querySelector('.stage');
    const dlg = el.querySelector('.dlg');
    const cast = document.createElement('div');
    cast.className = 'cast';
    const actors = {};
    ['cart', 'soldier', 'soldier', cfg.leader, 'farmer'].concat(hasW ? ['woodcutter'] : []).forEach((name) => {
      const img = new Image();
      img.className = 'actor ' + name;
      img.alt = '';
      img.draggable = false;
      img.src = (cfg.sprites[name] || base + name + '.png') + '?v=430'; // v430: กันแคชรูปเก่า
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
        const name = step.k === 'L' ? cfg.leader : step.k === 'F' ? 'farmer' : step.k === 'W' ? 'woodcutter' : null;
        portrait.hidden = !name;
        dlg.classList.toggle('no-portrait', !name);
        dlg.classList.toggle('no-plate', step.k === 'N' || step.k === 'G');
        dlg.classList.toggle('side-r', name === 'farmer' || name === 'woodcutter'); // ชาวนาพูด: รูปหน้า+ป้ายชื่ออยู่ขวา
        dlg.classList.toggle('flip-p', name === 'bronze' || name === 'vance'); // v427: รูปครึ่งตัวที่ต้นฉบับหันซ้าย → กลับด้านให้หันเข้าหาข้อความ
        if (name) portrait.src = (cfg.portraits[name] || base + 'portrait-' + name + '.png') + '?v=430';
        Object.entries(actors).forEach(([key, img]) => img.classList.toggle('speaking', key === name));
      }
    };
  }
  window.initChapterOneStoryArt = (el, steps) => {
    const dialogue = [
      ["L","ชาวบ้านทุกคน ฟังทางนี้! ตอนนี้ค่ายทหารขาดเสบียง ต้องใช้ข้าวสาลีกับอ้อยด่วน"],
      ["F","ข้าวสาลีกับอ้อยหมู่บ้านเราพอมีครับท่าน ไม่ทราบว่าท่านนายพลต้องการเท่าไหร่ครับ"],
      ["L","เราต้องการอย่างละ 30 ตัน!"],
      ["F","แต่ปีนี้ฝนแล้ง ผลผลิตไม่ค่อยดี ของจำนวนมากขนาดนั้น เกรงว่าจะส่งให้ไม่ทัน"],
      ["L","ไม่มีเวลาบ่น ส่งให้ครบภายในเวลาที่กำหนด เราจะจ่ายค่าตอบแทนให้คุ้มค่าแน่นอน"],
      ["W","ถ้าอย่างนั้น ผมจะรีบตัดไม้แล้วเอามาสร้างที่พักให้กับแรงงานเกษตรกรเพิ่มขึ้นครับ"],
      ["L","ดี! เริ่มเดี๋ยวนี้เลย!"]
    ];
    let right = 'F';
    const lines = dialogue.map(([k, text]) => {
      if (k !== 'L') right = k;
      return { k, text, right };
    });
    steps.splice(1, steps.length - 2, ...lines);
    return initStoryArt(el, CONFIGS[1], steps);
  };
  window.initChapterTwoStoryArt = (el, steps) => initStoryArt(el, CONFIGS[2], steps);
  window.initChapterThreeStoryArt = (el, steps) => initStoryArt(el, CONFIGS[3], steps);
  window.initChapterFourStoryArt = (el, steps) => initStoryArt(el, CONFIGS[4], steps);
  window.initChapterFiveStoryArt = (el, steps) => initStoryArt(el, CONFIGS[5], steps);
  window.initChapterSixStoryArt = (el, steps) => initStoryArt(el, CONFIGS[6], steps); // v426
})();
