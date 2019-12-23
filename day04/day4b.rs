use std::io;
extern crate regex;
use regex::Regex as Regex;

fn check(i: u32, re1: &Regex, re2: &Regex) -> bool{
    let as_string = i.to_string();
    let matched : bool = false;
    for cap in re1.captures_iter(&as_string) {
        for i in 1..10{
            if let Some(val) = cap.get(i){
                if val.as_str().len() == 2 {
                    return true;
                }
            }
        }
    }
    return false;
}

fn main() -> io::Result<()>  {
    let min = 264793;
    let max = 803935;
    let mut count = 0;
    let re1 : Regex = Regex::new(r"^(1+)?(2+)?(3+)?(4+)?(5+)?(6+)?(7+)?(8+)?(9+)?$").unwrap();
    re1.find(&"abcd".to_string());
    let re2 : Regex = Regex::new(r".*").unwrap();
    for i in min..max{
        if check(i, &re1, &re2){
            println!("Matched: {}",i);
            count += 1;
        }
    }
    println!("Matches: {}", count);
        
    Ok(())
}
