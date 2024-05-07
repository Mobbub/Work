import json, datetime

# Основной класс, который работает с бд
class WorkDB: 
    def __init__(self, file_path='main.json') -> None:
        self.file_path = file_path
        
    # Функция добавления записи в бд
    def add_note(self, new) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data=json.load(f)
        keys=list(data.keys())
        last_key=keys[-1]
        data[str(int(last_key)+1)]=new
        if new['Категория'] == 'Доход':
            data['Баланс']+=new['Сумма']
        else:
            data['Баланс']-=new['Сумма']
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return 'Новая запись успешно добавлена'

    # Функция вывода баланса
    def balance(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data=json.load(f)
        return data['Баланс']

    # Функция вывода баланса по категориям
    def bal_categ(self, type: str) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data=json.load(f)
        result=0
        keys=list(data.keys())
        second_key=keys[-1]
        for i in range(1, int(second_key)+1):
            if type == 'доход':
                if data[str(i)]['Категория'] == 'Доход':
                    result+=data[str(i)]['Сумма']
            else:
                if data[str(i)]['Категория'] == 'Расход':
                    result+=data[str(i)]['Сумма']
        return result

    # Функция для редактирования записи
    def edit_entry(self, index: int, type: str, new) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data=json.load(f)
        if type == 'Сумма':
            if data[index]['Категория'] == 'Доход':
                data['Баланс']-=data[index]['Сумма']
            elif data[index]['Категория'] == 'Расход':
                data['Баланс']+=data[index]['Сумма']
            if data[index]['Категория'] == 'Доход':
                data['Баланс']+=new
            elif data[index]['Категория'] == 'Расход':
                data['Баланс']-=new
        data[index][type]=new
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return 'Запись успешно изменена'

    # Функция для поиска записей
    def search(self, type: str, user_input) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data=json.load(f)
        result=''
        keys=list(data.keys())
        second_key=keys[-1]
        for i in range(1, int(second_key)+1):
            if type == 'доход':
                if data[str(i)]['Категория'] == 'Доход':
                    result+=f'\nНомер записи: {i}\nДата: {data[str(i)]["Дата"]}\nКатегория: {data[str(i)]["Категория"]}\nСумма: {data[str(i)]["Сумма"]}\nОписание: {data[str(i)]["Описание"]}\n'
            elif type == 'расход':
                if data[str(i)]['Категория'] == 'Расход':
                    result+=f'\nНомер записи: {i}\nДата: {data[str(i)]["Дата"]}\nКатегория: {data[str(i)]["Категория"]}\nСумма: {data[str(i)]["Сумма"]}\nОписание: {data[str(i)]["Описание"]}\n'        
            elif type == 'сумма':
                if str(data[str(i)]['Сумма']) == user_input:
                    result+=f'\nНомер записи: {i}\nДата: {data[str(i)]["Дата"]}\nКатегория: {data[str(i)]["Категория"]}\nСумма: {data[str(i)]["Сумма"]}\nОписание: {data[str(i)]["Описание"]}\n'                    
            elif type == 'дата':
                if str(data[str(i)]['Дата']) == user_input:
                    result+=f'\nНомер записи: {i}\nДата: {data[str(i)]["Дата"]}\nКатегория: {data[str(i)]["Категория"]}\nСумма: {data[str(i)]["Сумма"]}\nОписание: {data[str(i)]["Описание"]}\n'
            elif type == 'все':
                result+=f'\nНомер записи: {i}\nДата: {data[str(i)]["Дата"]}\nКатегория: {data[str(i)]["Категория"]}\nСумма: {data[str(i)]["Сумма"]}\nОписание: {data[str(i)]["Описание"]}\n'
        if result:
            return result
        return 'Ничего нет'

    # Функция для удаления записи
    def delete(self, index: int) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data=json.load(file)
        if data[index]['Категория'] == 'Доход':
                data['Баланс']-=data[index]['Сумма']
        elif data[index]['Категория'] == 'Расход':
            data['Баланс']+=data[index]['Сумма']
        if index in data:
            del data[index]
        new_data={}
        new_data["Баланс"]=data.pop("Баланс", 0)
        index=0
        for key, value in data.items():
            new_data[str(index)]=value
            index+=1
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)
        return 'Запись успешно удалена'


