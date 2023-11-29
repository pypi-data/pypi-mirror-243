use crate::constants::{ALPHA, ALPHA_LOWER, ALPHA_UPPER};
use pyo3::prelude::*;
use rand::Rng;

#[pyfunction]
pub fn alpha(length: usize, prefix: &str, case: &str) -> String {
    let mut rng = rand::thread_rng();

    // Define charset based on user selection
    let charset: &[u8] = match case {
        "upper" => ALPHA_UPPER,
        "lower" => ALPHA_LOWER,
        _ => ALPHA,
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
