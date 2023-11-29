use crate::constants::{ALPHANUMERIC, ALPHANUMERIC_LOWER, ALPHANUMERIC_UPPER};
use pyo3::prelude::*;
use rand::Rng;

#[pyfunction]
pub fn alphanumeric(length: usize, prefix: &str, case: &str) -> String {
    let mut rng = rand::thread_rng();

    // Define charset based on user selection
    let charset: &[u8] = match case {
        "upper" => ALPHANUMERIC_UPPER,
        "lower" => ALPHANUMERIC_LOWER,
        _ => ALPHANUMERIC,
    };

    let generated: String = (0..length)
        .map(|_| {
            let idx = rng.gen_range(0..charset.len());
            charset[idx] as char
        })
        .collect();

    // If prefix is an empty string, we ignore it
    if prefix.is_empty() {
        return generated;
    }

    return prefix.to_string() + &generated;
}
