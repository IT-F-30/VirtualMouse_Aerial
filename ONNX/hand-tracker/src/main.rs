use image::{DynamicImage, GenericImageView, ImageBuffer, Rgb, RgbImage};use image::{DynamicImage, GenericImageView, ImageBuffer, Rgb, RgbImage};

use imageproc::drawing::{draw_filled_circle_mut, draw_line_segment_mut};use imageproc::drawing::{draw_filled_circle_mut, draw_line_segment_mut};

use minifb::{Key, Window, WindowOptions};use minifb::{Key, Window, WindowOptions};

use nokhwa::Camera;use nokhwa::Camera;

use nokhwa::pixel_format::RgbFormat;use nokhwa::pixel_format::RgbFormat;

use nokhwa::utils::{CameraIndex, RequestedFormat, RequestedFormatType};use nokhwa::utils::{CameraIndex, RequestedFormat, RequestedFormatType};

use tract_onnx::prelude::*;use tract_onnx::prelude::*;



// 型定義を簡潔にする// 型定義を簡潔にする

type Model = SimplePlan<TypedFact, Box<dyn TypedOp>, Graph<TypedFact, Box<dyn TypedOp>>>;type Model = SimplePlan<TypedFact, Box<dyn TypedOp>, Graph<TypedFact, Box<dyn TypedOp>>>;



// 手のランドマークの接続関係（MediaPipe Hand準拠）// 手のランドマークの接続関係（MediaPipe Hand準拠）

const HAND_CONNECTIONS: &[(usize, usize)] = &[const HAND_CONNECTIONS: &[(usize, usize)] = &[

    // 親指    // 親指

    (0, 1), (1, 2), (2, 3), (3, 4),    (0, 1), (1, 2), (2, 3), (3, 4),

    // 人差し指    // 人差し指

    (0, 5), (5, 6), (6, 7), (7, 8),    (0, 5), (5, 6), (6, 7), (7, 8),

    // 中指    // 中指

    (0, 9), (9, 10), (10, 11), (11, 12),    (0, 9), (9, 10), (10, 11), (11, 12),

    // 薬指    // 薬指

    (0, 13), (13, 14), (14, 15), (15, 16),    (0, 13), (13, 14), (14, 15), (15, 16),

    // 小指    // 小指

    (0, 17), (17, 18), (18, 19), (19, 20),    (0, 17), (17, 18), (18, 19), (19, 20),

    // 手のひら    // 手のひら

    (5, 9), (9, 13), (13, 17),    (5, 9), (9, 13), (13, 17),

];];



