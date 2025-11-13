import sys

NUM_BAYS = 12
MAX_DAYS = NUM_BAYS * 365


def count_gen():
    """
    Counter generator to add indices to tasks.
    """
    id = 0
    while True:
        yield id
        id += 1


def dnc(tasks: list[tuple[int, int, int]], max_hours=MAX_DAYS) -> tuple[int, list[int]]:
    """
    Simple divide and conquer approach to solve the task selection problem.
    DO NOT USE THIS FUNCTION, IT IS INEFFICIENT FOR LARGE INPUTS.
    2^n TIME COMPLEXITY.
    """
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
    return worth_2, [id] + res_2


def dp(tasks: list[tuple[int, int, int]], max_hours=MAX_DAYS):
    """
    Dynamic programming approach to solve the task selection problem.
    """
    n = len(tasks)
    dp_table = [[0] * (max_hours + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, duration, priority = tasks[i - 1]
        revenue = duration * priority
        for j in range(max_hours + 1):
            task_row = dp_table[i - 1]
            if duration > j:
                dp_table[i][j] = task_row[j]
                continue
            dp_table[i][j] = max(
                task_row[j],
                task_row[j - duration] + revenue,
            )
    res = []
    j = max_hours
    for i in range(n, 0, -1):
        if dp_table[i][j] != dp_table[i - 1][j]:
            id, duration, priority = tasks[i - 1]
            res.append(id)
            j -= duration
    res.reverse()
    return res, dp_table


def main(path, output_path="output.txt"):
    with open(path) as f:
        tasks = []
        id_gen = count_gen()
        _ = f.readline()
        for line in f:
            if not line.strip():
                continue
            priority, duration = list(map(int, line.split(",")))
            tasks.append((next(id_gen), duration, priority))
    (res, _) = dp(tasks[::-1])
    with open(output_path, "w") as f:
        f.write(f"{len(res)}\n")
        f.write("\n".join(map(str, res)))


if __name__ == "__main__":
    main(sys.argv[1])
