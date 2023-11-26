import os
from time import sleep
from datetime import datetime, timedelta, date
from collections import UserList
import pickle
import re
import shutil
import os.path
import numexpr
from abc import ABC, abstractmethod
from colorama import init, Fore, Style


class AddressBook(UserList):

    def __init__(self):

        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        In this case, we have a list attribute called data.

        :param self: Represent the instance of the object itself
        :return: Nothing
        """

        super().__init__()
        self.data = []


    def __str__(self):

        """
        The __str__ function is a special function that returns a string representation of the object.
        This is what you see when you print an object, or convert it to a string using str().
        The __str__ method should return something that looks like this:

        :param self: Refer to the object itself
        :return: A string representation of the object
        """

        result = []
        for contact in self.data:
            result.append(f"name: {contact['name']}"
                          f"phone: {contact['phone']}"
                          f"birthday: {contact['birthday']}"
                          f"email: {contact['email']}"
                          f"status: {contact['status']}"
                          f"note: {contact['note']}")

        return '\n '.join(result)


    def __setitem__(self, key, value):

        """
        The __setitem__ function is a special function that allows you to set the value of an item in a dictionary.
        It takes two arguments: key and value. The key argument is the name of the item, and the value argument is what
        you want to set it equal to.

        :param self: Refer to the instance of the class
        :param key: Identify the contact to be updated
        :param value: Set the value of the key
        :return: The key and value of the dictionary
        """

        self.data[key] = {'name': value.name,
                          'phone': value.phone,
                          'birthday': value.birthday,
                          'email': value.email,
                          'status': value.status,
                          'note': value.note
                          }


    def __getitem__(self, key):

        """
        The __getitem__ function is a special function that allows you to access the data in your
        class as if it were a dictionary.
        For example, if you have an instance of your class called my_instance, then my_instance['key']
        will return the value associated with 'key' in my_instance.data.

        :param self: Represent the instance of the class
        :param key: Access the data in the dictionary
        :return: The value of the given key
        """
        return self.data[key]


    @staticmethod
    def print_contact(record):

        """
        The print_contact function takes a single argument, record, which is a dictionary.
        The function then prints the contents of the dictionary in an easy-to-read format.

        :param record: Pass the dictionary of a contact to the function
        :return: The contact information
        """

        print(' ' +
              Fore.WHITE + '*' * 25 +
              Fore.GREEN + '\n  name: ' +
              Fore.WHITE + f"{record['name']}",
              Fore.GREEN + '\n  phone: ' +
              Fore.WHITE + f"{record['phone']}",
              Fore.GREEN + '\n  birthday: ' +
              Fore.WHITE + f"{record['birthday']}",
              Fore.GREEN + '\n  email: ' +
              Fore.WHITE + f"{record['email']}",
              Fore.GREEN + '\n  status: ' +
              Fore.WHITE + f"{record['status']}",
              Fore.GREEN + '\n  note: ' +
              Fore.WHITE + f"{record['note']}\n" +
              Fore.WHITE + ' ' + '*' * 25)


    def add(self, record):

        """
        The add function adds a new contact to the data list.
            Args:
                record (Contact): The Contact object to be added.

        :param self: Represent the instance of the class
        :param record: Pass the contact information to be added
        :return: The contact that was added
        """

        contact = {'name': record.name,
                   'phone': record.phone,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note
                   }

        self.data.append(contact)
        print(Fore.RED + f'  contact {record.name} added')
        log(f'contact {record.name} added')


    def iterator(self, n):

        """
        The iterator function takes in a number n and returns an iterator that yields
        a list of length n containing the next set of records from the data. If there are
        not enough records to fill a list, it will yield whatever is left.

        :param self: Access the data attribute of the class
        :param n: Determine the number of records to be returned in each iteration
        :return: A generator object
        """

        index = 0
        temp = []
        for record in self.data:
            temp.append(record)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp


    def get_page(self, n):

        """
        The get_page function takes a page number as an argument and prints the
        contents of that page to the screen. It uses a generator function called
        iterator to iterate through each record in self.data, which is a list of
        dictionaries containing contact information.

        :param self: Represent the instance of the class
        :param n: Determine the number of records to be displayed per page
        :return: A generator object
        """

        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                for record in result:
                    print_contact(record)
                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '  press enter for next page>')

            except StopIteration:
                break


    def find_info(self, parameter, pattern):

        """
        The find_info function takes two arguments:
            1. parameter - the key of the dictionary to search for a pattern in
            2. pattern - a string that will be searched for within each value of
                         parameter

        :param self: Access the data attribute of the class
        :param parameter: Specify which field to search for the pattern
        :param pattern: Search for a specific string in the data
        :return: A list of records that match the pattern
        """

        result = []
        for key in self.data:
            if pattern in key[parameter]:
                result.append(key)

        if result:
            for record in result:
                print_contact(record)
        else:
            print(Fore.RED + '  no matches found for pattern')


    def edit(self, name, parameter, new_value):

        """
        The edit function takes in three arguments:
            1. name - the name of the contact to be edited
            2. parameter - the field to be changed (name, phone number, email)
            3. new_value - what you want that field to change into

        :param self: Represent the instance of the class
        :param name: Find the contact in the list
        :param parameter: Specify which parameter of the contact should be edited
        :param new_value: Replace the value of a parameter in the contact dictionary
        :return: Nothing
        """

        for contact in self.data:
            if contact['name'] == name:
                contact[parameter] = new_value
                print(Fore.RED + f'  contact {name} edited')
                log(f'contact {name} edited')
                break
            else:
                continue

    @staticmethod
    def __get_current_week():

        """
        The __get_current_week function returns a list of two datetime.date objects,
        the first being the start date of
        the current week and the second being one week after that. The function is used
        to determine which dates are
        included in a given report.

        :return: A list of two elements
        """

        now = datetime.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=0 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 4)

        return [week_start.date(), week_start.date() + timedelta(days=7)]


    def congratulate(self):

        """
        The congratulate function returns a string with the names of contacts who have birthdays in the current week.
        The function takes no arguments and uses self.data to get all contact data.

        :param self: Represent the instance of the class
        :return: A list of strings
        """

        result = []
        WEEKDAYS = ['', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        congratulate = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': []}
        for contact in self.data:
            if contact['birthday']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                new_birthday = birth_day.replace(year=current_date.year)
                birthday_weekday = new_birthday.weekday() + 1
                if self.__get_current_week()[0] <= new_birthday < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(contact['name'])
                    else:
                        congratulate['monday'].append(contact['name'])
        for k, v in congratulate.items():
            if len(v):
                result.append(Fore.GREEN + f"{k}:" + Fore.WHITE + f" {', '.join(v)}")

        if not result:
            print(Fore.RED + "  contacts not found")

        return '  ' + '\n  '.join(result)


    def days_to_birthday(self, name):

        """
        The days_to_birthday function takes a name as an argument and returns the number
        of days until that person's birthday.
        If the person's birthday has already passed this year, it will return the number of
        days until their next birthday.

        :param self: Refer to the instance of the class
        :param name: Find the contact in the data list
        :return: The number of days left until the birthday of a contact
        """

        for contact in self.data:
            if name == contact['name']:
                birthday = contact['birthday']
                birth_day = datetime.strptime(birthday, '%d.%m.%Y')
                birth_day = date(birth_day.year, birth_day.month, birth_day.day)
                current_date = date.today()
                user_date = birth_day.replace(year=current_date.year)
                delta_days = user_date - current_date
                if delta_days.days >= 0:
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                else:
                    user_date = user_date.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    print(Fore.MAGENTA + f"  {delta_days.days} days left until {name}'s birthday")
                break
        else:
            log('contact not found')
            print(Fore.RED + '  contact not found')


    def delete(self, name):

        """
        The delete function takes a name as an argument and deletes the contact
        from the data list. It first checks if there is a contact with that name,
        if not it prints 'contact not found' and returns None. If there is such
        a contact, it asks for confirmation before deleting it.

        :param self: Represent the instance of the class
        :param name: Find the contact in the list and delete it
        :return: A string
        """

        for key in self.data:
            if key['name'] == name:
                print(Fore.GREEN + '  are you sure for delete contact? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  contact {key["name"]} deleted')
                    log(f'contact {key["name"]} deleted')
                    break
                else:
                    break
        else:
            log('contact not found')
            print(Fore.RED + '  contact not found')


    def clear_book(self):

        """
        The clear_book function clears the data dictionary of all entries.

        :param self: Represent the instance of the class
        :return: Nothing
        """

        self.data.clear()


    def save(self, file_name):

        """
        The save function saves the addressbook to a file.

        :param self: Represent the instance of the class
        :param file_name: Specify the name of the file to save
        :return: The string &quot;addressbook saved&quot;
        """

        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('addressbook saved')


    def load(self, file_name):

        """
        The load function is used to load the addressbook from a file.
            If the file does not exist, it will create one and return an empty dictionary.
            If there is data in the file, it will be loaded into memory as a dictionary.

        :param self: Represent the instance of the class
        :param file_name: Specify the name of the file to be loaded
        :return: The data in the addressbook
        """

        empty_ness = os.stat(file_name)
        if empty_ness.st_size != 0:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
            log('addressbook loaded')
        else:
            print(Fore.RED + '\n  addressbook created')
            log('addressbook created')
        return self.data


class RecordAddressbook:

    def __init__(self, name='', phone='', birthday='', email='', status='', note=''):

        """
        The __init__ function is called when a new instance of the class is created.
        It sets up the attributes of that particular instance.

        :param self: Represent the instance of the class
        :param name: Store the name of the contact
        :param phone: Store the phone number of a contact
        :param birthday: Store the birthday of a contact
        :param email: Set the email attribute of the contact class
        :param status: Determine the status of a contact
        :param note: Store a note about the contact
        :return: The object that was created
        """

        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.status = status
        self.note = note


class FieldAddressbook(ABC):

    @abstractmethod
    def __getitem__(self):

        """
        The __getitem__ function is called when the object is indexed.

        :param self: Represent the instance of the class
        :return: A value from a dictionary
        """

        pass


class NameAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is the first function that is called when you create a new instance of a class.
        It's job is to initialize all of the attributes for an object.

        :param self: Represent the instance of the class
        :param value: Set the value of the object
        :return: The user input
        :doc-author: Trelent
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  name >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we can use:

        :param self: Represent the instance of the class
        :return: The value of the object
        """

        return self.value


class PhoneAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is called when the class is instantiated.
        It sets the value of self.value to whatever was passed in as an argument,
        or if no argument was passed in, it sets self.value to an empty string.

        :param self: Represent the instance of the class
        :param value: Set the value of the phone number
        :return: An instance of the class
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  phone(+380xxxxxxxxx) >>>: ')
            try:
                if re.match(r'^\+380\d{9}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  number')
                print(Fore.RED + '  incorrect number, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we would call foo[]. This function returns
            that value.

        :param self: Represent the instance of the class
        :return: The value of the instance
        """

        return self.value


class BirthdayAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is the first function that gets called when you create a new instance of a class.
        It's job is to initialize all of the attributes of the newly created object.


        :param self: Represent the instance of the class
        :param value: Set the value of the object
        :return: The value of the date entered by the user
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  birthday(dd.mm.YYYY) >>>: ')
            try:
                if re.match(r'^\d{2}.\d{2}.\d{4}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  birthday')
                print(Fore.RED + '  incorrect birthday, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we can use:

        :param self: Represent the instance of the class
        :return: The value of the item
        """

        return self.value


class EmailAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is the first function that gets called when you create a new instance of a class.
        It's job is to initialize all of the attributes of the newly created object.


        :param self: Represent the instance of the class
        :param value: Set the value of the email
        :return: A string
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  email >>>: ')
            try:
                if re.match(r'^(\w|\.|_|-)+@(\w|_|-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect  email')
                print(Fore.RED + '  incorrect email, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we would call foo[]. This function returns
            that value.

        :param self: Represent the instance of the class
        :return: The value of the object
        """

        return self.value


class StatusAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is the first function that gets called when you create a new instance of a class.
        It's job is to initialize all of the attributes of the newly created object.

        :param self: Represent the instance of the class
        :param value: Set the value of the status attribute
        :return: The self
        """

        while True:
            self.status_types = ['', 'family', 'friend', 'work']
            if value:
                self.value = value
            else:
                print(Fore.GREEN + '  status(family, friend, work)')
                self.value = input(Fore.GREEN + '  >>>: ')
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'there is no such status')
                print(Fore.RED + '  incorrect status, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we can use:

        :param self: Represent the instance of the class
        :return: The value of the key
        """

        return self.value


class NoteAddressbook(FieldAddressbook):

    def __init__(self, value=''):

        """
        The __init__ function is called when the class is instantiated.
        It sets the value of self.value to whatever was passed in as an argument,
        or if no argument was passed in, it sets self.value to an empty string.

        :param self: Represent the instance of the class
        :param value: Set the value of the note
        :return: A value, which is the input of the user
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  note >>>: ')
            try:
                if self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'MyClass' called 'my_instance',
            then my_instance[0] will return the first element in my_instance.value.

        :param self: Keep track of specific instances - it binds the attributes with the given arguments
        :return: The value of the instance
        """

        return self.value


class BotAddressbook:

    def __init__(self):

        """
        The __init__ function is called when the class is instantiated.
        It sets up the AddressBook object and assigns it to self.book.

        :param self: Refer to the instance of the class
        :return: The object itself
        """

        self.book = AddressBook()

    def handle(self, command):

        """
        The handle function is the main function of the class.
        It takes a command as an argument and performs actions depending on it.

        :param self: Represent the instance of the class
        :param command: Determine which function to call
        :return: A string that is displayed as a menu item
        """

        try:
            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of note per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except ValueError:
                        print(Fore.RED + '  incorrect number of note, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  addressbook empty')
                            break

            elif command == '2':
                name = NameAddressbook().value.strip().lower()
                if name:
                    if self.book:
                        for item in self.book:
                            if name == item['name']:
                                print(Fore.RED + '\n  this name already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            phone = PhoneAddressbook().value.strip()
                            birth = BirthdayAddressbook().value.strip()
                            email = EmailAddressbook().value.strip()
                            status = StatusAddressbook().value.strip()
                            note = NoteAddressbook().value.strip()
                            record = RecordAddressbook(name, phone, birth, email, status, note)
                            self.book.add(record)
                    else:
                        phone = PhoneAddressbook().value.strip()
                        birth = BirthdayAddressbook().value.strip()
                        email = EmailAddressbook().value.strip()
                        status = StatusAddressbook().value.strip()
                        note = NoteAddressbook().value.strip()
                        record = RecordAddressbook(name, phone, birth, email, status, note)
                        self.book.add(record)
                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '3':
                print(Fore.GREEN + '  parameter to find (name, phone, birthday, email, status, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                pattern = input(Fore.GREEN + '  pattern >>>: ').strip().lower()
                if pattern:
                    self.book.find_info(parameter, pattern)
                else:
                    print(Fore.RED + '  please enter a pattern')

            elif command == '4':
                all_records = []
                for key in self.book:
                    all_records.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_records}')
                print(Fore.GREEN + '  enter the name to edit')
                name = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(name, phone, birthday, email, status, note)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if name in all_records:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit(name, parameter, new_value)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '5':
                print(self.book.congratulate())

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name for birthday')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.days_to_birthday(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['name'])
                print(Fore.WHITE + f'  all names:  {all_titles}')
                print(Fore.GREEN + '  enter the name to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  addressbook cleared')
                        log('addressbook cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  addressbook {file_name} saved')
                else:
                    print(Fore.RED + f'  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  address_book {file_name} loaded')
                else:
                    print(Fore.RED + f'  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def log(command):

    """
    The log function takes in a command and writes it to the logs.txt file with a timestamp.

    :param command: Write the command that was executed to the log file
    :return: The current time and the command that was executed
    """

    current_time = datetime.strftime(datetime.now(), '[%Y-%m-%d] [%H:%M:%S]')
    message = f'{current_time} - {command}'
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


def menu_addressbook():

    """
    The menu_addressbook function prints the main menu of the Addressbook program.
        It takes no arguments and returns nothing.

    :return: A list of strings
    """

    print(Fore.RED + f" {' ' * 9}CLI ASSISTANT BOT")
    print(Style.RESET_ALL + ' ************** ADDRESSBOOK **************\n',
          Fore.GREEN + ' 1. show all contacts\n',
          ' 2. add new contact\n',
          ' 3. find contacts by pattern\n',
          ' 4. edit contact\n',
          ' 5. congratulate contacts\n',
          ' 6. days to birthday\n',
          ' 7. delete contact\n',
          ' 8. clear Addressbook\n',
          ' 9. save Addressbook\n',
          ' 10. load Addressbook\n',
          ' 11. exit\n',
          Style.RESET_ALL + '******************************************\n')


def print_goodbye():

    """
    The print_goodbye function prints a goodbye message to the user.
    
    :return: Nothing
    """
    
    print(Fore.YELLOW + '\n  Good bye!')
    sleep(1)


def addressbook():

    """
    The addressbook function is the main function of this program.
    It initializes a BotAddressbook object, and then enters an infinite loop that displays a menu to the user,
    and handles their input until they choose to exit.  The addressbook function also saves the address book
    when it exits.

    :return: 'exit'
    """

    init()
    file_name = 'ab_save.bin'
    addressbot = BotAddressbook()
    if os.path.exists(file_name):
        addressbot.book.load(file_name)
    else:
        addressbot.book.save(file_name)

    while True:
        os.system('cls')
        menu_addressbook()
        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')
        if user_input == '11':
            addressbot.book.save(file_name)
            print_goodbye()
            return 'exit'

        addressbot.handle(user_input)
        input(Fore.YELLOW + '\n  press Enter to continue')

        if user_input in ['2', '4', '7', '8']:
            addressbot.book.save(file_name)


class NoteBook(UserList):

    def __init__(self):
        
        """    
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        In this case, we have a list attribute called data.
        
        :param self: Represent the instance of the class
        :return: Nothing
        """
        
        super().__init__()
        self.data = []


    def __str__(self):
        
        """    
        The __str__ function is a special function that returns a string representation of the object.
        This is what you see when you print an object, or convert it to a string using str(). 
        The __str__ method should return something that looks like the original data structure, 
        so if we have an instance of our Contact class with name and phone number attributes, 
        we might want to return &quot;Contact(name='John Doe', phone='555-1234')&quot;. 
        
        :param self: Refer to the object itself
        :return: A string representation of the object
        """
        
        result = []
        for contact in self.data:
            result.append(f"title: {contact['title']}"
                          f"note: {contact['note']}"
                          f"tag: {contact['tag']}")
            
        return '\n '.join(result)


    def __setitem__(self, key, value):

        """    
        The __setitem__ function is a special function that allows you to set the value of an item in a dictionary.
        It takes two arguments: key and value. The key argument is the name of the item, and the value argument
        is what you want to store in that item.

        :param self: Refer to the instance of the class
        :param key: Set the key for the dictionary, and value is used to set the value of that key
        :param value: Store the title, note and tag of a new entry
        :return: A dictionary with the key, value and tag
        """

        self.data[key] = {'title': value.title,
                          'note': value.note,
                          'tag': value.tag
                          }


    def __getitem__(self, key):

        """
        The __getitem__ function is a special function that allows you to access the data in your
        class as if it were a dictionary.
        For example, if you have an instance of your class called my_instance, then my_instance['key']
        will return the value associated with 'key' in
        my_instance.data.

        :param self: Represent the instance of the class
        :param key: Access the value of a dictionary
        :return: The value of the key in the dictionary
        """

        return self.data[key]


    @staticmethod
    def print_note(record):
        print(' ' +
              Fore.WHITE + '*' * 25 +
              Fore.GREEN + '\n  title: ' +
              Fore.WHITE + f"{record['title']}",
              Fore.GREEN + '\n  note: ' +
              Fore.WHITE + f"{record['note']}",
              Fore.GREEN + '\n  tag: ' +
              Fore.WHITE + f"{record['tag']}\n" +
              Fore.WHITE + ' ' + '*' * 25)


    def add(self, record):

        """
        The add function adds a record to the data list.
            Args:
                record (Record): The Record object to be added.

        :param self: Represent the instance of the class
        :param record: Add a record to the data list
        :return: The message &quot;record {title} added&quot;
        """

        contact = {'title': record.title,
                   'note': record.note,
                   'tag': record.tag
                   }
        self.data.append(contact)
        print(Fore.RED + f'  record {record.title} added')
        log(f'record {record.title} added')


    def iterator(self, n):

        """
        The iterator function takes in a number n and returns an iterator that yields
        a list of length n containing the next set of records from the data. If there are
        not enough records to fill a list, it will yield whatever is left.

        :param self: Refer to the instance of the class
        :param n: Specify the number of records to be returned in each iteration
        :return: A generator object
        """

        index = 0
        temp = []
        for record in self.data:
            temp.append(record)
            index += 1
            if index >= n:
                yield temp
                temp.clear()
                index = 0
        if temp:
            yield temp


    def get_page(self, n):

        """
        The get_page function takes in a page number and prints out the records
        in that page. It uses an iterator to iterate through the data, and then
        prints out each record in that page.

        :param self: Access the attributes and methods of the class
        :param n: Determine which page of the notebook to display
        :return: The page number, title, note and tag
        """

        gen = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(gen)
                for record in result:
                    print_note(record)

                print(Fore.RED + f'  page {i + 1}')
                input(Fore.YELLOW + '\n  press enter for next page>')

            except StopIteration:
                break

    def add_tag(self, new_tag, title):

        """
        The add_tag function adds a new tag to the list of tags for a given title.
            If the tag already exists, it will not be added again.

        :param self: Access the class attributes
        :param new_tag: Add a new tag to the data list
        :param title: Find the title of the book
        :return: A string
        """

        for key in self.data:
            if key['title'] == title:
                if new_tag in key['tag']:
                    print(Fore.RED + f'  tag {new_tag} already exist')
                    break
                key['tag'].append(new_tag)
                print(Fore.RED + f' the new tag {new_tag} saved')
                break


    def find_note_by_word(self, word):

        """
        The find_note_by_word function takes a word as an argument and searches the notes for that word.
        If it finds any matches, it prints them out to the user.

        :param self: Access the data attribute of the class
        :param word: Search for a note that contains the word
        :return: A list of notes that contain the word
        """

        notes = []
        for key in self.data:
            if word in key['note']:
                notes.append(key)
        if notes:
            for record in notes:
                print_note(record)
        else:
            print(Fore.RED + '  no matches found for the keyword')


    def find_note_by_tag(self, tag):

        """
        The find_note_by_tag function takes a tag as an argument and returns all notes that contain the tag.
            If no matches are found, it prints 'no matches found for the tags'

        :param self: Represent the instance of the class
        :param tag: Search the data dictionary for any notes that contain the tag
        :return: A list of notes that have the specified tag
        """

        tags = []
        for key in self.data:
            if tag in key['tag']:
                tags.append(key)
        if tags:
            for record in tags:
                print_note(record)
        else:
            print(Fore.RED + '  no matches found for the tags')


    def edit_note(self, title, parameter, new_value):

        """
        The edit_note function takes in three parameters:
            1. title - the title of the note to be edited
            2. parameter - the parameter of that note to be edited (title, body, tags)
            3. new_value - what you want to change it too

        :param self: Represent the instance of the class
        :param title: Identify the note to be edited
        :param parameter: Specify which parameter to change
        :param new_value: Change the value of a parameter in a note
        :return: The edited contact
        """

        for key in self.data:
            if key['title'] == title:
                key[parameter] = new_value
                print(Fore.RED + f'  contact {title} edited')
                log(f'contact {title} edited')
                break
            else:
                continue


    def delete(self, name):

        """
        The delete function takes a name as an argument and deletes the record
            with that name from the data. If no such record exists, it prints a message
            to that effect.

        :param self: Represent the instance of the class
        :param name: Find the record to delete
        :return: The record that was deleted
        """

        for key in self.data:
            if key['title'] == name:
                print(Fore.GREEN + '  are you sure for delete note? (y/n)')
                del_contact = input(Fore.BLUE + '  >>>: ')
                if del_contact == 'y':
                    self.data.remove(key)
                    print(Fore.RED + f'  note {key["title"]} deleted')
                    log(f'record {key["title"]} deleted')
                    break
                else:
                    break
        else:
            log('record not found')
            print(Fore.RED + '  record not found')


    def clear_book(self):

        """
        The clear_book function clears the data dictionary of all entries.

        :param self: Represent the instance of the class
        :return: The dictionary with all the values removed
        """

        self.data.clear()


    def save(self, file_name):

        """
        The save function saves the notebook to a file.

        :param self: Represent the instance of the class
        :param file_name: Save the file with a specific name
        :return: The string &quot;notebook saved&quot;
        """

        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)
        log('notebook saved')


    def load(self, file_name):

        """
        The load function takes a file name as an argument and loads the data from that file.
        If the file is empty, it creates a new notebook.

        :param self: Represent the instance of the class
        :param file_name: Specify the name of the file to be loaded
        :return: The data list
        """

        empty_ness = os.stat(file_name)
        if empty_ness.st_size != 0:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
            log('notebook loaded')
        else:
            print(Fore.RED + '\n  notebook created')
            log('notebook created')
        return self.data


class RecordNotebook:
    def __init__(self, title='', note='', tag=None):

        """
        The __init__ function is called when an object is created.
        It sets the initial values for the attributes of a class.

        :param self: Represent the instance of the class
        :param title: Set the title of a note
        :param note: Store the note
        :param tag: Create a list of tags for each note
        :return: Nothing
        """

        self.title = title
        self.note = note
        self.tag = [tag]


class FieldNotebook(ABC):
    @abstractmethod
    def __getitem__(self):

        """
        The __getitem__ function is called when the object is indexed.

        :param self: Represent the instance of the class
        :return: The value of the key in a dictionary
        """

        pass


class TitleNotebook(FieldNotebook):

    def __init__(self, value=''):

        """
        The __init__ function is called when the class is instantiated.
        It sets the value of self.value to whatever was passed in as an argument,
        or if no argument was passed in, it sets self.value to an empty string.

        :param self: Represent the instance of the class
        :param value: Set the value of the title
        :return: Nothing
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  title >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !_-]{1,50}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we can use:

        :param self: Represent the instance of the class
        :return: The value of the object
        """

        return self.value


class NoteNotebook(FieldNotebook):

    def __init__(self, value=''):

        """
        The __init__ function is called when the class is instantiated.
        It sets the value of self.value to whatever was passed in as an argument,
        or if no argument was passed in, it sets self.value to an empty string.

        :param self: Represent the instance of the class
        :param value: Set the value of the note
        :return: The value of the note
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  note >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,250}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')

    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we would call foo[]. This function returns
            that value.

        :param self: Represent the instance of the class
        :return: The value of the key
        """

        return self.value


class TagNotebook(FieldNotebook):

    def __init__(self, value=''):

        """
        The __init__ function is the first function that gets called when you create a new instance of a class.
        It's job is to initialize all of the attributes of the newly created object.

        :param self: Represent the instance of the class
        :param value: Set the value of the tag
        :return: The value of the tag
        """

        while True:
            if value:
                self.value = value
            else:
                self.value = input(Fore.GREEN + '  tag >>>: ')
            try:
                if re.match(r'^[a-zA-Z\d,. !]{1,20}$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                log(f'incorrect value')
                print(Fore.RED + '  incorrect value, try again')


    def __getitem__(self):

        """
        The __getitem__ function is used to access the value of a class instance.
            For example, if we have an instance of the class 'Foo' called foo, and
            we want to get its value, we can use:

        :param self: Represent the instance of the class
        :return: The value of the object
        """

        return self.value


class BotNotebook:

    def __init__(self):

        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and initializes any variables that are necessary
        to track as part of objects of this class.

        :param self: Represent the instance of the class
        :return: The instance of the class
        """

        self.book = NoteBook()


    def handle(self, command):

        """
        The handle function is the main function of the class.
        It takes a command as an argument and performs actions depending on it.


        :param self: Represent the instance of the class
        :param command: Determine which command the user entered
        :return: The command that the user entered
        """
        try:

            if command == '1':
                while True:
                    print(Fore.GREEN + '  number of note per page')
                    try:
                        n = int(input(Fore.BLUE + '  >>>: '))
                    except ValueError:
                        print(Fore.RED + '  incorrect number of note, try again')
                        continue
                    else:
                        if self.book:
                            self.book.get_page(n)
                            break
                        else:
                            print(Fore.RED + '  note_book_vad empty')
                            break

            elif command == '2':
                title = TitleNotebook().value.strip().lower()
                if title:
                    if self.book:
                        for item in self.book:
                            if title == item['title']:
                                print(Fore.RED + '\n  this title already exists\n'
                                                 '  enter command to edit')
                                break
                        else:
                            note = NoteNotebook().value.strip().lower()
                            tag = TagNotebook().value.strip().lower()
                            record = RecordNotebook(title, note, tag)
                            self.book.add(record)
                    else:
                        note = NoteNotebook().value.strip().lower()
                        tag = TagNotebook().value.strip().lower()
                        record = RecordNotebook(title, note, tag)
                        self.book.add(record)

                else:
                    print(Fore.RED + '  please enter a title')

            elif command == '3':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title')
                title = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  add new tag')
                    new_tag = input(Fore.BLUE + '  >>>: ')
                    self.book.add_tag(new_tag, title)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '4':
                print(Fore.GREEN + '  enter the word to find note')
                word = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_word(word)

            elif command == '5':
                print(Fore.GREEN + '  enter the tag to find note')
                tag = input(Fore.BLUE + '  >>>: ')
                self.book.find_note_by_tag(tag)

            elif command == '6':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to edit')
                title = input(Fore.BLUE + '  >>>: ')
                print(Fore.GREEN + '  enter the parameter to edit(title, note, tag)')
                parameter = input(Fore.BLUE + '  >>>: ')
                if title in all_titles:
                    print(Fore.GREEN + '  enter new value')
                    new_value = input(Fore.BLUE + '  >>>: ')
                    self.book.edit_note(title, parameter, new_value)
                else:
                    log('record not found')
                    print(Fore.RED + '  record not found')

            elif command == '7':
                all_titles = []
                for key in self.book:
                    all_titles.append(key['title'])
                print(Fore.WHITE + f'  all titles:  {all_titles}')
                print(Fore.GREEN + '  enter the title to which you want to delete')
                name = input(Fore.BLUE + '  >>>: ')
                if name:
                    self.book.delete(name)
                else:
                    print(Fore.RED + '  please enter a name')

            elif command == '8':
                while True:
                    print(Fore.GREEN + '  are you sure for delete all? (y/n)')
                    clear_all = input(Fore.BLUE + '  >>>: ')
                    if clear_all == 'y':
                        self.book.clear_book()
                        print(Fore.RED + '  note_book_vad cleared')
                        log('note_book_vad cleared')
                        break
                    else:
                        break

            elif command == '9':
                print(Fore.GREEN + '  save file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.save(file_name)
                    print(Fore.RED + f'  note_book_vad {file_name} saved')
                else:
                    print(Fore.RED + '  please enter file name')

            elif command == '10':
                print(Fore.GREEN + '  load file name')
                file_name = input(Fore.BLUE + '  >>>: ').strip()
                if file_name:
                    self.book.load(file_name)
                    print(Fore.RED + f'  note_book_vad {file_name} loaded')
                else:
                    print(Fore.RED + '  please enter file name')

        except Exception as e:
            print(f'{e} invalid input, try again')


def menu_notebook():

    """
    The menu_notebook function prints the menu for the notebook.

    :return: A menu for the notebook
    """

    print(Fore.RED + f" {' ' * 9}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ************** NOTEBOOK **************\n',
          Fore.GREEN + ' 1. show all notes\n',
          ' 2. add new note\n',
          ' 3. add tag for note\n',
          ' 4. find note by word\n',
          ' 5. find note by tag\n',
          ' 6. edit note\n',
          ' 7. delete  note\n',
          ' 8. clear notebook\n',
          ' 9. save notebook\n',
          ' 10. load notebook\n',
          ' 11. exit\n',
          Fore.WHITE + '**************************************\n')


def notebook():

    """
    The notebook function is the main function of the notebook module.
    It creates a BotNotebook object and calls its handle method to process user input.


    :return: The string 'exit'
    """

    init()
    file_name = 'nb_save.bin'
    notebot = notebotNotebook()
    if os.path.exists(file_name):
        notebot.book.load(file_name)
    else:
        notebot.book.load(file_name)

    while True:
        os.system('cls')
        menu_notebook()
        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')

        if user_input == '11':
            notebot.book.save(file_name)
            print_goodbye()
            return 'exit'

        notebot.handle(user_input)
        input(Fore.YELLOW + '\n  press Enter to continue')

        if user_input in ['2', '3', '6', '7', '8']:
            notebot.book.save(file_name)



def about_calculate():

    """
    The about_calculate function prints a description of the calculator.

    :return: The description of the calculator
    """

    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ******************** DESCRIPTION *******************\n',
          Fore.GREEN + ' to use the calculator in the line, enter the\n',
          ' mathematical operation of the example "5+12/9",and\n',
          ' to get the result of the calculation, press Enter\n',
          Fore.WHITE + '****************************************************\n')


