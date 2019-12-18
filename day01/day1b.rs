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
        result += meta_fuel(number);
    }
    println!("{}", result);
    Ok(())
}

fn meta_fuel(x : i64) -> i64{
    let mut f = 0;
    let mut additional_fuel = fuel(x);

    while additional_fuel > 0{
        f += additional_fuel;
        additional_fuel = fuel(additional_fuel);
    }
    return f;
}

fn fuel(x : i64) -> i64{
    return (x / 3) - 2;
}
