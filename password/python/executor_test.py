import subprocess
from concurrent.futures import ThreadPoolExecutor


def do_task(task_id):
    print(f"开始处理任务 {task_id}")

    # 每个任务调用一个外部命令，比如 echo
    result = subprocess.run(["echo", f"任务 {task_id} 完成"], capture_output=True, text=True)
    print(result.stdout.strip())


def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(100):
            executor.submit(do_task, i)


if __name__ == "__main__":
    main()

# cd D:\tools\password\ ; python executor_test.py
