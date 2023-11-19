import psycopg2

DSN = 'postgresql://postgres:********@localhost:5432/clients'

# Значения переменных для меню выбора действий
cr_table = 1  # создать таблицу
cr_client = 2  # создать клиента
cr_phone = 3  # создать телефон
up_client = 4  # обновить данные по клиенту
del_phone = 5  # удалить телефон
del_client = 6  # удалить клиента
f_client = 7  # найти клиента
exit_menu = 8


def main():
    choice = 0
    while choice != exit_menu:
        display_menu()
        choice = choice_menu()
        if choice == cr_table:
            create_table()
        elif choice == cr_client:
            create_client()
        elif choice == cr_phone:
            create_phone()
        elif choice == up_client:
            update_client()
        elif choice == del_phone:
            delete_phone()
        elif choice == del_client:
            delete_client()
        elif choice == f_client:
            find_client()


def display_menu():  # главное меню
    print('Выберите одно из действий и нажмите:\n'
          '1 создать таблицу\n'
          '2 создать клиента\n'
          '3 добавить телефон\n'
          '4 обновить данные по клиенту\n'
          '5 удалить телефон клиента\n'
          '6 удалить клиента\n'
          '7 найти клиента\n'
          '8 выйти из меню\n'
          )


def choice_menu():
    choice = int(input('Вы хотите: '))  # выбор меню
    return choice


def create_table():  # создаем таблицу
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE client CASCADE;"
                        "DROP TABLE phonebook;")

            cur.execute("CREATE TABLE IF NOT EXISTS client(client_id SERIAL PRIMARY KEY,"
                        "client_name VARCHAR(50) CHECK (client_name != ''),"
                        "client_surname VARCHAR(100) CHECK (client_surname != ''),"
                        "email VARCHAR(100) UNIQUE CHECK (email != ''));")

            cur.execute("CREATE TABLE IF NOT EXISTS phonebook(phone_id SERIAL PRIMARY KEY,"
                        "phone_number VARCHAR(12) UNIQUE CHECK (phone_number != ''),"
                        "client_id INTEGER REFERENCES client(client_id) ON DELETE CASCADE);")

    conn.close()
    print('Таблица создана')


def create_client():  # запрашиваем данные клиента
    name = input('Введите имя клиента: ')
    surname = input('Введите фамилию клиента: ')
    email = input('Введите email: ')
    insert_client(name, surname, email)


def insert_client(name, surname, email):  # добавляем клиента
    conn = None
    try:
        conn = psycopg2.connect(DSN)
        with conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO client(client_name, client_surname, email)"
                            "VALUES (%s, %s, %s);", (name, surname, email))
                conn.commit()
            print("Клиент создан")
    except psycopg2.errors.UniqueViolation as error:
        print('Такой email уже существует', error)
    except psycopg2.errors.CheckViolation as error:
        print('Поле не может быть пустым', error)
    finally:
        if conn is not None:
            conn.close()


def create_phone():
    email = input('Введите email, чтобы добавить телефон: ')
    search_email(email)


def search_email(email):
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT client_id FROM client WHERE email = %s;", (email,))
            client_id = cur.fetchone()
            if client_id is not None:
                print(client_id)
                insert_phone(client_id)
            else:
                print('Клиент с данным email отсутствует, попробуйте еще раз')
    conn.close()


def insert_phone(client_id):  # добавить телефон
    question = input('Добавить номер телефона / Выход в меню Y/N: ')
    if question.lower() == "y":
        phone = input('Введите номер телефона: ')
        conn = None
        try:
            conn = psycopg2.connect(DSN)
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO phonebook (phone_number, client_id)"
                                "VALUES (%s, %s);""", (phone, client_id[0]))
                    insert_phone(client_id)
        except psycopg2.errors.UniqueViolation as error:
            print('Такой номер уже существует', error)
        except psycopg2.errors.CheckViolation as error:
            print('Номер телефона не может быть пустым', error)
        finally:
            if conn is not None:
                conn.close()


