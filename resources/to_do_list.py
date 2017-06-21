from argparse import ArgumentParser
from datetime import date
from root import tdl_log, print_list, create_backup


class ToDoTask:

    def __init__(self, t, d=date.today().strftime("%b %d, %Y")):
        self.date = d
        self.task = t

    def __str__(self):
        return "".join([self.date, '\t', self.task])


def add_item(task_str):
    create_backup(tdl_log)

    new_task = ToDoTask(task_str)
    with open(tdl_log, 'a') as writer:
        writer.write("{t_date}\t{task}".format(t_date=new_task.date, task=new_task.task))
        writer.write('\n')


def delete_item(number_of_item):
    create_backup(tdl_log)
    task_list = load_task_list()

    print "Removing:\n\t {num}) {date} \t {task}".format(
        num=str(number_of_item),
        date=task_list[number_of_item - 1].date,
        task=task_list[number_of_item - 1].task)

    task_list.remove(task_list[number_of_item - 1])

    with open(tdl_log, 'w') as writer:
        for t in task_list:
            if isinstance(t, ToDoTask) is True:
                writer.write("{t_date}\t{task}".format(t_date=t.date, task=t.task))
                writer.write('\n')


def view_to_do_list():

    task_list = load_task_list()
    map(str, task_list)
    print_list(task_list)


def load_task_list():

    lines = open(tdl_log).read().split('\n')
    task_list = []
    for line in lines:
        if len(line) > 0:
            if len(line.split('\t')) > 2:
                print line.split('\t')
            task_date, task_ = line.split('\t')
            task_list.append(ToDoTask(task_, task_date))
    return task_list


if __name__ == "__main__":

    swtiches = []

    p = ArgumentParser()
    p.add_argument("task", type=str, nargs="*", help="add task")

    group = p.add_mutually_exclusive_group()
    group.add_argument("-d", "--delete", type=int, help="delete task")
    group.add_argument("-v", "--view", action="store_true", help="view to do list")

    args = p.parse_args()

    if len(args.task) > 0:
        add_item(" ".join(args.task))

    elif args.delete > -1:
        delete_item(args.delete)

    elif args.view:
        view_to_do_list()

    else:
        task = raw_input("\nEnter task argument: ")
        if len(task) > 1:
            add_item(task)
