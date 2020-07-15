# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()




class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

class ToDoList:

    def __init__(self, dbname='todo.db'):
        engine = create_engine(f'sqlite:///{dbname}?check_same_thread=False')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add(self, task, task_date):
        new_row = Table(task=task,
         deadline=task_date)
        self.session.add(new_row)
        self.session.commit()
        print('The task has beed added!\n')

    def show_date(self, task_date, day_name=None):
        rows = self.session.query(Table).filter(Table.deadline == task_date.date()).all()
        day_name = task_date.strftime('%A') if day_name is None else day_name
        month_name = task_date.strftime('%b')
        print(f'{day_name} {task_date.day} {month_name}:')
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for number, item in enumerate(rows, 1):
                print(f'{number}) {item.task}')
        print('')

    def show_today(self):
        print('')
        self.show_date(datetime.today(), day_name='Today')

    def show_week(self):
        print('')
        today = datetime.today()
        i = 0
        while i <= 6:
            week_day = today + timedelta(days=i)
            self.show_date(week_day)
            i += 1

    def show_all(self, topic, nothing):
        self.topic = topic
        self.nothing = nothing
        print(self.topic)
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print(self.nothing)
        else:
            for number, item in enumerate(rows, 1):
                print(f'{number}) {item.task}. {item.deadline.day} {item.deadline.strftime("%b")}')
  #              print(item.deadline)

    def delete_row(self, delete_input):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        self.session.delete(rows[delete_input])
        self.session.commit()
        print('The task has been deleted!\n')

    def missed_task(self):
        print('\nMissed task:')
        rows = self.session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for number, item in enumerate(rows, 1):
                print(f'{number}) {item.task}. {item.deadline.day} {item.deadline.strftime("%b")}')
        print('')

    def show_commands(self):
        print('1) Today\'s tasks')
        print('2) Week\'s tasks')
        print('3) All tasks')
        print('4) Missed tasks')
        print('5) Add task')
        print('6) Delete task')
        print('0) Exit')

tasks = ToDoList()

while True:
    tasks.show_commands()
    user_command = input()
    if user_command == '1':
        tasks.show_today()
    elif user_command == '2':
        tasks.show_week()
    elif user_command == '3':
        tasks.show_all('All tasks:', 'Nothing to do!')
    elif user_command == '4':
        tasks.missed_task()
    elif user_command == '5':
        print('')
        task = input('Enter task\n')
        task_date = datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d')
        tasks.add(task, task_date)
    elif user_command == '6':
        tasks.show_all('Chose the number of task you want to delete:', 'Nothing to delete')
        delete_input = int(input())
        tasks.delete_row(delete_input)
    elif user_command == '0':
        print('\nBye!')
        break