def menu_calculate():

    """
    The menu_calculate function prints the calculator menu to the console.

    :return: The user's choice
    """

    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** CALCULATOR ******\n',
          Fore.GREEN + ' 1. about\n',
          ' 2. run calculator\n',
          ' 3. exit\n',
          Fore.WHITE + '************************\n')


def calculate():
    """
    The calculate function is the main function of the calculator module.
    It allows users to perform basic mathematical operations on numbers.

    :return: The exit value
    """

    init()
    while True:
        os.system('cls')
        menu_calculate()

        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')

        if user_input == '1':
            os.system('cls')
            about_calculate()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 6}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** CALCULATOR **********')
            print(Fore.GREEN + '  enter a mathematical operation')
            operation = input(Fore.BLUE + '  >>>: ')
            try:
                result = numexpr.evaluate(operation)
                print(Fore.MAGENTA + f"  result: {result}")
                input(Fore.YELLOW + '\n  press Enter to continue')
            except ValueError:
                print(Fore.RED + '\n  incorrect operating, try again')
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue
            except ZeroDivisionError:
                print(Fore.RED + '\n  incorrect operating division by zero, try again')
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print_goodbye()
            return 'exit'


def normalize(name):

    """
    The normalize function takes a string as an argument and returns the same string with all Cyrillic characters
    replaced by their Latin equivalents. The function also replaces spaces, punctuation marks, and other symbols with
    underscores.

    :param name: Pass the name of the file to be normalized
    :return: A string that is the same as the input
    """

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!#$%&()*+,-/:;<>=?@[]^~{|}'\\`. "
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",
        "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
        "_",
        "_", "_", "_", "_", "_", "_", "_", "_", "_")
    TRANS = {}
    CYRILLIC = tuple(CYRILLIC_SYMBOLS)

    for c, l in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    if re.search(r'\..{2,5}$', name):
        s_res = re.search(r'\..{2,5}$', name)
        suffix = s_res.group()
        name = name.removesuffix(suffix)
        name = name.translate(TRANS)
        name += suffix
    else:
        name = name.translate(TRANS)
    return name


