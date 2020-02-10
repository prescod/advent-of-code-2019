use std::io;
use std::fs;

mod intcode;

//  To read:

// https://doc.rust-lang.org/1.30.0/book/second-edition/ch07-01-mod-and-the-filesystem.html

fn main() -> io::Result<()>  {
    let filename = "day2.txt";
    let goal = 19690720;


    for num1 in 0..100{
        for num2 in 0..100{
                let data = fs::read_to_string(filename).unwrap();
                let parts : Vec<_> = data.split(",").collect();
                let mut nums : Vec<intcode::Word> = parts.iter()
                    .map(|num_str| num_str.to_string().parse::<intcode::Word>())
                    .map(|x|x.unwrap()).collect();
                    nums[1] = num1;
            nums[2] = num2;
            let result = intcode::compute(nums);
            if result==goal{
                println!(" FOUND ! {}", 100 * num1 + num2 );
            }
        }
    }   

    Ok(())
}

