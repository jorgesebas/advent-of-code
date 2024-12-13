use std::time::Instant;

fn blink_stones(mut stones: Vec<i64>, blinks: usize) -> Vec<i64> {
    let mut blink_num = 0;
    for _ in 0..blinks {
        blink_num += 1;
        let progreso: String = format!("{: <width$}", "#".repeat(blink_num + 1), width = blinks);
        print!("\r[{}] {}/{}", progreso, blink_num, blinks);
        std::io::Write::flush(&mut std::io::stdout()).unwrap();

        let mut new_stones = Vec::new();
        for &stone in &stones {
            if stone == 0 {
                new_stones.push(1);
            } else if stone.to_string().len() % 2 == 0 {
                let num_str = stone.to_string();
                let mid = num_str.len() / 2;
                let left: i64 = num_str[..mid].parse().unwrap();
                let right: i64 = num_str[mid..].parse().unwrap();
                new_stones.push(left);
                new_stones.push(right);
            } else {
                new_stones.push(stone * 2024);
            }
        }
        stones = new_stones;
    }
    println!();
    stones
}

fn main() {
    let start = Instant::now();
    let initial_stones = vec![2, 72, 8949, 0, 981038, 86311, 246, 7636740];
    println!("Piedras iniciales => {:?}", initial_stones);
    let blinks = 75;
    println!("Número de parpadeos: {}", blinks);
    let final_stones = blink_stones(initial_stones, blinks);
    println!("Número de piedras después de {} parpadeos: {}", blinks, final_stones.len());
    println!("{:.2} ms", start.elapsed().as_secs_f64() * 1000.0);
}