# Основной класс взаимодействия программы с пользователем
class Application:
    def __init__(self) -> None:
        self.actions=['1', '2', '3', '4', '1.', '2.', '3.', '4.', 'вывод баланса', 'добавление записи', 'редактирование записи', 'поиск по записям']
        self.actions_1=['1', '1.', 'вывод баланса', 'бал', 'баланс']
        self.actions_1_1=['1', '1.', 'бал', 'баланс']
        self.actions_1_2=['2', '2.', 'доход']
        self.actions_1_3=['3', '3.', 'расход']
        self.actions_2=['2', '2.', 'добавление записи']
        self.actions_2_1=['1', '1.', 'доход']
        self.actions_2_2=['2', '2.', 'расход']        
        self.actions_3=['3', '3.', 'ред', 'редактировать', 'редактировать запись', 'редактирование записи']
        self.actions_3_1=['1', '1.', 'ред', 'редактировать']
        self.actions_3_1_1=['1', '1.', 'дата']
        self.actions_3_1_2=['2', '2.', 'кат', 'категория']
        self.actions_3_1_2_1=['1', '1.', 'доход']
        self.actions_3_1_2_2=['2', '2.', 'расход']
        self.actions_3_1_3=['3', '3.', 'сумма']
        self.actions_3_1_4=['4', '4.', 'описание']
        self.actions_3_2=['2', '2.', 'удалить']
        self.actions_4=['4', '4.', 'поиск', 'поиск по записям']
        self.actions_4_1=['1', '1.', 'доход']
        self.actions_4_2=['2', '2.', 'расход']
        self.actions_4_3=['3', '3.', 'дата']
        self.actions_4_4=['4', '4.', 'сумма']
        self.add_note={
                'Дата': '',
                'Категория': '',
                'Сумма': 0,
                'Описание': ''                
            }

    # Основная функция логики общения с пользователем
    def main(self, deytv: str): 
        work_db=WorkDB()

        # Условие вывода баланса
        if deytv in self.actions_1:
            while True:
                user_input=input('Выберите действие (укажите номер или само действие):\n1. Баланс\n2. Доход\n3. Расход\n> ').lower()
                if user_input in self.actions_1_1:
                    result=work_db.balance()
                    return f'Ваш балланс равен: {result}'
                elif user_input in self.actions_1_2:
                    result=work_db.bal_categ('доход')
                    return f'Ваш доход за всё время: {result}'
                elif user_input in self.actions_1_3:
                    result=work_db.bal_categ('расход')
                    return f'Ваши расходы за всё время: {result}'
                else:
                    print('Нет такого варината ответа')

        # Условие добавления записи
        elif deytv in self.actions_2:
            while True:
                user_input = input('Выберите категорию записи (укажите номер или саму категорию):\n1. Доход\n2. Расход\n> ')
                if user_input.lower() in self.actions_2_1:
                    self.add_note['Категория']='Доход'
                    break
                elif user_input.lower() in self.actions_2_2:
                    self.add_note['Категория']='Расход'
                    break
                else:
                    print('Нет такого варината ответа')
            while True:
                user_input=input('Введите сумму:\n> ')
                try:
                    number=int(user_input)
                    self.add_note['Сумма']=number
                    break
                except ValueError:
                    try:
                        number=float(user_input)
                        self.add_note['Сумма']=number
                        break
                    except ValueError:
                        print('Введите число')
            self.add_note['Описание']=input('Введите описание:\n> ')
            today=datetime.date.today()
            formatted_date=today.strftime("%Y-%d-%m")
            self.add_note['Дата']=formatted_date
            return work_db.add_note(self.add_note)
        
        # Условие редактирования записи
        elif deytv in self.actions_3:
            func_vivod=work_db.search('все', '')
            while True:
                user_input=input('Выберите действие:\n1. Редактировать\n2. Удалить\n> ').lower()
                if user_input in self.actions_3_1:
                    print(f'Все ваши записи:\n{func_vivod}')
                    while True:
                        user_input_index=input('Введите номер записи, которую вы хотите отредактировать:\n> ')
                        try:
                            number=int(user_input_index)
                            break
                        except ValueError:
                            print('Введите число')
                    user_input_type=input('Что вы хотите в ней отредактировать:\n1. Дата\n2. Категория\n3. Сумма\n4. Описание\n> ')
                    if user_input_type in self.actions_3_1_1:
                        user_input_type='Дата'   
                        while True:
                            user_input_zap_now=input('Введите новое значение\n> ')
                            try:
                                date=datetime.datetime.strptime(user_input_zap_now, "%Y-%m-%d")
                                break
                            except ValueError:
                                print('Введите дату правильно') 
                    elif user_input_type in self.actions_3_1_2:
                        user_input_type='Категория'
                        while True:
                            user_input_zap_now=input('Введите новое значение:\n1. Доход\n2. Расход\n> ').lower()
                            if user_input_zap_now in self.actions_3_1_2_1:
                                user_input_zap_now='Доход'
                                break
                            elif user_input_zap_now in self.actions_3_1_2_2:
                                user_input_zap_now='Расход'
                                break
                            else:
                                print('Нет такого варианта ответа')
                    elif user_input_type in self.actions_3_1_3:
                        user_input_type='Сумма'
                        while True:
                            user_input_zap=input('Введите новое значение:\n> ')
                            try:
                                prov_user_input=int(user_input_zap)
                                user_input_zap_now=prov_user_input
                                break
                            except ValueError:
                                try:
                                    prov_user_input=float(user_input_zap)
                                    user_input_zap_now=prov_user_input
                                    break
                                except ValueError:
                                    print('Правильно введите новое значение')    
                    elif user_input_type in self.actions_3_1_4:
                        user_input_type='Описание'
                        user_input_zap_now=input('Введите новое значение:\n>')
                    return work_db.edit_entry(user_input_index, user_input_type, user_input_zap_now)
                elif user_input in self.actions_3_2:
                    print(f'Все ваши записи:\n{func_vivod}')
                    while True:
                        user_input=input('Укажите номер записи, которую надо удалить:\n> ')
                        try:
                            prov_user_input=int(user_input)
                            if prov_user_input > 0:
                                break
                        except ValueError:
                            print('Введите номер записи:\n> ')
                    return work_db.delete(user_input)
                else:
                    print('Нет такого варината ответа')
        
        # Условие для поиска записи
        elif deytv in self.actions_4:
            while True:
                user_input=input('Введите способ поиска записи:\n1. Доход\n2. Расход\n3. Дата\n4. Сумма\n> ').lower()
                if user_input in self.actions_4_1:
                    result=work_db.search('доход', '')
                    return result
                elif user_input in self.actions_4_2:
                    result=work_db.search('расход', '')
                    return result
                elif user_input in self.actions_4_3:
                    while True:
                        user_input=input('Введите дату в формате гггг-мм-дд\n> ')
                        try:
                            date=datetime.datetime.strptime(user_input, "%Y-%m-%d")
                            break
                        except ValueError:
                            print('Введите дату правильно')
                    result=work_db.search('дата', user_input)
                    return result
                elif user_input in self.actions_4_4:
                    while True:
                        user_input=input('Введите сумму:\n> ')
                        try:
                            float(user_input)
                            self.add_note['Сумма']=user_input
                            break
                        except ValueError:
                            print('Введите число')
                    result=work_db.search('сумма', user_input)
                    return result

    # Функция с основным циклом программы
    def run(self) -> None:
        while True:
            user_input=input("Выберите действие (укажите номер или само действие):\n1. Вывод баланса\n2. Добавление записи\n3. Редактирование записи\n4. Поиск по записям\n> ").lower()
            if user_input in self.actions:
                print(self.main(user_input))
            else:
                print('Нет такого варината ответа')    