fn draw_landmarks(img: &mut RgbImage, landmarks: &[f32], img_width: u32, img_height: u32) {fn draw_landmarks(img: &mut RgbImage, landmarks: &[f32], img_width: u32, img_height: u32) {

    let num_landmarks = landmarks.len() / 3;    let num_landmarks = landmarks.len() / 3;

        

    // ランドマークの接続線を描画    // ランドマークの接続線を描画

    for &(start_idx, end_idx) in HAND_CONNECTIONS {    for &(start_idx, end_idx) in HAND_CONNECTIONS {

        if start_idx < num_landmarks && end_idx < num_landmarks {        if start_idx < num_landmarks && end_idx < num_landmarks {

            let x1 = landmarks[start_idx * 3] * img_width as f32;            let x1 = landmarks[start_idx * 3] * img_width as f32;

            let y1 = landmarks[start_idx * 3 + 1] * img_height as f32;            let y1 = landmarks[start_idx * 3 + 1] * img_height as f32;

            let x2 = landmarks[end_idx * 3] * img_width as f32;            let x2 = landmarks[end_idx * 3] * img_width as f32;

            let y2 = landmarks[end_idx * 3 + 1] * img_height as f32;            let y2 = landmarks[end_idx * 3 + 1] * img_height as f32;

                        

            draw_line_segment_mut(            draw_line_segment_mut(

                img,                img,

                (x1, y1),                (x1, y1),

                (x2, y2),                (x2, y2),

                Rgb([0u8, 255u8, 0u8]), // 緑色の線                Rgb([0u8, 255u8, 0u8]), // 緑色の線

            );            );

        }        }

    }    }

        

    // ランドマークの点を描画    // ランドマークの点を描画

    for i in 0..num_landmarks {    for i in 0..num_landmarks {

        let x = landmarks[i * 3] * img_width as f32;        let x = landmarks[i * 3] * img_width as f32;

        let y = landmarks[i * 3 + 1] * img_height as f32;        let y = landmarks[i * 3 + 1] * img_height as f32;

                

        // 画像の範囲内かチェック        // 画像の範囲内かチェック

        if x >= 0.0 && x < img_width as f32 && y >= 0.0 && y < img_height as f32 {        if x >= 0.0 && x < img_width as f32 && y >= 0.0 && y < img_height as f32 {

            draw_filled_circle_mut(            draw_filled_circle_mut(

                img,                img,

                (x as i32, y as i32),                (x as i32, y as i32),

                5,                5,

                Rgb([255u8, 0u8, 0u8]), // 赤色の点                Rgb([255u8, 0u8, 0u8]), // 赤色の点

            );            );

        }        }

    }    }

}}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. ONNXモデルを読み込む
    println!("ONNXモデルを読み込んでいます...");
    let model: Model = tract_onnx::onnx()
        .model_for_path("../models/hand_landmark_full.onnx")?
        .into_optimized()?
        .into_runnable()?;

    println!("モデルの読み込みが完了しました。");

    // 2. Webカメラを開く
    println!("Webカメラを初期化しています...");
    let index = CameraIndex::Index(0);

    // より単純な設定でカメラを初期化
    let requested = RequestedFormat::new::<RgbFormat>(RequestedFormatType::HighestResolution(
        nokhwa::utils::Resolution::new(640, 480),
    ));

    println!("カメラデバイスを作成中...");
    let mut camera = Camera::new(index, requested)?;

    println!("カメラストリームを開いています...");
    camera.open_stream()?;

    println!("Webカメラを起動しました。ESCキーまたはウィンドウを閉じて終了します。");

    // 3. プレビューウィンドウを作成
    let window_width = 640;
    let window_height = 480;
    let mut window = Window::new(
        "Hand Tracker Preview",
        window_width,
        window_height,
        WindowOptions::default(),
    )?;

    // ウィンドウの更新レートを制限
    window.limit_update_rate(Some(std::time::Duration::from_millis(33))); // 約30 FPS

    let mut frame_count = 0;
    while window.is_open() && !window.is_key_down(Key::Escape) {
        // 4. フレームをキャプチャ
        let frame = match camera.frame() {
            Ok(frame) => frame,
            Err(e) => {
                eprintln!("フレームキャプチャエラー: {}", e);
                continue;
            }
        };

        // 5. 画像をDynamicImageに変換
        let decoded = frame.decode_image::<RgbFormat>()?;
        let width = decoded.width();
        let height = decoded.height();

        let img_buffer: ImageBuffer<Rgb<u8>, Vec<u8>> =
            ImageBuffer::from_raw(width, height, decoded.into_raw())
                .ok_or("画像バッファの作成に失敗")?;

        let dynamic_image = DynamicImage::ImageRgb8(img_buffer);

        // 6. 入力画像を準備する (前処理)
        // MediaPipeの仕様に合わせて画像をリサイズ・正規化する
        let resized_image =
            dynamic_image.resize_exact(224, 224, image::imageops::FilterType::Triangle);

        // テンソルに変換 (NCHW形式: バッチ, チャンネル, 高さ, 幅)
        let tensor: Tensor =
            tract_ndarray::Array4::from_shape_fn((1, 3, 224, 224), |(_, c, y, x)| {
                let pixel = resized_image.get_pixel(x as u32, y as u32);
                pixel[c] as f32 / 255.0
            })
            .into();

        // 7. 推論を実行する
        let result = model.run(tvec!(tensor.into()))?;

        // 8. 結果を解析する (後処理)
        let landmarks = result[0].as_slice::<f32>()?;

        // 9. ランドマークを描画
        let mut display_image = dynamic_image.to_rgb8();
        draw_landmarks(&mut display_image, landmarks, width, height);

        // 10. ウィンドウに表示するためにRGB8からu32バッファに変換
        let buffer: Vec<u32> = display_image
            .pixels()
            .map(|p| {
                let r = p[0] as u32;
                let g = p[1] as u32;
                let b = p[2] as u32;
                (r << 16) | (g << 8) | b
            })
            .collect();

        // 11. ウィンドウを更新
        window.update_with_buffer(&buffer, width as usize, height as usize)?;

        // フレームカウントとランドマーク情報を表示（デバッグ用）
        frame_count += 1;
        if frame_count % 30 == 0 {
            println!("フレーム {}: {} ランドマークを検出", frame_count, landmarks.len() / 3);
        }
    }

    println!("プログラムを終了します。");
    Ok(())
}
