use enigo::{Button, Coordinate, Direction, Enigo, Mouse, Settings};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::{error::Error, thread, time::Duration};

// マウス移動の設定
const SMOOTH_STEPS: usize = 10; // 滑らかな移動のステップ数
const STEP_DELAY_MS: u64 = 3; // 各ステップ間の遅延（ミリ秒）

/// x, y座標を受け取ってマウスを移動する関数
#[pyfunction]
fn rsmove(x: i64, y: i64) -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(format!("Enigo初期化エラー: {}", e)))?;

    move_relative(&mut enigo, x as i32, y as i32)
        .map_err(|e| PyValueError::new_err(format!("マウス移動エラー: {}", e)))?;
    Ok(())
}

/// 左クリックを実行する関数
#[pyfunction]
fn rsclick() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(format!("Enigo初期化エラー: {}", e)))?;

    left_click(&mut enigo).map_err(|e| PyValueError::new_err(format!("クリックエラー: {}", e)))?;
    Ok(())
}

/// 右クリックを実行する関数
#[pyfunction]
fn rsright_click() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(format!("Enigo初期化エラー: {}", e)))?;

    right_click(&mut enigo)
        .map_err(|e| PyValueError::new_err(format!("右クリックエラー: {}", e)))?;
    Ok(())
}

/// ダブルクリックを実行する関数
#[pyfunction]
fn rsdouble_click() -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default())
        .map_err(|e| PyValueError::new_err(format!("Enigo初期化エラー: {}", e)))?;

    double_left_click(&mut enigo)
        .map_err(|e| PyValueError::new_err(format!("ダブルクリックエラー: {}", e)))?;
    Ok(())
}

/// Pythonモジュールを定義
#[pymodule]
fn mous_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rsmove, m)?)?;
    m.add_function(wrap_pyfunction!(rsclick, m)?)?;
    m.add_function(wrap_pyfunction!(rsright_click, m)?)?;
    m.add_function(wrap_pyfunction!(rsdouble_click, m)?)?;
    Ok(())
}

/// マウスを滑らかに相対移動する
fn move_relative(enigo: &mut Enigo, x: i32, y: i32) -> Result<(), Box<dyn Error>> {
    // 小さな移動の場合は分割しない
    if x.abs() <= 5 && y.abs() <= 5 {
        enigo.move_mouse(x, y, Coordinate::Rel)?;
        return Ok(());
    }

    // 滑らかな移動のために分割
    let delay = Duration::from_millis(STEP_DELAY_MS);
    let dx = x as f32 / SMOOTH_STEPS as f32;
    let dy = y as f32 / SMOOTH_STEPS as f32;

    for _ in 0..SMOOTH_STEPS {
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
