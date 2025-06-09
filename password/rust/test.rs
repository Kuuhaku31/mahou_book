use std::thread;
use std::time::Duration;

fn main()
{
    // 创建一个新线程
    let handle = thread::spawn(|| {
        for i in 1..5
        {
            println!("子线程: {}", i);
            thread::sleep(Duration::from_millis(500));
        }
    });

    // 主线程继续执行
    for i in 1..3
    {
        println!("主线程: {}", i);
        thread::sleep(Duration::from_millis(500));
    }

    // 等子线程执行完
    handle.join().unwrap();
}
