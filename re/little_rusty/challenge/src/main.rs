use std::{
    env::args,
    fs::read,
    io::{stdout, Write},
    process::exit,
};

#[derive(Debug)]
struct VM {
    program: Vec<Instruction>,
    stack: Vec<u8>,
    instruction_pointer: usize,
}

#[derive(Debug)]
enum Instruction {
    Push(u8),
    Pop,
    Print,
    Xor(u8),
    Add(u8),
    Mul(u8),
    Jmpf(u8),
    Jmpb(u8),
    Nop,
    Invalid,
}

impl VM {
    fn new() -> Self {
        Self {
            program: Vec::new(),
            stack: Vec::new(),
            instruction_pointer: 0,
        }
    }

    fn load_program(&mut self, filename: &str) {
        let program_bytes = read(filename).unwrap();
        let mut i = 0;
        while i < program_bytes.len() {
            let cur_instruction = program_bytes[i];
            let serialized = match cur_instruction {
                0xCB => {
                    i += 1;
                    Instruction::Push(program_bytes[i])
                }
                0xF5 => Instruction::Pop,
                0xD2 => Instruction::Print,
                0x64 => {
                    i += 1;
                    Instruction::Xor(program_bytes[i])
                }
                0x79 => {
                    i += 1;
                    Instruction::Add(program_bytes[i])
                }
                0x7A => {
                    i += 1;
                    Instruction::Mul(program_bytes[i])
                }
                0xDB => {
                    i += 1;
                    Instruction::Jmpf(program_bytes[i])
                }
                0xBD => {
                    i += 1;
                    Instruction::Jmpb(program_bytes[i])
                }
                0x4F => Instruction::Nop,
                _ => Instruction::Invalid,
            };
            self.program.push(serialized);
            i += 1;
        }
    }

    fn exec_next_instruction(&mut self) {
        let cur_instruction = &self.program[self.instruction_pointer];
        match cur_instruction {
            Instruction::Push(val) => {
                self.stack.push(*val);
            }
            Instruction::Pop => {
                self.stack.pop();
            }
            Instruction::Print => {
                let to_print = self.stack.pop().unwrap();
                print!("{}", to_print as char);
                stdout().flush().unwrap();
            }
            Instruction::Xor(val) => {
                let mut new_val = self.stack.pop().unwrap();
                new_val ^= val;
                self.stack.push(new_val);
            }
            Instruction::Add(val) => {
                let mut new_val = self.stack.pop().unwrap();
                new_val += val;
                self.stack.push(new_val);
            }
            Instruction::Mul(val) => {
                let mut new_val = self.stack.pop().unwrap();
                new_val *= val;
                self.stack.push(new_val);
            }
            Instruction::Jmpf(val) => {
                // -1 corrects for incoming self.instruction_pointer += 1;
                self.instruction_pointer += *val as usize - 1;
            }
            Instruction::Jmpb(val) => {
                // +1 corrects for incoming self.instruction_pointer += 1;
                self.instruction_pointer -= *val as usize + 1;
            }
            Instruction::Nop => (),
            Instruction::Invalid => todo!(),
        }
    }

    fn run(&mut self) {
        while self.instruction_pointer < self.program.len() {
            self.exec_next_instruction();
            self.instruction_pointer += 1;
        }
    }
}

fn main() {
    let mut vm = VM::new();
    let cli_args: Vec<String> = args().collect();
    if cli_args.len() < 2 {
        eprintln!("Usage: {} <program_file>", cli_args[0]);
        exit(1);
    }
    let program_file = &cli_args[1];
    vm.load_program(program_file);
    vm.run();
}
