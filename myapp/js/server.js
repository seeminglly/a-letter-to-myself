const express = require("express");
const { Pool } = require("pg");
const cors = require("cors");

const app = express();
app.use(cors()); // CORS 허용
app.use(express.json());


const pool = new Pool({
  user: "postgres",
  host: "localhost",
  database: "mydatabase",
  password: "0718",
  port: 5432,
});

const insertSampleData = async () => {
  const query = `
    INSERT INTO myapp_letters (title, content, letter_date) VALUES
    ('크리스마스 다짐', '행복하자 🎄', '2023-12-25'),
    ('새해 목표', '운동하기 🏃‍♂️', '2024-01-01'),
    ('오늘의 다짐', '파이팅! 💪', '2024-03-03'),
    ('6개월 후 나에게', '잘 지내? 🕰️', '2024-06-01'),
    ('1년 후 나에게', '어떤 모습일까?', '2025-01-01');
  `;

  try {
    await pool.query(query);
    console.log("✅ 샘플 데이터 추가 완료!");
  } catch (err) {
    console.error("❌ 데이터 추가 실패:", err);
  } finally {
    pool.end();
  }
};

// 편지 목록 가져오기 API
app.get("/myapp_letters", async (req, res) => {
    try {
      const result = await pool.query("SELECT * FROM letters ORDER BY letter_date ASC");
      res.json(result.rows);
    } catch (err) {
      console.error(err);
      res.status(500).send("서버 오류");
    }
  });
  
  // 서버 실행
  app.listen(5000, () => console.log("🚀 서버 실행 중 (포트: 5000)"));

insertSampleData();
