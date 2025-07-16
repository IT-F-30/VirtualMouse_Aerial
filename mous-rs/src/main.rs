use enigo::{Button, Coordinate, Direction, Enigo, Mouse, Settings};
use std::{thread, time::Duration};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut enigo = Enigo::new(&Settings::default())?;

    thread::sleep(Duration::from_secs(2));

    println!("マウスを相対位置 (100, 50) へ移動します...");
    enigo.move_mouse(100, 50, Coordinate::Rel)?;
    thread::sleep(Duration::from_secs(1));

    println!("左クリックします...");
    enigo.button(Button::Left, Direction::Click)?;
    thread::sleep(Duration::from_secs(1));

    println!("右クリックします...");
    enigo.button(Button::Right, Direction::Click)?;
    thread::sleep(Duration::from_secs(1));

    println!("ダブルクリックします...");
    enigo.button(Button::Left, Direction::Click)?;
    thread::sleep(Duration::from_millis(100));
    enigo.button(Button::Left, Direction::Click)?;

    println!("完了しました。");

    Ok(())
}