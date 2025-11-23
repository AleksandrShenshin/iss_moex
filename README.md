# Библиотека для ISS MOEX
В данной библиотеке реализованы функции через API Московской Биржи. 

## Документация модуля

Для получения документации по модулю/функции можно использовать pydoc.

#### Для получения документации в командной строке:
python -m pydoc iss_moex

#### Создать html файл с описанием функций:
python -m pydoc -w iss_moex

#### Для вывода документации в интерпретаторе python

Вывод документации с помощью функции help():
  
    >>> import my_module 
    >>> help(my_module)

Также можно выводить документацию отдельного объекта:

    >>> import my_module
    >>> my_module.__doc__
    >>> my_module.my_function.__doc__
    >>> my_module.MyClass.__doc__
    >>> my_module.MyClass.my_method.__doc__
