"""Генератор векторных образцов дерева (квадратики-«дощечки») для штендеров.

Использование:
    python3 wood_swatch.py            # печатает SVG трёх образцов TIM
    from wood_swatch import swatch    # swatch(idx, base, light, dark, edge)

Как устроен образец (viewBox 34x34, скругление 6):
  1. Заливка базовым цветом дерева (base).
  2. Широкие тональные полосы: вертикальные кривые Безье шириной 2–6,
     случайно светлее/темнее/базовые, прозрачность 0.35–0.7 — даёт «слои» древесины.
  3. Тонкие волокна: кривые Безье толщиной 0.25–0.6 тёмным цветом,
     шаг 1.4–3.2, лёгкий изгиб ±1.8 — даёт рисунок волокна.
  4. Блик: диагональный градиент белый 28% → прозрачный → чёрный 15%
     (выглядит как лакированная дощечка).
  5. Рамка 1px цветом edge (темнее основного).
Всё обрезается clipPath со скруглением. random.Random(7+idx) — рисунок
стабильный, при повторной генерации не меняется.
"""
import random


def swatch(idx, base, light, dark, edge):
    r = random.Random(7 + idx)
    p = []
    x = -4
    while x < 40:  # широкие тональные полосы
        w = r.uniform(2, 6)
        col = r.choice([light, dark, base])
        p.append(f'<path d="M{x:.1f} -2 C{x+r.uniform(-2,2):.1f} 12 {x+r.uniform(-2,2):.1f} 24 '
                 f'{x+r.uniform(-1.5,1.5):.1f} 38" stroke="{col}" stroke-width="{w:.1f}" '
                 f'opacity="{r.uniform(.35,.7):.2f}" fill="none"/>')
        x += w * r.uniform(.8, 1.4)
    x = -2
    while x < 38:  # тонкие волокна
        p.append(f'<path d="M{x:.1f} -2 C{x+r.uniform(-1.8,1.8):.1f} 10 {x+r.uniform(-1.8,1.8):.1f} 22 '
                 f'{x+r.uniform(-1.2,1.2):.1f} 38" stroke="{dark}" stroke-width="{r.uniform(.25,.6):.2f}" '
                 f'opacity="{r.uniform(.4,.85):.2f}" fill="none"/>')
        x += r.uniform(1.4, 3.2)
    g = f"g{idx}"
    return (f'<svg class="sw" viewBox="0 0 34 34"><defs><clipPath id="c{idx}">'
            f'<rect x=".5" y=".5" width="33" height="33" rx="6"/></clipPath>'
            f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity=".28"/>'
            f'<stop offset=".5" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity=".15"/></linearGradient></defs>'
            f'<g clip-path="url(#c{idx})"><rect width="34" height="34" fill="{base}"/>{"".join(p)}'
            f'<rect width="34" height="34" fill="url(#{g})"/></g>'
            f'<rect x=".5" y=".5" width="33" height="33" rx="6" fill="none" stroke="{edge}" stroke-width="1"/></svg>')


# Цвета TIM: (base, light, dark, edge)
TIM_WOODS = {
    "натуральный": ("#dcbb92", "#ead2b0", "#b48a5e", "#9a7149"),
    "коричневый 787": ("#8a5a3b", "#a8754f", "#5e3a22", "#5a3820"),
    "тёмный L016": ("#382923", "#4f3d33", "#1c1310", "#1e1512"),
}

if __name__ == "__main__":
    for i, (name, c) in enumerate(TIM_WOODS.items(), 1):
        print(f"<!-- {name} -->")
        print(swatch(i, *c))
