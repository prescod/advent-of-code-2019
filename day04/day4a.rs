use std::io;
extern crate fancy_regex;
use fancy_regex::Regex as Regex;

fn check(i: u32, re1: &Regex, re2: &Regex) -> bool{
    let as_string = i.to_string();
    let matches = re1.is_match(&as_string).unwrap();
    let rc = matches && re2.is_match(&as_string).unwrap();

    return rc;
}

fn main() -> io::Result<()>  {
    let min = 264793;
    let max = 803935;
    let mut count = 0;
    let re1 : Regex = Regex::new(r"(\d)\1").unwrap();
    let re2 : Regex = Regex::new(r"^1*2*3*4*5*6*7*8*9*$").unwrap();
    for i in min..max{
        if check(i, &re1, &re2){
            println!("Matches: {}",i);
            count += 1;
        }
    }
    println!("Matches: {}", count);
        
    Ok(())
}
