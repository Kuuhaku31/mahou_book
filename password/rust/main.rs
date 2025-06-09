// test

use chrono; // Import chrono for date and time formatting
use indicatif::{ProgressBar, ProgressStyle}; // 引入 indicatif
use rayon::prelude::*;
use std::env;
use std::io::Write; // Import the Write trait to use the flush method
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{atomic::AtomicBool, Arc};
use std::time::Instant;
mod rust_7z;

fn 记录日志(日志文件地址: String, 内容: String) {
    let mut 文件 = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(日志文件地址)
        .expect("无法打开文件");

    let 当前时间 = chrono::Local::now()
        .format("[%Y-%m-%d %H:%M:%S] ")
        .to_string();

    if let Err(e) = writeln!(文件, "{}{}", 当前时间, 内容) {
        eprintln!("写入日志失败：{}", e);
    }
}

fn 测试密码(密码字符串: String, 文件地址: String) -> bool {
    let 状态 = Command::new("7z")
        .arg("t")
        .arg(format!("-p{}", 密码字符串))
        .arg(文件地址)
        .stdout(std::process::Stdio::null()) // 屏蔽标准输出
        .stderr(std::process::Stdio::null()) // 屏蔽标准错误
        .status()
        .expect("执行 7z 命令失败");

    if 状态.success() {
        println!("\n7z 验证成功！密码是：{}", 密码字符串);
        return true;
    } else {
        return false;
    }
}

// 传递范围，密码长度，文件地址
fn 测试1(开始: u64, 结束: u64, 密码长度: usize, 文件地址: String, 日志文件地址: String) {
    let 测试范围_str = format!("[{}, {})", 开始, 结束);
    let 总数 = 结束 - 开始;
    let 开始时间 = Instant::now();
    let 开始时间_str = chrono::Local::now()
        .format("[%Y-%m-%d %H:%M:%S]")
        .to_string();

    println!("开始测试...");
    println!("当前时间：{}", 开始时间_str);
    println!("测试范围：{}，共有 {} 个密码", 测试范围_str, 总数);
    println!("密码长度：{}", 密码长度);
    println!("文件地址：{}", 文件地址);

    // 初始化进度条
    let pb = ProgressBar::new(总数);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("#>-"),
    );

    let 找到了 = Arc::new(AtomicBool::new(false)); // 共享的终止信号
    let 密码字符串 = Arc::new(std::sync::Mutex::new(String::new())); // 用于存储找到的密码
    let 已处理计数 = Arc::new(AtomicU64::new(0)); // 用于记录已处理的数量

    // 用并行方式处理
    (开始..结束).into_par_iter().for_each_with(
        (找到了.clone(), 密码字符串.clone(), 已处理计数.clone()),
        |(找到了吗, 密码字符串, 已处理计数), i| {
            // 检查是否已经找到密码
            if 找到了吗.load(Ordering::Relaxed) {
                return;
            }

            // 测试密码
            let 测试密码字符串: String = format!("{:0>密码长度$}", i);
            if 测试密码(测试密码字符串.clone(), 文件地址.clone()) {
                找到了吗.store(true, Ordering::Relaxed);
                let mut 密码锁 = 密码字符串.lock().unwrap();
                *密码锁 = 测试密码字符串.clone(); // 更新找到的密码
            }

            // 更新进度条
            if !找到了吗.load(Ordering::Relaxed) {
                已处理计数.fetch_add(1, Ordering::Relaxed);
                pb.inc(1);
            }

            // 定期保存日志
            if i % 1000 == 0 {
                let 已处理 = 已处理计数.load(Ordering::Relaxed);
                let 内容 = format!(
                    "测试范围：{}，开始时间：{}，已处理 {} 个密码，当前密码：{}",
                    测试范围_str, 开始时间_str, 已处理, 测试密码字符串
                );
                记录日志(日志文件地址.clone(), 内容);
            }
        },
    );

    println!("\n程序结束！");
    let mut 内容 = format!(
        "范围：{}，开始时间：{}，共处理了 {} 个密码，耗时：{:?}，使用了 {} 个线程，",
        测试范围_str,
        开始时间_str,
        已处理计数.load(Ordering::Relaxed),
        开始时间.elapsed(),
        rayon::current_num_threads(),
    );
    if 找到了.load(Ordering::Relaxed) {
        内容.push_str(&format!("找到密码：{}", 密码字符串.lock().unwrap()));
    } else {
        内容.push_str("没有找到密码。");
    }
    println!("{}", 内容);
    记录日志(日志文件地址.clone(), 内容);
}

fn main() {
    let args: Vec<String> = env::args().collect(); // 获取命令行参数

    if args[1] == "t" {
        测试密码("95895952".to_string(), "D:/def/tt95895952.rar".to_string());
        return;
    } else {
        测试1(
            args[1].parse::<u64>().unwrap(),
            args[2].parse::<u64>().unwrap(),
            args[3].parse::<usize>().unwrap(),
            args[4].clone(),
            args[5].clone(),
        );
    }
}

// D:/tools/password/def.rar
// 7z t -p"141592" "D:/tools/password/def.rar"
// .rust_test 95880000 95900000 8 "D:\def\target.rar" "D:\def\log.txt"
//           95895952
