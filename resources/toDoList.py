from sys import argv
from datetime import date
from root import toDoListTextFile, switchParser, printList, createBackUp, \
    setClipboardData, chooseFromList, errorAlert

AVAILABLE_SWITCHES = ['a', 'v', 'd', 's']


class ToDoTask:

    def __init__(self, t, d=date.today().strftime("%b %d, %Y")):
        self.__date = d
        self.__task = t

    def get_date(self):
        return self.__date

    def get_task(self):
        return self.__task

    def __str__(self):
        return "".join([self.get_date(), '\t', self.get_task()])


def add_item(new_task):
    createBackUp(toDoListTextFile)

    new_task = ToDoTask(new_task)
    with open(toDoListTextFile, 'a') as writer:
        writer.write('\n')
        writer.write(
            str("".join([new_task.get_date(), "\t", new_task.get_task()])))


def delete_item(number_of_item):

    createBackUp(toDoListTextFile)
    task_list = load_task_list()

    print "Removing:\n\t {num} ) {date} \t {task}".format(
        num=str(number_of_item), date=task_list[number_of_item - 1].get_date(),
        task=task_list[number_of_item - 1].get_task())

    task_list.remove(task_list[number_of_item - 1])

    with open(toDoListTextFile, 'w') as writer:
        for t in task_list:
            if isinstance(t, ToDoTask) is True:
                writer.write(str("".join([t.get_date(), "\t", t.get_task()])))
                if task_list.index(t) != len(task_list) - 1:
                    writer.write('\n')


def view_to_do_list():

    task_list = load_task_list()
    map(str, task_list)
    printList(task_list)


def load_task_list():

    task_list = open(toDoListTextFile).read().split('\n')
    for i in range(0, len(task_list)):
        if len(task_list[i]) > 0:
            task_list[i] = ToDoTask(task_list[i].split(
                '\t')[1], task_list[i].split('\t')[0])

    return task_list


def handle_select():

    task_list = load_task_list()
    if 's' in switches:

        try:
            if len(switches['s']) > 0:
                result = task_list[int(switches['s'])].getTask()
            else:
                result = chooseFromList(task_list).get_task()

            print result
            setClipboardData(result)
        except IndexError:
            raise
            errorAlert("Choice is out of bounds.")

        except ValueError:
            errorAlert("Value of 's' switch must be an integer")


if __name__ == "__main__":

    switches = switchParser(argv)

    if 'a' in switches:
        if len(argv) > 1:
            add_item(" ".join(map(str, argv[1:])))
        else:
            task = raw_input("\nEnter task argument: ")
            if len(task) > 1:
                add_item(task)

    elif 'd' in switches:
        delete_item(int(argv[1]))

    elif 'v' in switches:
        view_to_do_list()

        handle_select()