# Идиома main 
if __name__ == "__main__":
    app=Application()
    app.run()

# Тестовое задание: Разработка консольного приложения "Личный финансовый кошелек"

# Цель: Создать приложение для учета личных доходов и расходов.

# Основные возможности:
# 1. Вывод баланса: Показать текущий баланс, а также отдельно доходы и расходы. СДЕЛАНО
# 2. Добавление записи: Возможность добавления новой записи о доходе или расходе. СДЕЛАНО
# 3. Редактирование записи: Изменение существующих записей о доходах и расходах. СДЕЛАНО
# 4. Поиск по записям: Поиск записей по категории, дате или сумме. СДЕЛАНО

# Требования к программе:
# 1. Интерфейс: Реализация через консоль (CLI), без использования веб- или графического интерфейса (также без использования фреймворков таких как Django, FastAPI, Flask  и тд). СДЕЛАНО
# 2. Хранение данных: Данные должны храниться в текстовом файле. Формат файла определяется разработчиком. СДЕЛАНО
# 3. Информация в записях: Каждая запись должна содержать дату, категорию (доход/расход), сумму, описание (возможны дополнительные поля). СДЕЛАНО

# Будет плюсом:
# 1. Аннотации: Аннотирование функций и переменных в коде. СДЕЛАНО
# 2. Документация: Наличие документации к функциям и основным блокам кода.
# 3. Описание функционала: Подробное описание функционала приложения в README файле.
# 4. GitHub: Размещение кода программы и примера файла с данными на GitHub.
# 5. Тестирование.
# 6. Объектно-ориентированный подход программирования. СДЕЛАНО

# Пример структуры данных в файле:
# Дата: 2024-05-02
# Категория: Расход
# Сумма: 1500
# Описание: Покупка продуктов

# Дата: 2024-05-03
# Категория: Доход
# Сумма: 30000
# Описание: Зарплата

# Это задание направлено на проверку навыков работы с файлами, понимания основ программирования и способности к созданию структурированного и читаемого кода. Удачи в реализации!