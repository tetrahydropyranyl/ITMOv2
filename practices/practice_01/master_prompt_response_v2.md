Внесены изменения в следующие файлы по результатам анализа TRAINING_PR.diff. В каждом артефакте зафиксированы факты и риски с                                                     
     привязкой к строкам диффа.                                                                                                                                                        
                                                                                                                                                                                       
     - practices/practice_01/adr.md                                                                                                                                                    
       - Заполнены статус, дата, контекст, решение, альтернативы, последствия и риски.                                                                                                 
       - Ключевые ссылки на дифф:                                                                                                                                                      
         - API: app/api.py:35-37                                                                                                                                                       
         - ReviewService: app/review_service.py:19-22                                                                                                                                  
         - Протокол LLM: app/review_service.py:9-13                                                                                                                                    
       - Главный риск: KeyError при отсутствии payload"diff" (app/api.py:37).                                                                                                          
                                                                                                                                                                                       
     - practices/practice_01/analysis.md                                                                                                                                               
       - Заполнены разделы AS IS, TO BE, Разница, Как использовали AI.                                                                                                                 
       - AS IS: последовательность от вызова POST /api/reviews до возврата {comment: str}. Ссылки: app/api.py:35-37; app/review_service.py:                                            
         19-22.                                                                                                                                                                        
       - TO BE: ожидание валидации поля diff и возврат 4xx (как цель процесса, без изменения кода в этом PR).                                                                          
       - Разница: таблица с проверками, негативный сценарий KeyError (app/api.py:37).                                                                                                  
                                                                                                                                                                                       
     - practices/practice_01/product-management.md                                                                                                                                     
       - Создан файл. Зафиксированы проблема, ценность, критерии готовности, метрики, риски, как использовали AI.                                                                      
       - Факты и риски подтверждены строками:                                                                                                                                          
         - Риск KeyError: app/api.py:37
         - Схема ответа {comment: str}: app/review_service.py:19-22
         
         - practices/practice_01/project_management.md                                                                                                                                     
       - Заполнены инкременты и ответственность, обновлена диаграмма Ганта, раздел о применении AI.                                                                                    
       - Проверки и зависимости ссылаются на TRAINING_PR.diff (app/api.py; app/review_service.py).                                                                                     
                                                                                                                                                                                       
     - practices/practice_01/tests_e2e.md                                                                                                                                              
       - Добавлены три сценария: позитивный, негативный (отсутствует diff -> KeyError), граничный (пустой diff).                                                                       
       - Evidence:                                                                                                                                                                     
         - app/api.py:35-37; app/review_service.py:19-22                                                                                                                               
         - KeyError: app/api.py:37                                                                                                                                                     
       - Заполнен раздел «Как использовали AI» с указанием P1-03.                                                                                                                      
                                                                                                                                                                                       
     - practices/practice_01/tests_integration.md                                                                                                                                      
       - Добавлены 2 проверки связей:                                                                                                                                                  
         - FastAPI -> ReviewService: отсутствие diff даёт KeyError (app/api.py:35-37).                                                                                                 
         - ReviewService -> LLM.generate: ошибки не обрабатываются (app/review_service.py:21).                                                                                         
       - Заполнен раздел «Как использовали AI» с P1-03.                                                                                                                                
                                                                                                                                                                                       
     - practices/practice_01/tests_load.md                                                                                                                                             
       - Добавлен базовый сценарий нагрузки для POST /api/reviews с привязкой к фактам из диффа.                                                                                       
       - Обоснование минимального объёма нагрузочных: прямой вызов llm.generate без обработчиков (app/review_service.py:19-22; app/api.py:                                             
         35-37).                                                                                                                                                                       
       - Заполнен раздел «Как использовали AI» с P1-03.
       
       - practices/practice_01/tests_unit.md                                                                                                                                             
       - Добавлены 2 юнит-проверки:                                                                                                                                                    
         - Формирование промпта (app/review_service.py:19-21).                                                                                                                         
         - Схема ответа {comment: str} (app/review_service.py:21-22).                                                                                                                  
       - Заполнен раздел «Как использовали AI» с P1-03.                                                                                                                                
                                                                                                                                                                                       
     - practices/practice_01/prompts.md                                                                                                                                                
       - Заполнена строка P1-03:                                                                                                                                                       
         - Артефакт и цель: заполнение ADR/analysis/product-management/tests* по диффу.                                                                                                
         - Инструмент/модель: gpt-5, тип: master prompt.                                                                                                                               
         - Принято: риск KeyError, контракт {comment: str}, тестовые сценарии.                                                                                                         
         - Отклонено: предположения вне TRAINING_PR.diff.                                                                                                                              
         - Evidence: app/api.py:35-37; app/review_service.py:9-13; app/review_service.py:19-22.                                                                                        
                                                                                                                                                                                       
     Все выводы в документах подтверждены ссылками на строки TRAINING_PR.diff. Форматы таблиц и разделов сохранены, существующие записи не                                             
     удалялись.
