# Схемы модулей дивана — вид сверху (стиль TOM / KF.8333)

Этот файл — полное описание того, как на штендере рисуются модули и комбинации
модульного дивана в виде сверху. Его можно отдать в другой чат, чтобы тот нарисовал
так же схемы для дивана **Thor** (или любого другого модульного дивана с такой же
конструкцией: стёганое сиденье-платформа, отдельные подушки спинки, валики-подлокотники).

В конце файла — **готовый рабочий HTML** (откройте в браузере — увидите схемы).
Чтобы сделать Thor, достаточно заменить в нём массивы `mods` и `cmbs` своими размерами
и, если нужно, подстроить константы в разделе «Что менять под другой диван».

---

## 1. Общие правила

- Вид **строго сверху**. Спинка — всегда сверху схемы, перед дивана (где сидят) — снизу.
- 1 единица SVG = **1 см** реального дивана. Все размеры в коде — в сантиметрах.
  Масштаб на странице задаётся одним числом `scale` (px на см).
- Над схемой — **ширина**: линия с числом посередине. Справа — **глубина**: вертикальная
  линия с числом посередине. Цифры серые `#77706a`, 11px, Montserrat 600. Линии `#b8afa5`, 1px.
- Комбинация = несколько модулей, поставленных рядом. Каждый модуль рисуется своим
  контуром — между модулями видна граница.
- Подписи модулей — по-русски, без слова «модуль» там, где можно:
  «Диван 3,5-местный с подлокотником», «Диван 1,5-местный без подлокотников»,
  «Угловой модуль», «Шезлонг (CL)». Комбинации подписываются только кодом **C1, C2…**
  (крупно, 22px, 800, терракотовый `#c4553a`), без перечисления состава.

## 2. Из чего состоит модуль (слои снизу вверх)

### 2.1 Платформа сиденья
- Прямоугольник на весь модуль `w × d`, скругление **rx 9**.
- Заливка белая, обводка тёмная `#2a2724`, толщина 1.4px (не масштабируется).

### 2.2 Стёжка — КЛЕТКИ (не кружочки!)
Сиденье поделено швами на квадраты, как на фабричном чертеже. Шов = впадина:
- под ним светлая широкая полоса `#e6dfd6` толщиной 4 (в см);
- поверх — тонкая линия `#9d948a` 0.9px;
- на **каждом пересечении** швов — точка-углубление: круг r = 2.6 см, `#8c837a`.

**Где идут вертикальные швы** (через всю глубину сиденья):
- если есть подлокотник — первый шов в **30 см** от края (узкая колонка под валиком);
- остальное пространство делится на колонки ≈ **43 см** (у модулей со спинкой) или
  ≈ **54 см** (у модулей без спинки: шезлонг, угловой);
- можно задать число колонок вручную параметром `cols` (у 2,5-местного `cols:4` —
  швы как у 3,5-местного, только клетки уже).

**Где идут горизонтальные швы**:
- модуль со спинкой: 3 ряда по глубине — **27% / 36% / 37%** (задний узкий ряд почти
  целиком закрыт подушками спинки);
- шезлонг (глубина > 130): ряды примерно по **40 см** (у 161 см — 4 ряда);
- остальные без спинки: 2 ряда пополам.

### 2.3 Подушки спинки — отдельные, свободные
- Цвет `#ece5dc`, обводка `#6f675f` 1.1px.
- Форма: скруглённый прямоугольник (r 11), передний край чуть вогнут (на 4 см).
- **Толщина 27 см.** Ширина обычной подушки — **84 см** (замер в салоне ≈ 84).
- Стоят у заднего края с промежутками 5 см, центрируются между подлокотниками.
  Количество: `round((w − 20) / 95)`, минимум 1 → у 204–236 см две подушки,
  у 88 см одна.
- **Угловой модуль**: две подушки по **74 см** (замер ≈ 74), стоят **угол об угол**:
  задняя подушка прижата вправо и заканчивается там, где начинается боковая;
  боковая подушка стоит вдоль правого края и начинается от переднего-нижнего угла
  задней. В углу остаётся маленький кусок открытого сиденья.

### 2.4 Подлокотники — валики
- Цвет и обводка как у подушек, скругление r 11.
- Ширина **24 см**, длина = глубина − 9 (почти до переднего края).
- Лежат **на** платформе: отступ 3 см от бокового края, 4 см от заднего.

