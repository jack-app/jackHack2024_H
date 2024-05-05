export const Settings = () => {
  return (
    <>
      <p>新しい課題を自動でカレンダーに保存しますか？</p>
      <a className="btn btn-primary" href="#">
        はい
      </a>
      <a className="btn btn-primary" href="#">
        いいえ
      </a>

      <form action="#" method="post">
        <label htmlFor="message">デフォルトの所要時間</label>
        <textarea name="message" id="message" rows={1}></textarea>
        <button type="submit">OK</button>
      </form>
    </>
  );
};
