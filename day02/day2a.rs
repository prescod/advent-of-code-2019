use std::io;
use std::fs;
use std::collections::HashMap;

extern crate serde_derive;
extern crate serde;
extern crate serde_json;

type Word = u128;
type Ptr = usize;

type Callback = fn(&mut Computer, x: Word, y: Word, out: Ptr);

struct Computer{
    memory: Vec<Word>,
    position: usize,
}

fn add(c : &mut Computer, x: Word, y: Word, out: Ptr){
    c.memory[out] = x + y;
}

fn mul(c : &mut Computer, x: Word, y: Word, out: Ptr){
    c.memory[out] = x * y;
}

fn commands() -> HashMap<Word, Callback>{
    let mut commands : HashMap<Word, Callback> = HashMap::new();
    commands.insert(1, add);
    commands.insert(2, mul);
    return commands;
}

fn compute(memory: Vec<Word>){
    let mut computer = Computer{position: 0, memory: memory};
    let mut opcode: Word = computer.memory[computer.position];
    let commands  = commands();
    while opcode != 99{
        if let Some(func) = commands.get(&opcode) {
            let pos = computer.position as Ptr;
            let op1 = computer.memory[computer.memory[pos + 1] as Ptr];
            let op2 = computer.memory[computer.memory[pos+ 2] as Ptr];
            let out = computer.memory[pos + 3] as Ptr;
            {
                func(&mut computer,op1, op2, out);
            }
        }else{
            println!("unknown opcode: {}", opcode);
        }
    
        computer.position += 4;
        opcode = computer.memory[computer.position];
    }
    println!("{}", computer.memory[0])
}

fn main() -> io::Result<()>  {
    let filename = "day2.txt";

    let data = fs::read_to_string(filename).unwrap();
    let parts : Vec<_> = data.split(",").collect();
    let mut nums : Vec<Word> = parts.iter()
            .map(|num_str| num_str.to_string().parse::<Word>())
            .map(|x|x.unwrap()).collect();

    nums[1] = 12;
    nums[2] = 2;

    compute(nums);

    Ok(())
}

