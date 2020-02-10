use std::collections::HashMap;

pub type Word = u128;
pub type Ptr = usize;

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

pub fn compute(memory: Vec<Word>) -> Word{
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
    return computer.memory[0];
}