def move_file(files_pattern, path, el, dst):

    """
    The move_file function takes in three arguments:
        1. files_pattern - a list of regex patterns to match against the file names
        2. path - the directory where all the files are located
        3. dst - destination folder for matched files

    :param files_pattern: Search for the file in the directory
    :param path: Specify the path of the directory where we want to search for files
    :param el: Represent the file name in the path
    :param dst: Specify the destination path
    :return: Nothing
    """

    for doc_pattern in files_pattern:
        if re.search(doc_pattern, el):
            new_el = normalize(el)
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)

            try:
                shutil.copy(src, dst)
                print(Fore.WHITE + "  file is copied successfully", el)
                os.remove(src)
                print(Fore.WHITE + "  file is deleted successfully", el)

            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file", el)
                os.remove(src)
                print(Fore.RED + "  file is deleted successfully", el)

            except PermissionError:
                print(Fore.RED + "  permission denied", el)

            except Exception:
                print(Fore.RED + "  error occurred while copying file", el)


def move_unknown_file(file_pattern, path, el, dst):

    """
    The move_unknown_file function takes in three arguments:
        1. files_pattern - a list of regular expressions that match the file types we want to keep
        2. path - the directory where all our files are located
        3. el - an element from os.listdir(path) which is a string representing one of the files in path
            (this will be used as part of our source and destination paths)

    :param file_pattern: Determine whether the file is a document or not
    :param path: Specify the path to the folder where we want to move files from
    :param el: Get the name of the file
    :param dst: Specify the destination folder
    :return: Nothing
    """

    for doc_pattern in file_pattern:
        if re.search(doc_pattern, el) is None:
            new_el = normalize(el)
            src = os.path.join(path, el)
            dst = os.path.join(dst, new_el)
            try:
                shutil.copy(src, dst)
                os.remove(src)
                print(Fore.WHITE + "  file is copied successfully")
            except shutil.SameFileError:
                print(Fore.RED + "  source and destination represents the same file")
            except PermissionError:
                print(Fore.RED + "  permission denied")
            except OSError:
                pass


