# v443: ไอคอนชุดใหม่จาก ChatGPT (3 แผ่น) ใส่แทนสัญลักษณ์เดิม
# ใช้: python3 tools/patch443.py index.html /path/icons443.json
import json, re, sys
path, ipath = sys.argv[1], sys.argv[2]
h = open(path, encoding='utf8').read()
I = json.load(open(ipath))

def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, (old[:80], n)
    h = h.replace(old, new)

# 1) ทะเบียนไอคอน v443 + ใช้แทนไอคอน UI เดิม (⚠ ✅ 💧 ⏸) และภาพสินค้า 8 ชนิด
reg = 'const ICON443 = ' + json.dumps(I) + ';\n'
rep("function uiIcon(name, size = 20) {",
    reg +
    "Object.assign(UI_ICON_SRC, { warning: ICON443.warn, check: ICON443.check, water: ICON443.drop, pause: ICON443.pause, hat: ICON443.hat }); // v443\n"
    "Object.assign(ITEM_IMG, { flour: ICON443.flour, sugar: ICON443.sugar, salt: ICON443.salt, wood: ICON443.wood, butter: ICON443.butter, waterdrum: ICON443.waterBarrel, crude: ICON443.oilBarrel, energy: ICON443.energy }); // v443: สินค้ารอขนหน้าอาคาร\n"
    "window.ICON443 = ICON443;\n"
    "function ico443(n, css) { return `<img src=\"${ICON443[n]}\" alt=\"\" draggable=\"false\" style=\"${css || 'width:1.25em;height:1.25em;vertical-align:-0.3em'};image-rendering:auto\">`; }\n"
    "function uiIcon(name, size = 20) {")
# 🎓 ในข้อความ → หมวก (ใส่ในรายการแปลงอีโมจิอัตโนมัติ)
rep("'✅': 'check', '📜': 'scroll' }; // v285", "'✅': 'check', '📜': 'scroll', '🎓': 'hat' }; // v285 · v443: 🎓 = หมวกบทเรียน")

# 2) หัวกล่องบทเรียน: หมวก + ปุ่มย่อ/ขยาย
rep("head.innerHTML = `<span>🎓 ${st.title}</span><span style=\"font-size:12px;opacity:.7;white-space:nowrap\">${tut.i + 1}/${TUT_STEPS.length} ${tut.min ? '▾' : '▴'}</span>",
    "head.innerHTML = `<span>${ico443('hat', 'width:24px;height:24px;vertical-align:-6px;margin-right:4px')}${st.title}</span><span style=\"font-size:12px;white-space:nowrap;display:inline-flex;align-items:center;gap:5px\"><span style=\"opacity:.7\">${tut.i + 1}/${TUT_STEPS.length}</span>${ico443(tut.min ? 'tutExpand' : 'tutCollapse', 'width:26px;height:26px')}</span>")

# 3) ที่จับลากการ์ด
rep("  grip.textContent = '⠿';\n  grip.style.cssText = 'flex:none;color:#a07a4a;font-size:16px;';",
    "  grip.innerHTML = ico443('handle', 'width:30px;height:auto;display:block'); // v443\n  grip.style.cssText = 'flex:none;cursor:grab;';")

# 4) ปุ่มกลับเมนู / แสดงเมนู
rep("  exit.textContent = '☰ แสดงเมนู';", "  exit.innerHTML = ico443('menu', 'width:22px;height:22px;vertical-align:-5px;margin-right:5px') + 'แสดงเมนู'; // v443")
# แผงเครื่องมือ: ปุ่มกลับเมนู ใช้ไอคอนบ้าน+ลูกศร
rep("    b.style.setProperty('--i', 'url(' + I[key] + ')');",
    "    b.style.setProperty('--i', 'url(' + (key === 'house' ? ICON443.backMenu : I[key]) + ')'); // v443")
# สวิตช์ ON/OFF ใช้ภาพ
rep("  const TOG = ['layers', 'lock', 'cloud', 'flask', 'spk', 'bat'];",
    "  const TOG = ['layers', 'lock', 'cloud', 'flask', 'spk', 'bat'];\n"
    "  (function () { const s = document.createElement('style'); s.textContent = `button.b358[data-sw]::after{content:\"\"!important;width:50px!important;height:31px!important;border:none!important;border-radius:0!important;padding:0!important;box-shadow:none!important;background:url(${ICON443.swOn}) center/contain no-repeat!important;}button.b358[data-sw=\"0\"]::after{background:url(${ICON443.swOff}) center/contain no-repeat!important;}`; document.head.appendChild(s); })(); // v443")

# 5) ฉากบทสนทนา: ปุ่มอ่านต่อ / ข้ามฉาก
rep("    if (typeof artFn === 'function') { try { art = artFn(el, steps); } catch (e) { art = null; } }",
    "    if (typeof artFn === 'function') { try { art = artFn(el, steps); } catch (e) { art = null; } }\n"
    "    { const t443 = nx.textContent.replace('▶', '').trim(); nx.innerHTML = (t443 ? t443 + ' ' : '') + ico443('next', 'width:26px;height:26px;vertical-align:middle'); nx.style.display = nx.style.display; } // v443\n"
    "    $('.skip').innerHTML = 'ข้าม ' + ico443('skip', 'width:24px;height:24px;vertical-align:-6px'); // v443")

