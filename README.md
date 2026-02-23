# Создание архива библиотек
1. Создать файл req_*.tx
```bash
pip freeze > req_*.txt
```
2. Для скачивания всех пакетов в директорию packages: 
```bash
pip download -r req_*.txt --dest packages
```

# Установка из архива
1. Локальная установка
```bash
pip install --no-index --find-links=packages -r req_*.txt 
```
# Установка пакетов *.tar.gz
1. Извлечь файлы командой
```bash
tar -xvzf имя_архива.tar.gz
```
2. Перейти в папку с архивом
3. Запустить команду
```bash
python setup.py install 
```
# Создание самозапускаемого файла с помощью pyinstaller
1. Инсталировани
```bash
pyinstaller -F --windowed -i favicon.ico -n calc main.py
```