### 2.5 Шезлонг (CL)
- Без спинки и без подлокотника.
- Одна подушка 84 × 27:
  - шезлонг стоит **вперёд** (108 × 161): подушка вертикально вдоль правого края (`pillow:1`);
  - шезлонг лежит **вдоль** дивана (161 × 108, как в C5): подушка горизонтально у
    задней стенки, со стороны дивана, дальний конец открыт (`pillowH:1`).

## 3. Данные TOM (пример заполнения)

| Модуль | Ш × Г, см | Параметры |
|---|---|---|
| Диван 2,5-местный с двумя подлокотниками | 207 × 108 | `arms:"LR", cols:4` |
| Диван 3,5-местный с двумя подлокотниками | 236 × 108 | `arms:"LR"` |
| Диван 3,5-местный с подлокотником | 204 × 108 | `arms:"L"` (зеркально — `"R"`) |
| Диван 1,5-местный без подлокотников | 88 × 108 | — |
| Угловой модуль | 108 × 108 | `back:"TR"` |
| Шезлонг (CL) | 108 × 161 | `back:"", pillow:1` |

| Комбинация | Состав | Размер |
|---|---|---|
| C1 | 3,5 + угловой + шезлонг вперёд | 312 × 269 |
| C2 | 3,5 + 1,5 + угловой + шезлонг | 400 × 269 |
| C3 | 3,5 + угловой + 3,5 (повёрнут, `rot:1`) | 312 × 312 |
| C4 | 3,5 + 1,5 + угловой + 3,5 | 400 × 312 |
| C5 | 3,5 + шезлонг вдоль (`pillowH`) | 365 × 108 |
| C6 | 3,5 + 3,5 (подлокотники по краям) | 408 × 108 |

## 4. Как описывать модуль в коде

```js
{ x, y,        // где стоит в комбинации (см от левого верхнего угла)
  w, d,        // ширина и глубина, см
  arms: "L" | "R" | "LR" | "",   // подлокотники-валики
  back: "T" (по умолч.) | "TR" (угловой) | "R" | "",  // где подушки спинки
  cols: 4,     // (необяз.) число колонок стёжки
  pillow: 1,   // подушка вертикально у правого края (шезлонг вперёд)
  pillowH: 1,  // подушка горизонтально у спинки слева (шезлонг вдоль)
  rot: 1 }     // повернуть модуль на 90° (для второй стороны угла);
               // w/d задаются уже в повёрнутом виде, спинка уходит вправо
```

Комбинация: `{t:"C3", W:312, D:312, parts:[ …модули… ]}`, где W×D — общий габарит.
Вторая сторона угла: `{x:204, y:108, w:108, d:204, rot:1, arms:"R"}` — 3,5-местный,
повёрнутый спинкой вправо, валик внизу.

## 5. Что менять под другой диван (Thor)

1. Размеры модулей и комбинаций — массивы `mods` и `cmbs`.
2. В функции `piece()` константы:
   - `CB=84` — ширина подушки спинки, `CC=74` — подушки углового, `CT=27` — толщина подушек;
   - `BW=24` — ширина валика-подлокотника, `AL=d-9` — его длина;
   - `AWc=30` — ширина узкой колонки стёжки под валиком;
   - 43 / 54 — ширина клетки стёжки; `[0.27,0.36,0.37]` — ряды по глубине.
3. Если у Thor нет стёжки клетками — убрать блок «стёжка», если подлокотники не валики,
   а высокие — заменить `rect` подлокотника.
4. Сверьте с фото сверху и фабричным чертежом: где реально проходят швы, сколько
   подушек спинки и как сходятся спинки у углового.

## 6. Готовый HTML (скопировать в файл `.html` и открыть)

