use ndarray::{Array, CowArray, IxDyn};
use ort::SessionBuilder;
use std::sync::Arc;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // ONNXランタイムの初期化
    let environment = Arc::new(ort::Environment::builder().with_name("test").build()?);

    // ONNXモデルの読み込み
    // 注: このパスはプロジェクトのルートからの相対パスです。
    // cargo run を hand-tracker ディレクトリで実行する場合、
    // パスは "../models/hand_landmark_full.onnx" になります。
    let session =
        SessionBuilder::new(&environment)?.with_model_from_file("./hand_landmark_full.onnx")?;

    println!("ONNX model loaded successfully.");

    // 入力テンソルの形状を取得 (モデルに依存)
    // hand_landmark_full.tflite の入力形状は [1, 256, 256, 3] です
    let input_shape = &[1, 256, 256, 3];
    let input_size: usize = input_shape.iter().product();

    // ダミーの入力データを作成 (すべて0.0)
    let dummy_input: Array<f32, _> = Array::zeros(IxDyn(input_shape));

    println!("Dummy input created with shape: {:?}", dummy_input.shape());

    // CowArray に変換
    let input_cow = CowArray::from(&dummy_input);

    // 推論の実行
    let outputs = session.run(vec![ort::Value::from_array(
        session.allocator(),
        &input_cow,
    )?])?;

    println!("Inference completed successfully.");

    // 出力テンソルの情報を表示
    for (i, output) in outputs.iter().enumerate() {
        let output_tensor = output.try_extract::<f32>()?;
        let view = output_tensor.view();
        let shape = view.shape();
        println!("Output {}: shape={:?}", i, shape);
    }

    Ok(())
}
