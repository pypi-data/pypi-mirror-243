use chrono::Datelike;
use pyo3::prelude::*;

#[pyfunction]
pub fn var(varstring: &str, prefix: &str) -> String {
    let now = chrono::Local::now();
    let vars = varstring.split("%");
    let mut generated: String = "".to_owned();

    for partial in vars {
        let val = match partial {
            "yyyy" => now.year().to_string(),
            "yy" => last_two_chars(now.year().to_string()),
            "mm" => add_0(now.month().to_string()),
            "m" => now.month().to_string(),
            "dd" => add_0(now.day().to_string()),
            "d" => now.day().to_string(),
            _ => "UNMATCHED".to_string(),
        };

        if !(val == "UNMATCHED") {
            generated.push_str(&val);
        }
    }

    // If prefix is an empty string, we ignore it
    if prefix.is_empty() {
        return generated;
    }

    return prefix.to_string() + &generated;
}

// Get the last two characters of a string
fn last_two_chars(mut val: String) -> String {
    let len = val.chars().count();
    val.drain(0..len - 2);
    return val;
}

// Prepend 0 to a day/month if its only one char long
fn add_0(val: String) -> String {
    let len = val.chars().count();

    if len == 1 {
        return "0".to_string() + &val;
    }

    return val;
}
