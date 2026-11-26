# МойСклад → Ashley заказ план

`ashley_sold.py <YYYY-MM-DD>` — товары Ashley, проданные за день по заказам покупателей:
Code, продано, доступно (остаток − резерв), в пути (qty), trip, дата прихода.

`trips.csv` — трипы Ashley, ещё не внесённые в МойСклад (`trip;article;qty;eta;note`).
Правило даты прихода Ashley: **дата инвойса + 35 дней**.
Трип, номер которого уже стоит в комментарии заказа поставщику в МоёмСкладе, из этого файла не берётся.

`parse_ashley_invoice.py OUT.csv INVOICE.pdf...` — разбирает PDF «Ashley Consolidated Invoice»
(письма от ECommServ@ashleyfurniture.com в ящике South Gate) в строки трипов с датой прихода = дата инвойса + 35 дней.
Результат передаётся в отчёт: `ashley_sold.py <дата> --trips OUT.csv`.
