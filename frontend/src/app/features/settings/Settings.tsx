import { useEffect, useState } from 'react';
import { storage } from '../../storageManager';
import { auto } from '@twind/core';

export const Settings = () => {
  const [autoSave, setAutoSave] = useState(false);
  const [defaultTime, setDefaultTime] = useState(60);

  const getSttings = async () => {
    const autoSave = (await storage.get('autoSave')) as boolean;
    const defaultTime = (await storage.get('defaultTime')) as number;
    return { autoSave, defaultTime };
  };

  useEffect(() => {
    (async () => {
      const settings = await getSttings();
      setAutoSave(settings.autoSave);
      setDefaultTime(settings.defaultTime);
    })();
  }, []);

  const save = () => {
    chrome.storage.local.set({ autoSave, defaultTime });
    storage.save('autoSave', String(autoSave));
    storage.save('defaultTime', String(defaultTime));
  };

  return (
    <div>
      <div className=" flex">
        <p>新しい課題を自動でカレンダーに保存しますか？</p>
        <input
          type="checkbox"
          checked={autoSave}
          onChange={(event) => {
            setAutoSave(event.target.checked);
          }}
        />
      </div>

      <div>
        <label htmlFor="message">デフォルトの所要時間</label>
        <input
          type="number"
          min={0}
          max={1440}
          value={defaultTime}
          step={1}
          onChange={(event) => {
            setDefaultTime(Number(event.target.value));
          }}
        />
        <span>分</span>
      </div>

      <div>
        <button onClick={save}>OK</button>
      </div>
    </div>
  );
};
