use std::io::{self, BufReader};
use std::io::prelude::*;
use std::fs::File;

fn main() -> io::Result<()>  {
    let filename = "input.txt";

    let f = File::open(filename)?;
    let f = BufReader::new(f);
    let mut result = 0;

    for line in f.lines() {
        let l = line.unwrap();
        let number: i64 = l.parse().unwrap();
        result += fuel(number);
    }
    println!("{}", result);
    Ok(())
}

fn fuel(x : i64) -> i64{
    return (x / 3) - 2;
}
