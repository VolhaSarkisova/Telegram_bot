Телеграм-бот для резервирования столиков в ресторане.

Пользователь имеет возможность выбора:
    даты (сегодня, завтра, послезавтра), 
    продолжительности (1 час, 2 часа, 3 часа), 
    времени бронирования (зависит от продолжительности, т.е. если пользователь указал продолжительность 3 часа, то максимальное время, на которое сможет забронировать 
                                                                                              ВРЕМЯ_ДО_КОТОРОГО_РАБОТАЕТ_РЕСТОРАН-ПРОДОЛЖИТЕЛЬНОСТЬ-1ЧАС(про запас)).
После указания данных параметров программа отображает доступные к бронированию столики (перечень всевозможных комбинаций стол-время формируется автоматически при его отсутствии).
Пользователь отправляет контактные данные (для возмождности обратной связи) и бронирует стол (флаг 1).
Администратор подтверждает/отменяет бронирование (флаг 2/0).
Результат решения администратора отображается пользователю в чате.