# 6) ภาพบนกระดาน: ป้ายพัก, Z ลอย, ลูกศรชี้คนงาน, ป้ายสถานะ, สัญลักษณ์ถือของ
rep("""  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.beginPath();
  ctx.arc(cx, top, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffd166';
  ctx.fillRect(cx - r * 0.45, top - r * 0.5, r * 0.3, r);
  ctx.fillRect(cx + r * 0.15, top - r * 0.5, r * 0.3, r);
  ctx.restore();""",
"""  const pim = artImg('i443_pause', ICON443.pause); // v443: ป้ายพักแบบภาพ
  if (pim) { ctx.drawImage(pim, cx - r * 1.15, top - r * 1.15, r * 2.3, r * 2.3); ctx.restore(); return; }
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.beginPath();
  ctx.arc(cx, top, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffd166';
  ctx.fillRect(cx - r * 0.45, top - r * 0.5, r * 0.3, r);
  ctx.fillRect(cx + r * 0.15, top - r * 0.5, r * 0.3, r);
  ctx.restore();""")

rep("""function drawSleepZ(cx, cy, now) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);""",
"""function drawSleepZ(cx, cy, now) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  { const zim = artImg('i443_zzz', ICON443.zzz); // v443: Z ลอยแบบภาพ (ลอยขึ้นลงช้าๆ จางเข้าออก)
    if (zim) { const s = Math.max(16, 20 * viewZoom) * uiK381(), ph = (now % 2400) / 2400;
      ctx.save(); ctx.globalAlpha = 0.75 + 0.25 * Math.sin(ph * Math.PI * 2);
      ctx.drawImage(zim, cx - s * 0.2, cy - 30 * viewZoom - s - Math.sin(ph * Math.PI * 2) * 3 * viewZoom, s, s * zim.height / zim.width);
      ctx.restore(); return; } }""")

rep("""  const bob = Math.sin(now / 180) * 3 * F;
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.beginPath();
  ctx.moveTo(cx - half, cy - half * 1.5 + bob);""",
"""  const bob = Math.sin(now / 180) * 3 * F;
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const aim = artImg('i443_arrow', ICON443.arrowDown); // v443: ลูกศรชี้คนงานแบบภาพ
  if (aim) { const w = half * 2.4, hh = w * aim.height / aim.width; ctx.drawImage(aim, cx - w / 2, cy - hh + bob, w, hh); ctx.restore(); return; }
  ctx.beginPath();
  ctx.moveTo(cx - half, cy - half * 1.5 + bob);""")

# ป้ายสถานะอาคาร: ภาพป้ายวงกลมสำเร็จรูป
rep("""  const pulse = 1 + 0.08 * Math.sin(performance.now() / 220);
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.beginPath();
  ctx.arc(cx, top, r * pulse, 0, Math.PI * 2);""",
"""  const pulse = 1 + 0.08 * Math.sin(performance.now() / 220);
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const b443 = BADGE443[r0.icon] && !r0.kind ? artImg('i443_' + BADGE443[r0.icon], ICON443[BADGE443[r0.icon]]) : null; // v443
  if (b443) { const d = r * 2.3 * pulse; ctx.drawImage(b443, cx - d / 2, top - d / 2, d, d); ctx.restore(); return; }
  ctx.beginPath();
  ctx.arc(cx, top, r * pulse, 0, Math.PI * 2);""")
rep("function drawStopMark(c, x, y, now) {",
    "const BADGE443 = { '⛔': 'stNoRoad', '📦': 'stFull', '❗': 'stWarn', '💧': 'stWater' }; // v443: ป้ายสถานะอาคาร\n"
    "const LUMBER443 = { 'รอต้นไม้โต': 'stGrow', 'ไม่มีคลังไม้ว่าง': 'stWood' };\n"
    "function drawStopMark(c, x, y, now) {")
rep("""  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.beginPath(); ctx.arc(cx, top, r, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.fill();""",
"""  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const l443 = LUMBER443[reason] ? artImg('i443_' + LUMBER443[reason], ICON443[LUMBER443[reason]]) : (m[1] === '#e53935' ? artImg('i443_stNoRoad', ICON443.stNoRoad) : null); // v443
  if (l443) { const d = r * 2.3; ctx.drawImage(l443, cx - d / 2, top - d / 2, d, d); ctx.restore(); return; }
  ctx.beginPath(); ctx.arc(cx, top, r, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.fill();""")

# สัญลักษณ์ถือของ: น้ำ = สี่เหลี่ยมฟ้า, ของอื่น = ข้าวหลามตัดเขียว
rep("""    ctx.fillStyle = colors[carryKind] || fallback;
    ctx.beginPath();
    ctx.arc(cx + 6, cy - 6, 3, 0, Math.PI * 2);
    ctx.fill();""",
"""    const c443 = artImg(CARRY_BLUE443.has(carryKind) ? 'i443_cb' : 'i443_cg', CARRY_BLUE443.has(carryKind) ? ICON443.carryBlue : ICON443.carryGreen); // v443
    if (c443) { const s = Math.max(7, 6 * viewZoom); ctx.drawImage(c443, cx + 6 - s / 2, cy - 6 - s / 2, s, s); return; }
    ctx.fillStyle = colors[carryKind] || fallback;
    ctx.beginPath();
    ctx.arc(cx + 6, cy - 6, 3, 0, Math.PI * 2);
    ctx.fill();""")
rep("function drawWorkerAt(cx, cy, shirt, carry, carryKind, colors, fallback, pose) {",
    "const CARRY_BLUE443 = new Set(['water', 'waterdrum', 'brine']); // v443\nfunction drawWorkerAt(cx, cy, shirt, carry, carryKind, colors, fallback, pose) {")

open(path, 'w', encoding='utf8').write(h)
print('ok')