def update_client():  # обновить данные о клиенте
    email = input('Введите email, для поиска клиента: ')
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM client WHERE email = %s;""", (email,))
            data_client = cur.fetchall()
            if data_client != []:
                update_name(email)
            else:
                print('Клиент с данным email отсутствует, попробуйте еще раз')
    conn.close()


def update_name(email):
    email = email
    name_question = input('Обновить имя клиента Y/N: ')
    if name_question.lower() == "y":
        new_name = input('Введите новое имя клиента: ')
        conn = psycopg2.connect(DSN)
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE client SET client_name = %s"
                            "WHERE email = %s;", (new_name, email))
                print('Имя обновлено')
        conn.close()
    else:
        print('Имя не обновляем')
    update_surname(email)


def update_surname(email):
    email = email
    surname_question = input('Обновить фамилию клиента Y/N: ')
    if surname_question.lower() == "y":
        new_surname = input('Введите новую фамилию клиента: ')
        conn = psycopg2.connect(DSN)
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE client SET client_surname = %s "
                            "WHERE email = %s;", (new_surname, email))
                print('Фамилия обновленa')
        conn.close()
    else:
        print('Фамилию не обновляем')
    update_email(email)


def update_email(email):
    email = email
    email_question = input('Обновить email клиента Y/N: ')
    if email_question.lower() == "y":
        new_email = input('Введите новый email клиента: ')
        conn = psycopg2.connect(DSN)
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE client SET email = %s "
                            "WHERE email = %s;", (new_email, email))
                print('email обновлен')
        conn.close()
        update_phone(new_email)
    else:
        print('email не обновляем')
        update_phone(email)


def update_phone(email):
    email = email
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT phone_id, phone_number "
                        "FROM client FULL JOIN phonebook USING (client_id) "
                        "WHERE email = %s;", (email,))
            data_client = cur.fetchall()
            if data_client != []:
                print(data_client)
                phone_question = input('Хотите обновить телефон Y/N: ')
                if phone_question.lower() == "y":
                    phone_id = int(input('Введите id телефона: '))
                    new_phone = input('Введите новый телефон: ')
                    cur.execute("UPDATE phonebook SET phone_number = %s "
                                "WHERE phone_id = %s;", (new_phone, phone_id))
                    print('Телефон обновлен')
            else:
                print('Клиент не имеет номера телефона')
    conn.close()


def delete_phone():  # удалить телефон
    email = input('Введите email, для поиска клиента: ')
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM client INNER JOIN phonebook "
                        "USING (client_id) WHERE email = %s;", (email,))
            data_client = cur.fetchall()
            if data_client != []:
                print(data_client)
                phone_id = int(input('Введите id телефона клиента для удаления: '))
                cur.execute("DELETE FROM phonebook "
                            "WHERE phone_id = %s;", (phone_id,))
                print('Телефон удален')
            else:
                print('У клиента отсутствует телефон')
    conn.close()


def delete_client():  # удалить клиента
    email = input('Введите email, для поиска клиента: ')
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT client_id FROM client "
                        "WHERE email = %s;", (email,))
            client_id = cur.fetchone()
            if client_id is not None:
                print(client_id)
                client_id = int(input('Введите id клиента для удаления: '))
                # cur.execute("""DELETE FROM phonebook WHERE client_id = %s;
                #             DELETE FROM client WHERE client_id = %s""", (client_id, client_id))
                cur.execute("""DELETE FROM client WHERE client_id = %s;""", (client_id,))
                print('Клиент удален')
            else:
                print('Клиент с данным email отсутствует, попробуйте еще раз')
    conn.close()


def find_client():  # поиск клиента
    search_client = input('Введите данные, для поиска клиента: ')
    conn = psycopg2.connect(DSN)
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM client FULL JOIN phonebook USING (client_id)"
                        "WHERE to_tsvector('russian', client_name) || "
                        "to_tsvector('russian', client_surname) || "
                        "to_tsvector('english', email) || "
                        "COALESCE (to_tsvector('russian', phone_number), '', '(Null)') "
                        "@@ plainto_tsquery('russian',%s);", (search_client,))
            data_client = cur.fetchall()
            if data_client != []:
                print(data_client)
            else:
                print('Клиент или номер телефона отсутствует в базе')
    conn.close()


if __name__ == '__main__':
    main()