def rec_sort(path):

    """
    The move_unknown_file function takes in three arguments:
     1. path - the directory where all our files are located
    :param path: Specify the directory where all our files are located
    :return: Nothing
    """

    new_folders = ['images',
                   'documents',
                   'audio',
                   'video',
                   'archives',
                   'programs',
                   'unknown']

    for el in new_folders:
        try:
            os.mkdir(path + '\\' + el)
        except FileExistsError:
            print(Fore.RED + f"  file already exists: {el}")
        except OSError:
            print(Fore.RED + f"  error creating folder: {el}")

    dst_doc = os.path.join(path, 'documents')
    dst_img = os.path.join(path, 'images')
    dst_aud = os.path.join(path, 'audio')
    dst_vid = os.path.join(path, 'video')
    dst_arh = os.path.join(path, 'archives')
    dst_prg = os.path.join(path, 'programs')
    dst_un = os.path.join(path, 'unknown')
    el_list = os.listdir(path)

    for folder in new_folders:
        for el in el_list:
            if folder == el:
                el_list.remove(el)
    for el in el_list:
        image_files = ['\.jpeg$', '\.png$', '\.jpg$', '\.svg$', '\.tiff$', '\.tif$', '\.bmp$', '\.gif$']
        video_files = ['\.avi$', '\.mp4$', '\.mov$', '\.mkv$', '\.3gp$', '\.3g2$', '\.mpg$', '\.mpeg$']
        doc_files = ['\.doc$', '\.docx$', '\.txt$', '\.pdf$',
                     '\.xls$', '\.xlsx$', '\.pptx$', '\.mpp$', '\.html$', '\.csv$', '\.bin$', '\.rtf$']
        audio_files = ['\.mp3$', '\.ogg$', '\.wav$', '\.amr$', '\.mid$', '\.midi$', '\.mpa$', '\.wma$']
        arch_files = ['\.zip$', '\.gz$', '\.tar$', '\.7z$', '\.rar$']
        program_files = ['\.exe$', '\.bat$', '\.apk$']
        unknown_files = []
        unknown_files.extend(image_files)
        unknown_files.extend(video_files)
        unknown_files.extend(doc_files)
        unknown_files.extend(audio_files)
        unknown_files.extend(arch_files)
        unknown_files.extend(program_files)

        if not os.path.isdir(path + '\\' + el):
            move_file(image_files, path, el, dst_img)
            move_file(video_files, path, el, dst_vid)
            move_file(doc_files, path, el, dst_doc)
            move_file(audio_files, path, el, dst_aud)
            move_file(arch_files, path, el, dst_arh)
            move_file(program_files, path, el, dst_prg)
            move_unknown_file(unknown_files, path, el, dst_un)
        elif os.path.isdir(path + '\\' + el):
            rec_sort(path + '\\' + el)


