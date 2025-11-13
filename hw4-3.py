import sys

NUM_BAYS = 12

type Task = tuple[int, int, int]  # (id, start_day, priority)


def count_gen():
    id = 0
    while True:
        yield id
        id += 1


def dnc(tasks: list[Task], max_hours=NUM_BAYS * 365) -> tuple[int, list[int]]:
    if not tasks:
        return 0, []
    task = tasks.pop()
    id, duration, priority = task
    if duration > max_hours:
        return dnc(tasks, max_hours)
    revenue = duration * priority
    worth_1, res_1 = dnc(tasks[:], max_hours)
    worth_2, res_2 = dnc(tasks[:], max_hours - duration)
    if worth_1 > (worth_2 := worth_2 + revenue):
        return worth_1, res_1
    return worth_2, res_2 + [id]


def main(path, output_path="output.txt"):
    with open(path) as f:
        tasks = []
        id_gen = count_gen()
        _ = f.readline()
        for line in f:
            if not line.strip():
                continue
            duration, priority = list(map(int, line.split(",")))
            tasks.append((next(id_gen), duration, priority))
    tasks_sorted = sorted(tasks, key=lambda x: x[2], reverse=True)
    worth, res = dnc(tasks_sorted)
    with open(output_path, "w") as f:
        f.write(f"{len(res)}\n")
        f.write(",".join(map(str, res)) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
