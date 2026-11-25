# v443: บทเรียนใหม่ตามแบบของบอสหนึ่ง — เริ่มจากแผนที่ว่าง สร้างทีละอย่าง จบที่ขายแป้ง
# ใช้: python3 tools/patch443_tut.py index.html
import sys
path = sys.argv[1]
h = open(path, encoding='utf8').read()

def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, (old[:90], n)
    h = h.replace(old, new)

# 1) แผนที่บทเรียน: แม่น้ำด้านบน ภูเขาด้านซ้าย ต้นไม้ 3 ต้นริมแม่น้ำ (ไม่มีสระ)
rep("""function tutTerrain() {
  return {""", """function tutTerrain() {
  if (TUT443) { // v443: แผนที่ว่าง แม่น้ำบน ภูเขาซ้าย ต้นไม้ 3 ต้นริมแม่น้ำ
    const borders = Object.fromEntries(BORDER_SLOTS.map((k) => [k, 'plains']));
    borders.top = 'river'; borders.topLeft = 'river'; borders.topRight = 'river';
    borders.left = 'mountain'; borders.bottomLeft = 'mountain';
    return { biome: 'plains', borders, features: T443.trees.map(([x, y]) => ({ type: 'tree', x, y })) };
  }
  return {""")

# 2) เริ่มบทเรียน: ล้างเมืองเริ่มต้น เหลือคลังไม้ที่มีไม้ 8 อัน + ต้นไม้
rep("""  if (TUT317) { useSide(humanSide); const ws = tutFind('woodshed'); if (ws) { const c = board[ws[1]][ws[0]]; c.stock = Math.max(c.stock || 0, TUT_WOOD317); } }""",
"""  if (TUT443) tutBoard443(); // v443: แผนที่ว่าง
  else if (TUT317) { useSide(humanSide); const ws = tutFind('woodshed'); if (ws) { const c = board[ws[1]][ws[0]]; c.stock = Math.max(c.stock || 0, TUT_WOOD317); } }""")

