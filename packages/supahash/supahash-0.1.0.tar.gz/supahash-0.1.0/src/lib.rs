use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sha3::{Digest, Keccak256};


#[pyfunction]
fn keccak_256(py: Python, input: &[u8]) -> PyResult<PyObject> {
    let mut hasher = Keccak256::new();
    hasher.update(input);
    let result = hasher.finalize();

    // Convert the hash to bytes and return as a Python bytes object
    Ok(PyBytes::new(py, &result).into())
}

/// A Python module implemented in Rust.
#[pymodule]
fn supahash(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(keccak_256, m)?)?;
    Ok(())
}
