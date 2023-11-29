use crate::constants::NUMERIC;
use pyo3::prelude::*;
use rand::Rng;

#[pyfunction]
pub fn numeric(length: usize, prefix: &str) -> String {
    let mut rng = rand::thread_rng();

    let generated: String = (0..length)
        .map(|_| {
            let idx = rng.gen_range(0..NUMERIC.len());
            NUMERIC[idx] as char
        })
        .collect();

    // If prefix is an empty string, we ignore it
    if prefix.is_empty() {
        return generated;
    }

    return prefix.to_string() + &generated;
}
