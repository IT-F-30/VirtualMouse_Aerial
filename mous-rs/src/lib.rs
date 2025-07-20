use enigo::{Button, Coordinate, Direction, Enigo, Mouse, Settings};
use std::{error::Error, thread, time::Duration};
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError; // これを追加

/// 1. x, y座標を受け取る関数
/// 戻り値がないので PyResult<()> とします
#[pyfunction]
fn rsmove(x: i64, y: i64) -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    move_relative(&mut enigo, x as i32, y as i32)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(())
}

/// 2. クリックを処理する関数
/// 引数がない場合も () が必要です
#[pyfunction]
fn rsclick() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    left_click(&mut enigo)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(())
}

/// 3. 右クリックを処理する関数
#[pyfunction]
fn rsright_click() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    right_click(&mut enigo)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(())
}

/// 4. ダブルクリックを処理する関数
#[pyfunction]
fn rsdouble_click() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    double_left_click(&mut enigo)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(())
}


/// Pythonモジュールを定義する部分
/// wrap_pyfunction!マクロで各関数を登録します
#[pymodule]
fn mous_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rsmove, m)?)?;
    m.add_function(wrap_pyfunction!(rsclick, m)?)?;
    m.add_function(wrap_pyfunction!(rsright_click, m)?)?;
    m.add_function(wrap_pyfunction!(rsdouble_click, m)?)?;
    Ok(())
}


fn move_relative(enigo: &mut Enigo, x: i32, y: i32) -> Result<(), Box<dyn Error>> {
    // 0.1秒かけて滑らかに移動する
    let steps = 20;
    let delay = Duration::from_millis(5); // 5ms * 20 = 100ms
    let dx = x as f32 / steps as f32;
    let dy = y as f32 / steps as f32;
    for i in 0..steps {
        enigo.move_mouse(dx.round() as i32, dy.round() as i32, Coordinate::Rel)?;
        thread::sleep(delay);
    }
    Ok(())
}

/// マウスの左ボタンをクリックします。
fn left_click(enigo: &mut Enigo) -> Result<(), Box<dyn Error>> {
    enigo.button(Button::Left, Direction::Click)?;
    Ok(())
}

/// マウスの右ボタンをクリックします。
fn right_click(enigo: &mut Enigo) -> Result<(), Box<dyn Error>> {
    enigo.button(Button::Right, Direction::Click)?;
    Ok(())
}

/// マウスの左ボタンをダブルクリックします。
fn double_left_click(enigo: &mut Enigo) -> Result<(), Box<dyn Error>> {
    enigo.button(Button::Left, Direction::Click)?;
    // OSがダブルクリックと認識するための短い待機
    thread::sleep(Duration::from_millis(100));
    enigo.button(Button::Left, Direction::Click)?;
    Ok(())
}