def delete_empty_folders(path):

    """
    The delete_empty_folders function takes in one argument:
     1. path - the directory where all our files are located

    :param path: Specify the directory where all our files are located
    :return: Nothing
    """

    for el in os.listdir(path):
        if os.path.isdir(path + '\\' + el):
            try:
                os.rmdir(path + '\\' + el)
                print(Fore.WHITE + "  directory '%s' has been removed successfully" % (path + '\\' + el))
                log("directory '%s' has been removed successfully" % (path + '\\' + el))
                delete_empty_folders(path)
            except OSError:
                log("directory '%s' can not be removed" % (path + '\\' + el))
                delete_empty_folders(path + '\\' + el)


def about_filesort():
    """


    """
    print(Fore.RED + f" {' ' * 18}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ********************* DESCRIPTION ********************\n',
          Fore.GREEN + ' the script helps to sort files in folders according\n',
          ' to popular file types as a result, files will be \n',
          ' moved into folders: <images>, <documents>,\n',
          ' <audio>, <video>, <archives>, <programs>, <unknown>\n',
          ' if the folder does\'t contain files of some file\n',
          ' type then a new folder for this type will not create\n',
          Fore.WHITE + '*******************************************************\n')


def menu_filesort():
    print(Fore.RED + f" {' ' * 4}CLI ASSISTANT BOT")
    print(Fore.WHITE + ' ****** FILE SORT ******\n',
          Fore.GREEN + ' 1. about\n',
          ' 2. run file sort\n',
          ' 3. exit\n',
          Fore.WHITE + '************************\n')


