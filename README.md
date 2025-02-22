# Альфа-тз

## Описание


- **task1**: В рамках первой задачи была проведена предобработка данных. Обновленная таблица с подготовленными данными сохранена в файле `data/data_prep_transforme.csv`. 

- **task2**: Во второй задаче было разработано API для инференса, что позволяет пользователям отправлять запросы и получать прогнозы на основе входящих данных. Это API было упаковано в Docker-контейнер, что упрощает развертывание и использование в различных средах.

- **task3**: В третьей задаче я экспериментировал с различными методами, включая ансамблирование и подбор параметров. Однако, несмотря на все усилия, мне не удалось достичь желаемого результата, так как это был мой первый опыт работы с временными рядами.

- **task4**: Последняя задача была выполнена с использованием алгоритмической библиотеки для оптимизации распределения конфет. В результате были получены значимые выводы и результаты, которые демонстрируют общую прибыль, объемы транспортировки и прибыльность открытых магазинов. 

### Вывод 4 задачи
```
==================================================
Candy Distribution Optimization Results
==================================================
Total Profit: 415544.57 currency units

Transport Volume:
 - F_01 -> S_11: 340.0 candies
 - F_02 -> S_12: 360.0 candies
 - F_03 -> S_06: 120.0 candies
 - F_03 -> S_10: 4.0 candies
 - F_04 -> S_03: 70.0 candies
 - F_05 -> S_07: 290.0 candies
 - F_05 -> S_10: 96.0 candies
 - F_06 -> S_07: 70.0 candies
 - F_06 -> S_13: 60.0 candies
 - F_08 -> S_08: 60.0 candies

Closed Shops:
 - S_01, S_02, S_04, S_05, S_09

Unallocated Candies by Factory:
 - Factory F_01: 49.0 candies
 - Factory F_02: 49.0 candies
 - Factory F_03: 0.0 candies
 - Factory F_04: 0.0 candies
 - Factory F_05: 0.0 candies
 - Factory F_06: 66.0 candies
 - Factory F_07: 394.0 candies
 - Factory F_08: 305.0 candies

Unmet Demand by Shop:
 - Shop S_01: 200.0 candies
 - Shop S_02: 20.0 candies
 - Shop S_03: 250.0 candies
 - Shop S_04: 360.0 candies
 - Shop S_05: 360.0 candies
 - Shop S_06: 0.0 candies
 - Shop S_07: 0.0 candies
 - Shop S_08: 0.0 candies
 - Shop S_09: 80.0 candies
 - Shop S_10: 0.0 candies
 - Shop S_11: 0.0 candies
 - Shop S_12: 0.0 candies
 - Shop S_13: 0.0 candies

Profitability of Open Shops:
 - S_03: 17725.64 currency units
 - S_06: 59998.71 currency units
 - S_07: 46305.07 currency units
 - S_08: 11822.78 currency units
 - S_10: 14507.83 currency units
 - S_11: 112687.72 currency units
 - S_12: 147312.81 currency units
 - S_13: 5184.00 currency units
==================================================
```

## Установка
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/XlordPlay/alfa_test
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Для запуска Docker перейдите в папку `task2/`, соберите и поднимите контейнер:
   ```bash
   cd task2/
   sudo docker-compose up --build
   ```

## Использование
Для проверки API в `task2/` выполните следующую команду в терминале:

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "features": {
    "equity_amt": 0.4,
    "cc_trn_cnt_1": 0,
    "rel_age": 99,
    "cc_trn_cnt": 0,
    "cc_avg_bal": 0.4,
    "dep_max_amt": 235.8,
    "cc_appr_amt": 2000,
    "customerID": 3764517,
    "tr_min_bal": 6067.53,
    "npv_trans": 498.65,
    "reject": -1,
    "cc_min_bal": 0.4,
    "cc_avg_bal_1": 0,
    "tr_la_open_mth": 87,
    "acc_funds": 6574.2,
    "npv_total": 468.37,
    "acc_credit": 500,
    "prod_count": 2,
    "cc_ea_open_mth": 22,
    "recency": 22
  }
}'
```

## Дополнительные мысли
Если бы было больше времени, я бы провел более детальный EDA (анализ данных) для лучшего понимания структуры и особенностей данных. Также я бы уделил больше внимания оптимизации моделей, добавил бы пайплайн для упрощения процесса разработки и развертывания, а также собрал бы онлайн метрики для мониторинга производительности модели в реальном времени. 