```html
<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>Схемы модулей</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#2a2724;--mute:#77706a;--acc:#c4553a;--line:#e3dcd3}
body{margin:0;padding:30px;font-family:Montserrat,sans-serif;color:var(--ink);background:#fff}
h2{font-size:24px;font-weight:800;margin:24px 0 10px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-left:1px solid var(--line)}
.card{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 8px;min-height:220px;display:flex;flex-direction:column;align-items:center;text-align:center}
.draw{flex:1;display:flex;align-items:center;justify-content:center}
.dim{display:inline-grid;grid-template-columns:auto auto;align-items:center}
.dim .w{grid-column:1;font-size:11px;font-weight:600;display:flex;align-items:center;gap:5px;color:var(--mute);margin-bottom:3px}
.dim .w:before,.dim .w:after{content:"";flex:1;height:1px;background:#b8afa5}
.dim .d{grid-column:2;grid-row:2;align-self:stretch;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:600;color:var(--mute);margin-left:6px}
.dim .d:before,.dim .d:after{content:"";flex:1;width:1px;background:#b8afa5}
.dim svg{grid-column:1;grid-row:2;display:block;overflow:visible}
.card h5{font-size:12px;font-weight:600;line-height:1.25;margin:8px 0 0}
#cmbs .card h5{font-size:22px;font-weight:800;color:var(--acc)}
</style></head><body>
<h2>Популярные комбинации</h2><div class="grid" id="cmbs"></div>
<h2>Модули</h2><div class="grid" id="mods"></div>
<script>
function cush(x,y,w,h,vert){ // свободная подушка спинки, вогнутый передний край
  if(vert){ // лежит вдоль правого/левого края: x,y — левый верх, w — толщина, h — длина
    const r=11; return `<path d="M${x+r} ${y} L${x+w-r} ${y} Q${x+w} ${y} ${x+w} ${y+r} L${x+w} ${y+h-r} Q${x+w} ${y+h} ${x+w-r} ${y+h} L${x+r} ${y+h} Q${x} ${y+h} ${x} ${y+h-r} Q${x+4} ${y+h/2} ${x} ${y+r} Q${x} ${y} ${x+r} ${y}Z" class="b"/>`;}
  const r=11; return `<path d="M${x+r} ${y} L${x+w-r} ${y} Q${x+w} ${y} ${x+w} ${y+r} L${x+w} ${y+h-r} Q${x+w} ${y+h} ${x+w-r} ${y+h} Q${x+w/2} ${y+h-4} ${x+r} ${y+h} Q${x} ${y+h} ${x} ${y+h-r} L${x} ${y+r} Q${x} ${y} ${x+r} ${y}Z" class="b"/>`;
}
function piece(p){
  if(p.rot){const q=Object.assign({},p,{rot:0,x:0,y:0,w:p.d,d:p.w}); return `<g transform="translate(${p.x+p.w},${p.y}) rotate(90)">${piece(q)}</g>`;}
  const {x,y,w,d}=p, back=p.back??"T", arms=p.arms||"";
  const CB=84, CC=74, CT=27, BW=24, g=2.5;
  let s=`<g transform="translate(${x},${y})"><rect x="0" y="0" width="${w}" height="${d}" rx="9" class="o"/>`;
  // стёжка по фабричному чертежу: у подлокотника — узкая колонка ~30 см под валиком,
  // дальше колонки ~43 см; швы идут через всю глубину; ряды: узкий задний (под подушками) + 2 передних
  const AWc=30, xs=[];
  let x0=arms.includes("L")?AWc:0, x1=w-(arms.includes("R")?AWc:0);
  if(arms.includes("L")) xs.push(AWc);
  const nc=p.cols||Math.max(1,Math.round((x1-x0)/(back==="T"?43:54)));
  for(let i=1;i<nc;i++) xs.push(x0+i*(x1-x0)/nc);
  if(arms.includes("R")) xs.push(w-AWc);
  const rowsH = back.includes("T") ? [d*0.27, d*0.36, d*0.37] : (d>130 ? Array(Math.round(d/40)).fill(d/Math.round(d/40)) : [d/2,d/2]);
  let yy=0; const ys=[];
  for(const rh of rowsH){ yy+=rh; ys.push(yy); } ys.pop();
  for(const xx of xs) s+=`<line x1="${xx}" y1="3" x2="${xx}" y2="${d-3}" class="sm"/><line x1="${xx}" y1="3" x2="${xx}" y2="${d-3}" class="sl"/>`;
  for(const y2 of ys) s+=`<line x1="3" y1="${y2}" x2="${w-3}" y2="${y2}" class="sm"/><line x1="3" y1="${y2}" x2="${w-3}" y2="${y2}" class="sl"/>`;
  for(const xx of xs) for(const y2 of ys) s+=`<circle cx="${xx}" cy="${y2}" r="2.6" class="dp"/>`;
  // подушки спинки
  const L=arms.includes("L")?BW+4:0, R=arms.includes("R")?BW+4:0;
  if(back==="TR"){ /* спинки угол об угол: правый-нижний угол верхней касается левого-верхнего угла боковой */ const hx=w-CT-3-CC; s+=cush(hx,3,CC,CT)+cush(w-CT-3,3+CT,CT,CC,1); }
  else {
    if(back.includes("T")){ const avail=w-L-R-6, n=Math.max(1,Math.round((w-20)/95)), cw2=Math.min(CB,(avail-(n-1)*5)/n), tot=n*cw2+(n-1)*5, x0=L+3+(avail-tot)/2;
      for(let i=0;i<n;i++) s+=cush(x0+i*(cw2+5),3,cw2,CT); }
    if(back.includes("R")) s+=cush(w-CT-3,4,CT,Math.min(CB,d-8),1);
  }
  if(p.pillow) s+=cush(w-CT-4,6,CT,Math.min(CB,d-12),1);
  if(p.pillowH) s+=cush(4,3,CB,CT);
  // подлокотники-валики лежат на платформе
  const AL=d-9;
  if(arms.includes("L")) s+=`<rect x="3" y="4" width="${BW}" height="${AL}" rx="11" class="a"/>`;
  if(arms.includes("R")) s+=`<rect x="${w-BW-3}" y="4" width="${BW}" height="${AL}" rx="11" class="a"/>`;
  return s+`</g>`;
}
function drawing(W,D,parts,scale){
  const svg=`<svg width="${W*scale}" height="${D*scale}" viewBox="0 0 ${W} ${D}">
  <style>.o{fill:#fff;stroke:#2a2724;stroke-width:1.4;vector-effect:non-scaling-stroke}
  .b,.a{fill:#ece5dc;stroke:#6f675f;stroke-width:1.1;vector-effect:non-scaling-stroke}
  .s{fill:#fff;stroke:#bdb4aa;stroke-width:.9;vector-effect:non-scaling-stroke}
  .sm{stroke:#e6dfd6;stroke-width:4}
  .sl{stroke:#9d948a;stroke-width:.9;vector-effect:non-scaling-stroke}
  .dp{fill:#8c837a}
  .t{stroke:#a59c93;stroke-width:.8;vector-effect:non-scaling-stroke}
  .wd{fill:#d6b38a;stroke:#8a6440;stroke-width:1.2;vector-effect:non-scaling-stroke}
  .wdl{fill:none;stroke:#8a6440;stroke-width:1;vector-effect:non-scaling-stroke}</style>
  ${parts.map(piece).join("")}</svg>`;
  return `<div class="dim"><div class="w">${W}</div>${svg}<div class="d">${D}</div></div>`;
}
const card=(c,s)=>`<div class="card"><div class="draw">${drawing(c.W,c.D,c.parts,s)}</div><h5>${c.t}</h5></div>`;
const mods=[
 {t:"Диван 2,5-местный<br>с двумя подл.",W:207,D:108,parts:[{x:0,y:0,w:207,d:108,arms:"LR",cols:4}]},
 {t:"Диван 3,5-местный<br>с двумя подл.",W:236,D:108,parts:[{x:0,y:0,w:236,d:108,arms:"LR"}]},
 {t:"Диван 3,5-местный<br>с подлокотником",W:204,D:108,parts:[{x:0,y:0,w:204,d:108,arms:"L"}]},
 {t:"Диван 1,5-местный<br>без подлокотников",W:88,D:108,parts:[{x:0,y:0,w:88,d:108}]},
 {t:"Угловой<br>модуль",W:108,D:108,parts:[{x:0,y:0,w:108,d:108,back:"TR"}]},
 {t:"Шезлонг (CL)",W:108,D:161,parts:[{x:0,y:0,w:108,d:161,back:"",pillow:1}]},
];
const cmbs=[
 {t:"C1",W:312,D:269,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:108,d:108,back:"TR"},{x:204,y:108,w:108,d:161,back:"",pillow:1}]},
 {t:"C2",W:400,D:269,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:88,d:108},{x:292,y:0,w:108,d:108,back:"TR"},{x:292,y:108,w:108,d:161,back:"",pillow:1}]},
 {t:"C3",W:312,D:312,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:108,d:108,back:"TR"},{x:204,y:108,w:108,d:204,rot:1,arms:"R"}]},
 {t:"C4",W:400,D:312,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:88,d:108},{x:292,y:0,w:108,d:108,back:"TR"},{x:292,y:108,w:108,d:204,rot:1,arms:"R"}]},
 {t:"C5",W:365,D:108,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:161,d:108,back:"",pillowH:1}]},
 {t:"C6",W:408,D:108,parts:[{x:0,y:0,w:204,d:108,arms:"L"},{x:204,y:0,w:204,d:108,arms:"R"}]},
];
document.getElementById("mods").innerHTML=mods.map(c=>card(c,.5)).join("");
document.getElementById("cmbs").innerHTML=cmbs.map(c=>card(c,.5)).join("");

</script></body></html>
```
