use pyo3::prelude::*;
mod constants;
mod methods;

/// A Python module implemented in Rust.
#[pymodule]
fn simpleuid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(methods::alphanumeric::alphanumeric, m)?)?;
    m.add_function(wrap_pyfunction!(methods::numeric::numeric, m)?)?;
    m.add_function(wrap_pyfunction!(methods::alpha::alpha, m)?)?;
    m.add_function(wrap_pyfunction!(methods::var::var, m)?)?;
    Ok(())
}
