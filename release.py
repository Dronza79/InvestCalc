import subprocess
import re
import os


def release():
    version_file = "__version__.py"

    # 1. Считываем текущую версию
    if not os.path.exists(version_file):
        with open(version_file, "w") as f:
            f.write('VERSION = "1.0.0"')

    with open(version_file, "r") as f:
        content = f.read()
        print(f'{content=}')
        current_version = re.search(r'VERSION = "(.*?)"', content).group(1)

    print(f"Текущая версия: {current_version}")

    # 2. Выбор части версии для увеличения
    print("Выберите тип обновления:\n1. Major (1.0.0 -> 2.0.0)\n2. Minor (1.0.0 -> 1.1.0)\n3. Patch (1.0.0 -> 1.0.1)")
    choice = input("Ваш выбор (1/2/3): ")

    parts = list(map(int, current_version.split('.')))

    if choice == '1':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif choice == '2':
        parts[1] += 1
        parts[2] = 0
    else:
        parts[2] += 1

    new_version = ".".join(map(str, parts))

    # 3. Ввод расширенного сообщения
    print("Введите описание изменений (нажмите Enter дважды или Ctrl+Z для завершения):")
    lines = []
    while True:
        try:
            line = input()
            if not line and (not lines or not lines[-1]):  # Выход при двойном Enter
                break
            lines.append(line)
        except EOFError:  # Выход при Ctrl+Z (Windows)
            break

    description = "\n".join(lines)

    # Формируем полное сообщение: Заголовок + Пустая строка + Тело
    full_commit_msg = f"v{new_version}\n\n{description}"
    print(f'{full_commit_msg=}')
    # 4. Сохранение и Git
    with open(version_file, "w") as f:
        f.write(f'VERSION = "{new_version}"\n')
    try:
        # Добавляем все изменения
        subprocess.run(["git", "add", "."], check=True)
        # Делаем коммит
        subprocess.run(["git", "commit", "-m", full_commit_msg], check=True)
        # Создаем тег версии
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        # ЗАЛИВКА НА GITHUB
        print(f"\nОтправка данных на GitHub (https://github.com/Dronza79/InvestCalc)...")
        # Отправляем текущую ветку (обычно main или master)
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)
        # Отправляем созданный тег, чтобы версия появилась в разделе Releases
        subprocess.run(["git", "push", "origin", f"v{new_version}"], check=True)
        print(f"\nУспешно! Версия {new_version} опубликована на GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка Git: {e}")


if __name__ == "__main__":
    release()