def filesort():

    """
    The filesort function is a CLI menu that allows the user to sort files in a directory.
    The user can choose from three options:
        1) About - displays information about the function and how it works.
        2) Sort - sorts all files in a given directory into subdirectories based on file type.
            The subdirectories are created if they do not already exist, and empty directories
            are deleted after sorting is complete.
            If an error occurs during sorting, the program will display an error message and return to main menu.

    :return: The filesort function
    """

    init()
    while True:
        os.system('cls')
        menu_filesort()
        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')

        if user_input == '1':
            os.system('cls')
            about_filesort()
            input(Fore.YELLOW + '  press Enter to continue')

        elif user_input == '2':
            os.system('cls')
            print(Fore.RED + f" {' ' * 7}CLI ASSISTANT BOT")
            print(Fore.WHITE + ' ********** FILE SORT **********')
            print(Fore.GREEN + '  input the file path')
            path = input(Fore.BLUE + '  >>>: ')
            try:
                if os.path.exists(path):
                    rec_sort(path)
                    delete_empty_folders(path)
                    print(Fore.MAGENTA + '\n  sorting completed successfully')
                    input(Fore.YELLOW + '\n  press Enter to continue')
                else:
                    print(Fore.RED + f'\n  path {path} is not found, try again')
                    log(f'path {path} is not found, try again')
                    input(Fore.YELLOW + '\n  press Enter to continue')

            except Exception:
                input(Fore.YELLOW + '\n  press Enter to continue')
                continue

        elif user_input == '3':
            print_goodbye()
            return 'exit'


def main():
    """
    The main function
    :return:
    :rtype:
    """
    init()
    while True:
        os.system('cls')
        print(Fore.RED + f" {' ' * 11}CLI ASSISTANT BOT")
        print(Fore.WHITE + ' **************** MENU ****************\n',
              Fore.GREEN + ' 1. address book\n',
              ' 2. note book\n',
              ' 3. file sort\n',
              ' 4. calculator\n',
              ' 5. exit\n',
              Fore.WHITE + '***************************************\n')

        user_input = input(Fore.BLUE + '  your choose(number)>>>: ')

        if user_input == '1':
            result = addressbook()
            if result == 'exit':
                continue

        elif user_input == '2':
            result = notebook()
            if result == 'exit':
                continue

        elif user_input == '3':
            result = filesort()
            if result == 'exit':
                continue

        elif user_input == '4':
            result = calculate()
            if result == 'exit':
                continue

        elif user_input == '5':
            print_goodbye()
            break


if __name__ == '__main__':
    main()