# 3) ขั้นบทเรียนชุดใหม่ (แทนชุดเดิมทั้งหมด)
NEW = r"""
// ==================== v443: บทเรียนแบบใหม่ (บอสหนึ่งออกแบบ) ====================
// แผนที่ว่าง → ข้าวสาลี → บ่อน้ำ → แถบทรัพยากร → ถนน → บ้านเกษตรกร → ไซโล → บ่อ 2 → บ่อ 3 (ไม้ไม่พอ)
// → บ้านคนตัดไม้ → บ่อ 3 → สระ (น้ำ 10) → ข้าวติดสระ/ห่าง 1/ไกล → แม่น้ำ + ระยะน้ำ
// → โรงโม่ (ถนนไปที่ไม่มีเงา) → ระยะเงา + ภูเขา → โรงโม่ในเงา → คลังสินค้า → เร่งเวลา → แป้ง 10 → สถานี → ขายแป้ง
const TUT443 = true;
const T443 = {
  trees: [[9, 0], [10, 0], [11, 0]], woodshed: [10, 8],
  field1: [[8, 13]], wells: [[7, 13], [9, 13], [8, 14]],
  road1: [[8, 9], [9, 9], [10, 9]], house: [[8, 8]], silo: [[9, 8]], lumber: [[10, 10]],
  pond: [[11, 13]], pfields: [[12, 13], [11, 15], [6, 13]], // สระใกล้บ่อ (เดินสั้น)
  road2: [[11, 9], [12, 9], [13, 9], [14, 9]], mill1: [[14, 8]],
  road3: [[7, 9], [6, 9], [5, 9], [4, 9], [3, 9]], mill2: [[3, 8]],
  store: [[13, 10]], depot: [[15, 11], [15, 12], [15, 13]],
};
const TUT443_WOOD = 8; // บ่อ 1 + บ้านเกษตรกร 1 + ไซโล 5 + บ่อ 2 = 8 → บ่อที่ 3 ไม้ไม่พอ
function tutBoard443() {
  useSide(humanSide);
  const now = gameNow();
  for (let y = 0; y < GRID_SIZE; y++) for (let x = 0; x < GRID_SIZE; x++) board[y][x] = null;
  for (const [x, y] of T443.trees) {
    const c = makeCell('tree', now, x, y);
    if (c) { c.water = c.need; c.growStart = now - c.growMs * 10; board[y][x] = c; }
  }
  const [wx, wy] = T443.woodshed;
  board[wy][wx] = makeCell('woodshed', now, wx, wy, { x: wx, y: wy + 1 });
  board[wy][wx].stock = TUT443_WOOD;
  try { clearPathCache(); } catch (e) { /* ไม่เป็นไร */ }
  try { updateStatus(); refreshToolbar(); } catch (e) { /* ไม่เป็นไร */ }
}
const $443 = (n) => '$' + Number(n).toLocaleString('en-US');
function cost443(t) { return `${$443(COST[t])}${WOOD_COST[t] ? ` + ไม้ ${WOOD_COST[t]}` : ''}`; }
function tutBase443(t) { tut.base443 = tut.base443 || {}; tut.base443[t] = countType(t); }
function tutAdded443(t) { return countType(t) - ((tut.base443 || {})[t] || 0); }
function tutUtil443(btn) { // ปุ่มในแผงเครื่องมือ: ยังไม่เปิดแผง = แท็บเครื่องมือ
  if (openRow === utilRow) return btn;
  const t = tabList.find((o) => o.row === utilRow); return t ? t.tab : null;
}
function tutUtilDo443(name) {
  return openRow === utilRow ? `👉 กดปุ่ม <b>${name}</b> (ปุ่มที่กะพริบ)` : '👉 กดแท็บ <b>เครื่องมือ</b> ที่แถบล่าง (ปุ่มที่กะพริบ)';
}
// ขั้นโรงโม่/คลังสินค้า/สถานี: เติมไม้ในคลังไม้ให้พอสร้าง (บทเรียนไม่ต้องรอไม้นาน คนตัดไม้ยังทำงานตามปกติ)
function tutWood443(need) {
  if (woodStock() >= need) return '';
  const p = tutFind('woodshed'); if (!p) return '';
  const c = board[p[1]][p[0]];
  c.stock = Math.min(BUILDINGS.woodshed.capacity, (c.stock || 0) + need - woodStock());
  if (!tut.woodMsg443) { tut.woodMsg443 = true; showMessage('🎁 บทเรียนแถมไม้ให้พอสร้าง (ปกติต้องรอคนตัดไม้)'); }
  try { updateStatus(); } catch (e) { /* ไม่เป็นไร */ }
  return '';
}
function closeUtil443() { try { if (openRow === utilRow) showGroup(null); } catch (e) { /* ไม่เป็นไร */ } }
function offRange443() { try { if (showRange) rangeBtn.click(); if (showShade324) shadeRangeBtn324.click(); } catch (e) { /* ไม่เป็นไร */ } }
function soldFlour443() { return (humanSide.produced.flour || 0) > 0; }
function tutWorker443(type) { const p = tutFind(type); return p ? board[p[1]][p[0]] : null; }
// ขั้นสร้างอาคาร: ปุ่มกะพริบ + ช่องแนะนำ + นับที่สร้างเพิ่มในขั้นนี้
function build443(type, tiles, n, title, text, extra) {
  return Object.assign({
    title, el: () => tutPick(type), enter: () => tutBase443(type),
    tiles: () => tutHold432(type, tiles.filter(([x, y]) => !board[y][x])), cam: () => tiles,
    done: () => tutAdded443(type) >= n,
    text: () => `${typeof text === 'function' ? text() : text}<br>${tutDo434(type)}`,
  }, extra || {});
}
function road443(tiles, title, text, pre) {
  return { title, el: () => tutPick('road'), enter: () => { if (pre) pre(); tutBase443('road'); },
    tiles: () => tutHold432('road', tutLeft(tiles, 'road')), cam: () => tiles,
    done: () => !tutLeft(tiles, 'road').length || tutAdded443('road') >= tiles.length,
    progress: () => `วางแล้ว ${Math.min(tiles.length, Math.max(tiles.length - tutLeft(tiles, 'road').length, tutAdded443('road')))}/${tiles.length} ช่อง`,
    text: () => `${text}<br>${tutDo434('road')}` };
}
const TUT_STEPS_443 = [
  { title: 'ยินดีต้อนรับสู่ SproutMill 👋', next: true, cam: () => [[3, 2], [14, 14]],
    text: () => `เราจะเริ่มจาก<b>ที่ดินว่างเปล่า</b> แล้วสร้างฟาร์มทีละอย่าง จนทำ<b>แป้ง</b>ไปขายได้<br>ทำตาม<b>ปุ่มและช่องที่กะพริบสีเหลือง</b>`},
  build443('field', T443.field1, 1, 'ปลูกข้าวสาลี', () => `เริ่มจากปลูก ${thumbHtml('field', 24)} <b>ทุ่งข้าวสาลี</b> 1 แปลง (${$443(COST.field)})`),
  build443('well', [T443.wells[0]], 1, 'ข้าวสาลีต้องการน้ำ 💧', () => `ข้าวสาลีจะโตได้ ต้องได้<b>น้ำ ${BUILDINGS.field.water} หน่วย</b>มารด<br>สร้าง ${thumbHtml('well', 24)} <b>บ่อน้ำ</b> ราคา <b>${$443(COST.well)}</b> และใช้<b>ไม้ ${WOOD_COST.well} อัน</b>`),
  { title: 'ดูทรัพยากรของคุณ', next: true, el: () => document.querySelector('.chip306.items306'),
    text: () => `แถบด้านบนบอกว่าตอนนี้มีอะไรเท่าไหร่<br>💰 <b>เงิน</b> ${$443(coins)}<br>${thumbHtml('woodshed', 24)} <b>ไม้ในคลังไม้</b> เหลือ <b>${kindStock('wood')}</b> อัน (ช่องที่กะพริบ)<br>สร้างอะไรก็จะหักเงินและไม้จากตรงนี้` },
  road443(T443.road1, 'ต้องมีคนรดน้ำ', `บ่อน้ำไม่รดน้ำเอง ต้องมี<b>คนงาน</b>จาก ${thumbHtml('farmhouse', 24)} <b>บ้านเกษตรกร</b> ตักน้ำไปรด<br>บ้านเกษตรกร<b>ต้องวางติดถนน</b>ถึงจะสร้างได้ มาวาง ${thumbHtml('road', 24)} <b>ถนน</b> ก่อน`),
  build443('farmhouse', T443.house, 1, 'สร้างบ้านเกษตรกร', () => `${thumbHtml('farmhouse', 24)} <b>บ้านเกษตรกร</b> ${cost443('farmhouse')} · คนงาน 1 คน มี<b>ค่าแรง</b>หักทุกนาที<br>⚠ ต้อง<b>ติดถนน</b> วางที่อื่นจะสร้างไม่ได้`),
  build443('silo', T443.silo, 1, 'สร้างไซโลเก็บข้าว', () => `ข้าวที่เก็บเกี่ยวได้ ต้องมีที่เก็บ สร้าง ${thumbHtml('silo', 24)} <b>ไซโล</b> ${cost443('silo')} · ต้อง<b>ติดถนน</b>`),
  { title: 'ดูเกษตรกรทำงาน', arrow443: 'farmhouse', next: true, cam: () => T443.field1.concat(T443.house, [T443.wells[0]]), minMs: 3000,
    done: () => { const c = tutWorker443('farmhouse'); return !!(c && c.farmer && (c.farmer.carryKind === 'water' || c.farmer.carryKind === 'wheat')); },
    text: 'ลูกศรแดงชี้<b>เกษตรกร</b> เขาจะไปตักน้ำที่บ่อ แล้วเดินไปรดข้าวสาลี<br>เมื่อข้าวโต เขาจะเก็บเกี่ยวแล้วขนไปเก็บในไซโล' },
  build443('well', [T443.wells[1]], 1, 'สร้างบ่อน้ำบ่อที่ 2', () => `บ่อ 1 บ่อตักได้ทีละ 1 ถัง แล้วต้องรอน้ำเติม<br>สร้าง ${thumbHtml('well', 24)} <b>บ่อน้ำบ่อที่ 2</b> (${cost443('well')}) ข้าวจะได้น้ำเร็วขึ้น`),
  { title: 'สร้างบ่อน้ำบ่อที่ 3', el: () => (tut.noWood443 ? null : tutPick('well')), enter: () => { tutBase443('well'); tut.noWood443 = false; },
    tiles: () => tutHold432('well', [T443.wells[2]].filter(([x, y]) => !board[y][x])), cam: () => [T443.wells[2]],
    done: () => tut.noWood443 || tutAdded443('well') >= 1,
    text: () => `ลองสร้าง ${thumbHtml('well', 24)} <b>บ่อน้ำบ่อที่ 3</b><br>${tutDo434('well')}` },
  build443('lumberjack', T443.lumber, 1, 'ไม้ไม่พอ! 🪵', () => `${tut.noWood443 ? '❗ <b>ไม้หมดแล้ว</b> สร้างบ่อที่ 3 ไม่ได้<br>' : ''}ไม้ได้มาจาก ${thumbHtml('lumberjack', 24)} <b>บ้านคนตัดไม้</b> (${cost443('lumberjack')}) คนตัดไม้จะไปตัด${thumbHtml('tree', 22)}<b>ต้นไม้ริมแม่น้ำ</b> มาเก็บในคลังไม้ · ต้อง<b>ติดถนน</b>`,
    { enter: () => { tutBase443('lumberjack'); try { buildType = null; refreshToolbar(); } catch (e) { /* ไม่เป็นไร */ } } }),
  { title: 'รอคนตัดไม้', arrow443: 'lumberjack', cam: () => T443.trees.concat(T443.lumber, [T443.woodshed]),
    enter: () => { tut.wood443 = kindStock('wood'); },
    done: () => kindStock('wood') > (tut.wood443 || 0),
    progress: () => `🪵 ไม้ในคลัง ${kindStock('wood')}`,
    text: () => `ลูกศรแดงชี้<b>คนตัดไม้</b> ดูเขาเดินไปตัดต้นไม้ริมแม่น้ำ แล้วขนกลับมาเก็บใน ${thumbHtml('woodshed', 22)} <b>คลังไม้</b>` },
  build443('well', [T443.wells[2]], 1, 'สร้างบ่อที่ 3 ได้แล้ว', () => `มีไม้แล้ว สร้าง ${thumbHtml('well', 24)} <b>บ่อน้ำบ่อที่ 3</b> ได้เลย`,
    { done: () => countType('well') >= 3 }),
  build443('pond', T443.pond, 1, 'สร้างสระน้ำ', () => `${thumbHtml('pond', 24)} <b>สระน้ำ</b> ${$443(COST.pond)} ให้น้ำกับข้าวรอบๆ <b>ฟรี</b> โดยไม่ต้องตัก<br>แต่ตอนสร้าง เกษตรกรต้องขน<b>น้ำ ${BUILDINGS.pond.waterCost} หน่วย</b>จากบ่อมาเติมก่อน`),
  { title: 'รอเติมน้ำสระ', arrow443: 'farmhouse', el: () => (gameSpeed > 1 ? null : hudSpeedPill), cam: () => T443.pond.concat(T443.wells),
    done: () => { const p = tutFind('pond'); return !!(p && !board[p[1]][p[0]].building); },
    progress: () => { const p = tutFind('pond'), c = p && board[p[1]][p[0]]; return c && c.building ? `💧 น้ำในสระ ${c.waterIn || 0}/${BUILDINGS.pond.waterCost}` : '✅ สระพร้อมใช้'; },
    text: () => `เกษตรกรกำลังขนน้ำจากบ่อมาเติมสระ<br>${gameSpeed > 1 ? '⏩ เร่งเวลาอยู่' : '💡 รอนานไหม? กดปุ่ม <b>x1</b> (ที่กะพริบ) เพื่อเร่งเวลา'}` },
  build443('field', T443.pfields, 3, 'ปลูกข้าวรอบสระ', () => `ปลูก ${thumbHtml('field', 24)} <b>ข้าวสาลี 3 แปลง</b> ในช่องเหลือง แล้วเทียบกัน<br>• <b>ติดสระ</b> ได้น้ำฟรี 💧<b>2</b> หน่วย<br>• <b>ห่างสระ 1 ช่อง</b> ได้ 💧<b>1</b> หน่วย<br>• <b>ไกลสระ</b> ไม่ได้น้ำฟรี ต้องรอตักจากบ่อ`,
    { progress: () => `ปลูกแล้ว ${Math.max(0, tutAdded443('field'))}/3 แปลง` }),
  { title: 'แม่น้ำให้น้ำฟรี', el: () => tutUtil443(rangeBtn), cam: () => [[4, 0], [12, 5]],
    done: () => !!showRange,
    text: () => `<b>แม่น้ำ</b>ด้านบนให้น้ำฟรีกับช่องใกล้ๆ ติดแม่น้ำ 💧<b>5</b> แล้วลดลง <b>5-4-3-2-1</b> ตามระยะ<br>${tutUtilDo443('ระยะน้ำ')}` },
  { title: 'ดูระยะน้ำ', next: true, cam: () => [[4, 0], [12, 5]], enter: () => closeUtil443(),
    text: 'สีฟ้าบนแผนที่คือช่องที่ได้น้ำฟรี ยิ่งเข้มยิ่งได้มาก<br>ปลูกพืชในช่องสีฟ้า ไม่ต้องสร้างบ่อเยอะ<br>💡 เปิด/ปิดได้เองที่แท็บ <b>เครื่องมือ</b>' },
  road443(T443.road2, 'ต่อถนนไปสร้างโรงโม่', `ต่อไปจะทำ<b>แป้ง</b> ด้วย ${thumbHtml('windmill', 24)} <b>โรงโม่แป้ง</b> ซึ่งต้อง<b>ติดถนน</b><br>ต่อ ${thumbHtml('road', 24)} <b>ถนน</b>ไปทางขวา บริเวณนี้<b>ไม่มีเงา</b>`, () => { closeUtil443(); offRange443(); }),
  build443('windmill', T443.mill1, 1, 'สร้างโรงโม่แป้ง', () => `${thumbHtml('windmill', 24)} <b>โรงโม่แป้ง</b> ${cost443('windmill')}<br>ทำแป้ง 1 ถุง ใช้<b>ข้าวสาลี 2 + ไม้ 1</b>`,
    { progress: () => tutWood443(WOOD_COST.windmill) }),
  { title: 'เงาทำให้ช้า', el: () => tutUtil443(shadeRangeBtn324), cam: () => [[0, 6], [5, 11]],
    done: () => !!showShade324,
    text: () => `<b>ภูเขา</b>ด้านซ้ายทำให้เกิด<b>เงา</b> ติดภูเขาเงาแรงสุด แล้วลดลง <b>5-4-3-2-1</b> ตามระยะ (อาคารสูงบางชนิดก็มีเงา)<br>${tutUtilDo443('ระยะเงา')}` },
  road443(T443.road3, 'ต่อถนนเข้าไปในเงา', `ลองดูว่าเงาทำอะไรได้ ต่อ ${thumbHtml('road', 24)} <b>ถนน</b>ไปทางซ้ายจนถึงเงาภูเขา (สีเข้มบนแผนที่)`, () => closeUtil443()),
  build443('windmill', T443.mill2, 1, 'สร้างโรงโม่ในเงา', () => `สร้าง ${thumbHtml('windmill', 24)} <b>โรงโม่แป้ง</b>อีกหลัง <b>ในเงา</b> (${cost443('windmill')})`,
    { progress: () => tutWood443(WOOD_COST.windmill) }),
  { title: 'โรงโม่ในเงาผลิตช้า', next: true, cam: () => T443.mill2.concat(T443.mill1),
    text: () => { let lv = 0; eachCell((c, x, y) => { if (c && c.type === 'windmill') lv = Math.max(lv, -shadeLevelAt(x, y)); }); return `โรงโม่ในเงา${lv ? ` (เงา <b>${lv}</b> ระดับ)` : ''} ใช้<b>เวลาผลิตนานขึ้น</b> ตามระดับเงาที่โดน<br>เงา 1 ระดับ ช้าลง x2 · 2 ระดับ x4 · 3 ระดับ x8<br>💡 แตะโรงโม่เพื่อดูว่าช้าลงเท่าไหร่ · สร้างอาคารผลิตให้<b>พ้นเงา</b>จะดีที่สุด`; } },
  build443('storehouse', T443.store, 1, 'สร้างคลังสินค้า', () => `แป้งที่ผลิตได้ต้องมีที่เก็บ สร้าง ${thumbHtml('storehouse', 24)} <b>คลังสินค้า</b> ${cost443('storehouse')} · ต้อง<b>ติดถนน</b>`,
    { progress: () => tutWood443(WOOD_COST.storehouse), enter: () => { tutBase443('storehouse'); closeUtil443(); offRange443(); } }),
  { title: 'เร่งเวลา', el: () => hudSpeedPill, cam432: 'free', minMs: 2500,
    done: () => gameSpeed > 1,
    text: 'ผลิตแป้งต้องใช้เวลา ปุ่ม <b>x1</b> ที่แถบบนใช้<b>เร่งเวลา</b> (กดซ้ำ x2 → x4 → x8 → x16)<br>ปุ่ม <b>พัก</b> ข้างกันใช้หยุดเกม' },
  { title: 'รอแป้งครบ 10 ถุง', cam: () => T443.mill1.concat(T443.store, T443.mill2),
    done: () => kindStock('flour') >= SHIPMENT || soldFlour443(), minMs: 1500,
    progress: () => (kindStock('flour') >= SHIPMENT ? `✅ ครบ ${SHIPMENT} ถุงแล้ว!` : `แป้งในคลังสินค้า ${kindStock('flour')}/${SHIPMENT}`),
    text: () => `โรงโม่ใช้ข้าวสาลีจากไซโล + ไม้จากคลังไม้ ทำเป็นแป้ง แล้วขนไปเก็บในคลังสินค้า<br>รถส่งของทีละ <b>${SHIPMENT} ถุง</b>` },
  build443('tradedepot', T443.depot, 1, 'สร้างสถานีขนส่งสินค้า', () => `${thumbHtml('tradedepot', 24)} <b>สถานีขนส่งสินค้า</b> ${cost443('tradedepot')} ใช้ส่งของไปขาย ต้องวาง<b>ที่ขอบแผนที่</b>`,
    { progress: () => tutWood443(WOOD_COST.tradedepot) }),
  { title: 'ส่งแป้งไปขาย', enter: () => { try { closeSellPopup(); } catch (e) { /* ไม่เป็นไร */ } },
    el: () => (depotPopup && depotPopup.rows.flour ? depotPopup.rows.flour.btn : null),
    tiles: () => (depotPopup ? [] : tutDepot432()), cam: () => tutDepot432(),
    done: () => tutTrip() || soldFlour443(),
    text: () => (depotPopup ? `กดปุ่ม <b>ส่ง ${SHIPMENT} ชิ้น</b> ที่แถว<b>แป้ง</b>` : `แตะ ${thumbHtml('tradedepot', 24)} <b>สถานีขนส่งสินค้า</b> (ช่องที่กะพริบ)`) },
  { title: 'รถกำลังไปขาย 🚚', enter: () => { try { closeDepotPopup(); } catch (e) { /* ไม่เป็นไร */ } }, cam: () => tutDepot432(),
    done: () => soldFlour443(),
    text: 'ได้ 💰 เงินและ ⭐ ดาว ตอนรถกลับถึง<br>💡 ติ๊ก <b>auto</b> ในหน้าสถานี รถจะส่งเองทุกครั้งที่ของครบ' },
  { title: '🎉 ขายแป้งได้แล้ว!', end: true,
    text: 'คุณรู้ครบแล้ว: <b>น้ำ → ข้าว → ไซโล → โรงโม่ → คลัง → ขาย</b><br>💡 ลากนิ้ว/เมาส์เพื่อเลื่อนแผนที่ · ถ่างนิ้ว/ลูกกลิ้งเพื่อซูม' },
];
if (TUT443) TUT_STEPS_ALL.splice(0, TUT_STEPS_ALL.length, ...TUT_STEPS_443);
// ลูกศรแดงชี้คนงาน (ขั้นที่มี arrow443)
function tutArrow443(now) {
  const st = TUT_STEPS[tut.i];
  if (!st || !st.arrow443) return;
  const c = tutWorker443(st.arrow443), w = c && (c.farmer || c.rancher);
  if (!w) return;
  if (w.state === 'idle') { const [cx, cy] = tileCenterScreen(w.hx, w.hy); drawSelectArrow(cx, cy - 34 * viewZoom, now); }
  else { const [cx, cy] = microCenterScreen(...walkPos(w, now)); drawSelectArrow(cx, cy - 22 * viewZoom, now); }
}
"""
rep("const TUT_STEPS = TUT_STEPS_ALL.filter(", NEW + "const TUT_STEPS = TUT_STEPS_ALL.filter(")

# 4) วาดลูกศรชี้คนงานพร้อมช่องกะพริบ
rep("""function drawTutorialTiles() {
  if (!tut) return;
  const st = TUT_STEPS[tut.i];""", """function drawTutorialTiles() {
  if (!tut) return;
  try { tutArrow443(performance.now()); } catch (e) { /* ไม่เป็นไร */ }
  const st = TUT_STEPS[tut.i];""")

# 5) จับเหตุการณ์ "ไม้ไม่พอ" ตอนวางในบทเรียน
rep("  const _pb313 = placeBuilding;\n  placeBuilding = function (x, y, type) {",
    "  const _pb313 = placeBuilding;\n  placeBuilding = function (x, y, type) {\n    if (tutorialMode && tut && WOOD_COST[type] && woodStock() < WOOD_COST[type]) tut.noWood443 = true; // v443")

open(path, 'w', encoding='utf8').write(h)
print('ok')
