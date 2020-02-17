use fnv::{FnvHashMap, FnvHashSet};
use std::collections::HashSet;
use std::fs;
use std::time::Instant;

extern crate fnv;

fn mov((x, y): (i32, i32), direction: char) -> (i32, i32) {
    match direction {
        'U' => (x, y + 1),
        'D' => (x, y - 1),
        'R' => (x + 1, y),
        'L' => (x - 1, y),
        _ => unreachable!(),
    }
}

struct Point {
    // marker: char,
    distance: u32,
}

type Grid = FnvHashMap<(i32, i32), Point>;
type Wire = Vec<String>;

fn fill_grid(wire: &Wire) -> Grid {
    let mut grid = Grid::default();
    let mut current_location = (0, 0);
    let mut total_distance = 0;
    for instruction in wire {
        let direction = instruction.as_bytes()[0] as char;
        let distance_str = &instruction[1..];
        let distance: u32 = distance_str.parse().unwrap();
        for _i in 0..distance {
            total_distance += 1;
            current_location = mov(current_location, direction);
            if !grid.contains_key(&current_location) {
                if direction == 'L' || direction == 'R' {
                    let point = Point {
                        /*marker: '-', */ distance: distance,
                    };
                    grid.insert(current_location, point);
                }
                if direction == 'U' || direction == 'D' {
                    let point = Point {
                        /* marker: '|', */ distance: distance,
                    };
                    grid.insert(current_location, point);
                }
            }
            grid.insert(
                current_location,
                Point {
                    /* marker: '+', */ distance: total_distance,
                },
            );
        }
    }
    println!("total len: {}", grid.len());
    return grid;
}

fn manhattan_distance((x, y): (i32, i32), _grids: &Vec<Grid>) -> u32 {
    return (x.abs() + y.abs()) as u32;
}

fn total_distance((x, y): (i32, i32), grids: &Vec<Grid>) -> u32 {
    return grids
        .iter()
        .map(|grid: &Grid| grid.get(&(x, y)).unwrap().distance)
        .sum();
}

type MetricFunction = fn(location: (i32, i32), grids: &Vec<Grid>) -> u32;

// type Intersections = Intersection<'_, (i32, i32), std::collections::hash_map::RandomState>;

fn find_intersections(wires: Vec<Wire>) -> (Vec<Grid>, HashSet<(i32, i32)>) {
    let mut now = Instant::now();
    let grids: Vec<_> = wires.iter().map(|x| fill_grid(x)).collect();
    println!("Created grids {}", now.elapsed().as_millis());

    now = Instant::now();
    let grid_1_keys: HashSet<_> = grids[0].keys().cloned().collect();
    let grid_2_keys: HashSet<_> = grids[1].keys().cloned().collect();
    println!("Created hashsets {}", now.elapsed().as_millis());
    let mut now = Instant::now();
    let intersections: HashSet<_> = grid_1_keys.intersection(&grid_2_keys).cloned().collect();
    println!("Found Intersections {}", now.elapsed().as_millis());
    return (grids, intersections);
}

fn find_closest_intersection(
    grids: &Vec<Grid>,
    metric: MetricFunction,
    intersections: &HashSet<(i32, i32)>,
) -> u32 {
    let mut now = Instant::now();
    let mut distances: Vec<_> = intersections
        .iter()
        .map(|&pos| metric(pos, &grids))
        .collect();
    distances.sort();
    let closest = distances[0];
    println!("Found closest distance {}", now.elapsed().as_millis());
    return closest;
}

fn _array_to_wire(wire: &[&str]) -> Wire {
    return wire.iter().map(|st| st.to_string()).collect();
}

fn main() {
    let filename = "input.txt";

    let data = fs::read_to_string(filename).unwrap();
    let lines: Vec<String> = data.split("\n").map(|st| st.to_string()).collect();
    let wires: Vec<Wire> = lines
        .iter()
        .map(|line| line.split(",").map(|x| x.to_string()).collect())
        .collect();

    let (grids, intersections) = find_intersections(wires);
    println!(
        "{}",
        find_closest_intersection(&grids, manhattan_distance, &intersections)
    );
    println!(
        "{}",
        find_closest_intersection(&grids, total_distance, &intersections)
    );

    // let wire1a = array_to_wire(&["R8", "U5", "L5", "D3"]);
    // let wire1b = array_to_wire(&["U7", "R6", "D4", "L4"]);
    // println!("{}", find_intersection(vec![&wire1a, &wire1b], manhattan_distance));

    // let wire2a = array_to_wire(&["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"]);
    // let wire2b = array_to_wire(&["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]);
    // println!("{}", find_intersection(vec![&wire2a, &wire2b], manhattan_distance));

    // let wire3a = array_to_wire(&["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"]);
    // let wire3b = array_to_wire(&["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]);
    // println!("{}", find_intersection(vec![&wire3a, &wire3b], manhattan_distance));

    // println!("{}", find_intersection(vec![&wires[0], &wires[1]], manhattan_distance));

    // println!("{}", find_intersection(vec![&wire1a, &wire1b], total_distance));
    // println!("{}", find_intersection(vec![&wire2a, &wire2b], total_distance));
    // println!("{}", find_intersection(vec![&wire3a, &wire3b], total_distance));
    // println!("{}", find_intersection(vec![&wires[0], &wires[1]], total_distance));
}
